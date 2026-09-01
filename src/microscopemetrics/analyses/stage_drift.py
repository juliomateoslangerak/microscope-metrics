from datetime import datetime
from os import rename

import microscopemetrics_schema.datamodel as mm_schema
import numpy as np
import pandas as pd
from scipy.signal import correlate
from skimage.registration import phase_cross_correlation

import microscopemetrics as mm
from microscopemetrics.analyses import analysis_tools as mm_analysis_tools
from microscopemetrics.analyses import schema_tools as mm_schema_tools

# Fraction of the available lags fitted by `_compute_msd_key_measurements`. The
# long lags are averaged over too few samples to be worth fitting.
_MSD_FIT_MAX_LAG_FRACTION = 0.25

_RELATIVE_POSITION_COLUMNS = [
    "relative_position_pixel_z",
    "relative_position_pixel_y",
    "relative_position_pixel_x",
    "relative_position_micron_z",
    "relative_position_micron_y",
    "relative_position_micron_x",
]


def _squared_column_name(column, quantity):
    """Rename a relative position column into a squared quantity of `quantity`.

    Squaring squares the units too, so pixel becomes pixel2 and micron micron2.
    """
    return (
        column.replace("relative_position", quantity)
        .replace("_pixel_", "_pixel2_")
        .replace("_micron_", "_micron2_")
    )


def _compute_relative_positions(
    channel: np.ndarray,
    reference_frame: int,
    voxel_size_micron,
):
    relative_positions = pd.DataFrame(
        [
            phase_cross_correlation(
                channel[reference_frame],
                t_point_array,
                upsample_factor=4,
            )[0]
            for t_point_array in channel
        ],
        columns=[
            "relative_position_pixel_z",
            "relative_position_pixel_y",
            "relative_position_pixel_x",
        ],
    )
    relative_positions[
        [
            "relative_position_micron_z",
            "relative_position_micron_y",
            "relative_position_micron_x",
        ]
    ] = (
        relative_positions[
            [
                "relative_position_pixel_z",
                "relative_position_pixel_y",
                "relative_position_pixel_x",
            ]
        ].to_numpy()
        * voxel_size_micron
    )
    return relative_positions


def _compute_displacements(relative_positions):
    displacements = (
        relative_positions[_RELATIVE_POSITION_COLUMNS]
        .diff()
        .rename(columns=lambda c: c.replace("relative_position", "displacement"))
    )
    displacements["displacement_micron_3d"] = np.linalg.norm(
        displacements[
            [
                "displacement_micron_z",
                "displacement_micron_y",
                "displacement_micron_x",
            ]
        ],
        axis=1,
    )

    return displacements


def _compute_square_displacements(relative_positions, reference_frame):
    """Square displacement of every time point with respect to the reference frame.

    Relative positions are already expressed with respect to the reference
    frame, so this is their square. Unlike the MSD, this is a per-time-point
    quantity: it is the single origin, unaveraged estimate of the MSD at a lag
    of `lag_from_reference_t_points`, which equals the time point only when the
    reference frame is the first one.
    """
    square_displacements = (
        relative_positions[_RELATIVE_POSITION_COLUMNS]
        .pow(2)
        .rename(columns=lambda c: _squared_column_name(c, "square_displacement"))
    )
    square_displacements["square_displacement_micron2_3d"] = square_displacements[
        [f"square_displacement_micron2_{axis}" for axis in "zyx"]
    ].sum(axis=1)
    square_displacements["lag_from_reference_t_points"] = np.abs(
        relative_positions.index - reference_frame
    )

    return square_displacements


def _compute_msd(measurements):
    """Ensemble and time averaged mean square displacement at every accessible lag.

    For a lag of n time points, MSD(n) is the mean of |r(t + n) - r(t)|**2 over
    every time origin t of every image. Pooling the images raises the number of
    samples per lag, which is what makes the long lags usable at all.
    `validate_images_requirements` rejects images that do not share the same
    number of time points, so every image contributes the same number of samples
    and they are all weighted equally.
    """
    per_image_positions = [
        image_measurements.sort_values("t_point")[_RELATIVE_POSITION_COLUMNS]
        for _, image_measurements in measurements.groupby("image_id", sort=False)
    ]
    lags = range(1, min(len(positions) for positions in per_image_positions))
    pooled_displacements = [
        pd.concat([positions.diff(periods=lag) for positions in per_image_positions])
        for lag in lags
    ]
    msd = pd.DataFrame(
        [displacements.pow(2).mean() for displacements in pooled_displacements],
        columns=_RELATIVE_POSITION_COLUMNS,
    ).rename(columns=lambda c: _squared_column_name(c, "msd"))
    msd.insert(0, "lag_t_points", list(lags))
    msd.insert(1, "msd_n_images", len(per_image_positions))
    msd.insert(
        2,
        "msd_n_samples",
        [len(displacements.dropna(how="all")) for displacements in pooled_displacements],
    )
    msd["msd_micron2_3d"] = msd[[f"msd_micron2_{axis}" for axis in "zyx"]].sum(axis=1)

    return msd


def _compute_velocities(
    displacements,
    time_intervals,
):
    if time_intervals is None:
        nans_list = [np.nan for _ in displacements["displacement_pixel_z"]]
        return pd.DataFrame(
            {
                "displacement_micron_z": nans_list,
                "displacement_micron_y": nans_list,
                "displacement_micron_x": nans_list,
                "displacement_micron_3d": nans_list,
                "time_interval": nans_list,
            }
        )

    velocities = (
        displacements[
            [
                "displacement_micron_z",
                "displacement_micron_y",
                "displacement_micron_x",
                "displacement_micron_3d",
            ]
        ]
        # We assume that the first time point interval is not relevant as is t=0
        .div(time_intervals[1:])
        .rename(columns=lambda c: c.replace("displacement", "velocity"))
        .rename(columns=lambda c: c.replace("micron", "micron_per_sec"))
    )
    time_intervals[0] = np.nan
    velocities.insert(0, "time_interval", time_intervals)

    return velocities


def _merge_measurements(
    image_id,
    relative_positions,
    displacements,
    velocities,
    square_displacements,
):
    """Merge the per-time-point measurements of one image into a single table.

    All of these measurements are indexed by time point, so they are simply put
    side by side. The MSD is deliberately not part of this table: it is indexed
    by lag, which is a different axis, and is returned separately.
    """
    measurements = pd.concat(
        [
            relative_positions,
            displacements,
            pd.DataFrame(velocities),
            square_displacements,
        ],
        axis=1,
    )
    measurements.insert(0, "image_id", image_id)
    measurements.insert(1, "t_point", range(len(relative_positions)))

    return measurements


def _linear_fit(x, y):
    """Unweighted least squares fit of y = slope * x + intercept and its r2.

    Returns NaN for everything if fewer than two points are usable or if x does
    not vary, and a NaN r2 if y does not vary, as the fit explains no variance
    that could be quantified.
    """
    usable = np.isfinite(x) & np.isfinite(y)
    if usable.sum() < 2:
        return np.nan, np.nan, np.nan

    x, y = x[usable], y[usable]
    x_deviation = x - x.mean()
    y_deviation = y - y.mean()
    x_variation = np.sum(x_deviation**2)
    if not x_variation:
        return np.nan, np.nan, np.nan

    slope = np.sum(x_deviation * y_deviation) / x_variation
    intercept = y.mean() - slope * x.mean()
    y_variation = np.sum(y_deviation**2)
    if not y_variation:
        return slope, intercept, np.nan
    r2 = 1 - np.sum((y - slope * x - intercept) ** 2) / y_variation

    return slope, intercept, r2


def _compute_msd_key_measurements(msd_measurements, max_lag=None):
    """Fit the MSD against the lag and extract slope, intercept and r2.

    MSD(n) = slope * n + intercept is fitted up to `max_lag`, which defaults to
    the first `_MSD_FIT_MAX_LAG_FRACTION` of the available lags. The long lags
    are averaged over progressively fewer samples, see `msd_n_samples`, so
    including them would let the noisiest points drive an unweighted fit. At
    least two lags are always fitted, but with only two the fit is exact by
    construction and its r2 carries no information.

    For purely diffusive motion the slope is proportional to the diffusion
    coefficient and the intercept to the squared localization error, while a low
    r2 flags a MSD that is not linear in the lag, as happens with directed
    drift.

    r2 is reported once per axis rather than once per unit because it does not
    depend on the unit: the micron MSD is the pixel MSD scaled by the squared
    voxel size, and scaling y by a constant leaves r2 unchanged. It is taken
    from the pixel fit, which stays available when the voxel size is unknown.
    """
    if max_lag is None:
        max_lag = max(2, int(np.ceil(len(msd_measurements) * _MSD_FIT_MAX_LAG_FRACTION)))
    fitted_msd = msd_measurements[msd_measurements["lag_t_points"] <= max_lag]

    lags = fitted_msd["lag_t_points"].to_numpy(dtype=float)
    fits = {
        (unit, axis): _linear_fit(
            lags,
            fitted_msd[f"msd_{squared_unit}_{axis}"].to_numpy(dtype=float),
        )
        for unit, squared_unit in (("pixel", "pixel2"), ("micron", "micron2"))
        for axis in "xyz"
    }
    fits["micron", "3d"] = _linear_fit(
        lags,
        fitted_msd["msd_micron2_3d"].to_numpy(dtype=float),
    )

    fitted = (
        [("pixel", axis) for axis in "xyz"]
        + [("micron", axis) for axis in "xyz"]
        + [("micron", "3d")]
    )
    key_measurements = {f"msd_slope_{unit}_{axis}": fits[unit, axis][0] for unit, axis in fitted}
    key_measurements |= {
        f"msd_intercept_{unit}_{axis}": fits[unit, axis][1] for unit, axis in fitted
    }
    key_measurements |= {f"msd_r2_{axis}": fits["pixel", axis][2] for axis in "xyz"}
    key_measurements["msd_r2_3d"] = fits["micron", "3d"][2]

    return pd.DataFrame([key_measurements])


def _generate_key_measurements(image_properties, msd_key_measurements):
    measurement_aggregation_columns = [
        "relative_position_pixel_x",
        "relative_position_pixel_y",
        "relative_position_pixel_z",
        "relative_position_micron_x",
        "relative_position_micron_y",
        "relative_position_micron_z",
        "displacement_pixel_x",
        "displacement_pixel_y",
        "displacement_pixel_z",
        "displacement_micron_x",
        "displacement_micron_y",
        "displacement_micron_z",
        "displacement_micron_3d",
        "velocity_micron_per_sec_x",
        "velocity_micron_per_sec_y",
        "velocity_micron_per_sec_z",
        "velocity_micron_per_sec_3d",
    ]

    # `agg` puts the statistics on the index, so it is unstacked into a single
    # row of <column>_<statistic> values, which is what the schema expects.
    aggregated_measurements = (
        image_properties[measurement_aggregation_columns]
        .agg(["mean", "median", "std"])
        .unstack()
        .to_frame()
        .T
    )
    aggregated_measurements.columns = aggregated_measurements.columns.map("_".join)

    key_measurements = pd.concat([aggregated_measurements, msd_key_measurements], axis=1)

    return [
        mm_schema.StageDriftKeyMeasurement(**km)
        for km in key_measurements.to_dict(orient="records")
    ]


def _process_image(
    image: mm_schema.Image,
    channel_nr: int,
    reference_frame_nr: int,
    snr_threshold: float,
):
    image_id = mm_schema_tools.get_object_id(image) or image.name
    mm.logger.info(f"Processing image {image_id}...")

    voxel_size_micron = (
        image.voxel_size_z_micron or np.nan,
        image.voxel_size_y_micron or np.nan,
        image.voxel_size_x_micron or np.nan,
    )
    try:
        time_intervals = image.time_series.time_points_sec
    except AttributeError:
        time_intervals = None

    relative_positions = _compute_relative_positions(
        channel=image.array_data[..., channel_nr],
        reference_frame=reference_frame_nr,
        voxel_size_micron=voxel_size_micron,
    )

    displacements = _compute_displacements(relative_positions)

    velocities = _compute_velocities(
        displacements,
        time_intervals,
    )

    square_displacements = _compute_square_displacements(
        relative_positions,
        reference_frame=reference_frame_nr,
    )

    return _merge_measurements(
        image_id=image_id,
        relative_positions=relative_positions,
        displacements=displacements,
        velocities=velocities,
        square_displacements=square_displacements,
    )


def analyse_stage_drift(dataset: mm_schema.StageDriftDataset) -> bool:
    mm_schema_tools.validate_images_requirements(
        images_list=dataset.input_data.beads_images,
        axis_to_check_shape=[0, 1, 2, 3, 4],
        saturation_threshold=dataset.input_parameters.saturation_threshold,
        bit_depth=dataset.input_parameters.bit_depth,
    )

    # Containers for input data and input parameters
    snr_threshold = dataset.input_parameters.snr_threshold
    channel_nr = dataset.input_parameters.channel_nr
    reference_frame_nr = dataset.input_parameters.reference_frame_nr

    image_properties = []

    for image in dataset.input_data.beads_images:
        # TODO: implement here the use ot the analysis_roi
        image_properties.append(
            _process_image(
                image=image,
                channel_nr=channel_nr,
                reference_frame_nr=reference_frame_nr,
                snr_threshold=snr_threshold,
            )
        )

    image_properties = pd.concat(image_properties, ignore_index=True)
    msd = _compute_msd(image_properties)
    msd_key_measurements = _compute_msd_key_measurements(msd)

    # Key measurements are generated while these are still dataframes, before
    # they are converted into microscope-metrics tables.
    key_measurements = _generate_key_measurements(
        image_properties,
        msd_key_measurements,
    )

    image_properties = mm_schema_tools.df_to_table(
        image_properties,
        name="stage_drift_image_measurements",
        description="Image level stage drift measurements",
    )
    msd = mm_schema_tools.df_to_table(
        msd,
        name="stage_drift_msd_measurements",
        description="Dataset level stage drift mean square displacement measurements",
    )

    dataset.output = mm_schema.StageDriftOutput(
        processing_application=mm.__name__,
        processing_version=mm.__version__,
        processing_datetime=datetime.now(),
        key_measurements=key_measurements,
        image_properties=image_properties,
        mean_square_displacements=msd,
    )

    dataset.processed = True

    return True
