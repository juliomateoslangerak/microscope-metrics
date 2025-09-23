import logging
from datetime import datetime
from typing import Dict, List, Tuple

import microscopemetrics_schema.datamodel as mm_schema
import numpy as np
import pandas as pd
import scipy

import microscopemetrics as mm
from microscopemetrics.analyses import tools as mm_tools

# TODO: Determine what are we going to consider the threshold for measuring stability
REQ_NR_LINEARITY = 10
REQ_NR_STABILITY_SHORT_TERM = 100
REQ_NR_STABILITY_LONG_TERM = 100


def _stability(values: np.ndarray) -> float:
    p_max = np.max(values)
    p_min = np.min(values)
    return 1 - ((p_max - p_min) / (p_max + p_min))


def _is_constant(series: pd.Series) -> bool:
    """Check if a series has at most one unique non-NaN value."""
    non_na = series.dropna().unique()
    return len(non_na) <= 1


def _is_regular_timeseries(series: pd.Series) -> bool:
    """Check if a datetime series has regular intervals."""
    deltas = series.diff().dt.total_seconds().unique()
    return len(deltas) == 1


def _is_equally_spaced(values: np.ndarray, tol=1e-8) -> bool:
    """Check if sorted values are equally spaced within tolerance."""
    diffs = np.diff(np.sort(values))
    return np.allclose(diffs, diffs[0], atol=tol)


def _find_linearity_subset(
    df: pd.DataFrame,
    min_points: int = 10,
) -> pd.DataFrame | None:
    """
    Find the single longest contiguous block of rows where light source power linearity can be assessed.

    Returns a copy of the subset DataFrame or None if none found.
    Assumes df is ordered by acquisition_datetime (contiguity is with respect to df order).
    """
    if df.empty:
        return None

    linearity_subset_df = df.copy()

    linearity_mask = (
        linearity_subset_df["power_set_point"] == linearity_subset_df["power_set_point"].shift()
    )
    groups = linearity_mask.cumsum()

    # Find the rows where power_set_point changes
    groups = linearity_subset_df.groupby(groups).agg(
        {"acquisition_datetime": ["count", "min", "max"]}
    )

    # Select the group with the maximum count of acquisition_datetime
    linearity_group = groups[
        groups["acquisition_datetime"]["count"] == groups["acquisition_datetime"]["count"].max()
    ]
    if (
        linearity_group.empty
        or linearity_group["acquisition_datetime"]["count"].values[0] < min_points
    ):
        return None

    start_time = linearity_group["acquisition_datetime"]["min"].values[0]
    end_time = linearity_group["acquisition_datetime"]["max"].values[0]
    subset = linearity_subset_df[
        (linearity_subset_df["acquisition_datetime"] >= start_time)
        & (linearity_subset_df["acquisition_datetime"] <= end_time)
    ]

    return subset.copy()


def _find_stability_subsets(
    df: pd.DataFrame,
    min_points_short_term: int = 100,
    min_points_long_term: int = 100,
) -> List[pd.DataFrame] | None:
    """
    Find the contiguous blocks of rows where light source power stability can be assessed.

    Returns a list of the subset DataFrames or None if none found.
    Assumes df is ordered by acquisition_datetime (contiguity is with respect to df order).
    """
    if df.empty:
        return None

    stability_subset_df = df.copy()

    # Find the rows where power_set_point does not change, integration_time_seconds does not change,
    # and diff between acquisition_datetime is constant
    set_point_mask = (
        stability_subset_df["power_set_point"] != stability_subset_df["power_set_point"].shift()
    )
    integration_time_mask = (
        stability_subset_df["integration_time_seconds"]
        != stability_subset_df["integration_time_seconds"].shift()
    )
    interval_time_mask = (
        stability_subset_df["acquisition_datetime"].diff().dt.total_seconds().fillna(0)
        != stability_subset_df["acquisition_datetime"].diff().dt.total_seconds().fillna(0).shift()
    )

    stability_mask = set_point_mask | integration_time_mask | interval_time_mask

    groups = stability_mask.cumsum()
    groups = stability_subset_df.groupby(groups).agg(
        {"acquisition_datetime": ["count", "min", "max"]}
    )

    # Select the group with the maximum count of acquisition_datetime
    stability_groups = groups[
        groups["acquisition_datetime"]["count"] >= min(min_points_short_term, min_points_long_term)
    ]
    if stability_groups.empty:
        return None

    start_times = stability_groups["acquisition_datetime"]["min"].values
    end_times = stability_groups["acquisition_datetime"]["max"].values

    return [
        stability_subset_df[
            (stability_subset_df["acquisition_datetime"] >= start)
            & (stability_subset_df["acquisition_datetime"] <= end)
        ].copy()
        for start, end in zip(start_times, end_times)
    ]


def _compute_basic_measurement(measurements: pd.DataFrame) -> Dict:
    return {
        "nr_of_measurements": len(measurements),
        "power_mean_mw": measurements["power_mw"].mean(),
        "power_median_mw": measurements["power_mw"].median(),
        "power_std_mw": measurements["power_mw"].std(),
        "power_min_mw": measurements["power_mw"].min(),
        "power_max_mw": measurements["power_mw"].max(),
    }


def _compute_linearity(measurements: pd.DataFrame) -> Dict:
    pass


def _compute_stability(
    measurements: pd.DataFrame, short_long_term_threshold_seconds: float
) -> Dict:
    time_deltas = measurements["acquisition_datetime"].diff().dt.total_seconds().fillna(0).values
    # The first measurement delta is always zero, so we set it to the second one
    time_deltas[0] = time_deltas[1]
    long_term_segment = time_deltas > short_long_term_threshold_seconds
    short_term_segment = ~long_term_segment

    long_term_stability = None
    long_term_measurement_duration_seconds = None
    short_term_stability = None
    short_term_measurement_duration_seconds = None
    if np.any(long_term_segment):
        # Validate that there are enough measurements for long term stability
        if np.sum(long_term_segment) < REQ_NR:
            logging.warning("Not enough measurements for long term stability analysis.")
        else:
            logging.info("Light source has long term stability measurements.")
            long_term_stability = _stability(measurements[short_term_segment]["power_mw"].values)
            long_term_measurement_duration_seconds = time_deltas[short_term_segment].mean()
    if np.any(short_term_segment):
        # Validate that there are enough measurements for short term stability
        if np.sum(short_term_segment) < REQ_NR:
            logging.warning("Not enough measurements for short term stability analysis.")
        else:
            logging.info("Light source has short term stability measurements.")
            short_term_stability = _stability(measurements[long_term_segment]["power_mw"].values)
            short_term_measurement_duration_seconds = time_deltas[long_term_segment].mean()

    return {
        "power_std_mw": measurements["power_mw"].std(),
        "short_term_power_stability": short_term_stability,
        "short_term_measurement_duration_seconds": short_term_measurement_duration_seconds,
        "long_term_power_stability": long_term_stability,
        "long_term_measurement_duration_seconds": long_term_measurement_duration_seconds,
    }


def _compute_light_source_power_key_measurements(
    power_measurements: List[mm_schema.PowerMeasurement],
    input_parameters: mm_schema.LightSourcePowerInputParameters,
) -> mm_schema.LightSourcePowerKeyMeasurements:
    power_measurement_df = pd.DataFrame.from_records(power_measurements)

    key_measurements = []

    # Go through each light source, power meter and measuring location combinations
    for light_source in power_measurement_df["light_source"].drop_duplicates(ignore_index=True):
        for measurement_device in power_measurement_df["measurement_device"].drop_duplicates(
            ignore_index=True
        ):
            for measuring_location in power_measurement_df["measuring_location"].drop_duplicates(
                ignore_index=True
            ):
                logging.info(
                    f"Processing light source {light_source}, "
                    f"measurement device {measurement_device}, "
                    f"measuring location {measuring_location}."
                )

                subset_key_measurements = {
                    "light_source": light_source,
                    "measurement_device": measurement_device,
                    "measuring_location": measuring_location,
                    "nr_of_measurements": np.nan,
                    "power_mean_mw": np.nan,
                    "power_median_mw": np.nan,
                    "power_std_mw": np.nan,
                    "power_min_mw": np.nan,
                    "power_max_mw": np.nan,
                    "power_linearity": np.nan,
                    "short_term_power_stability": np.nan,
                    "short_term_measurement_duration_seconds": np.nan,
                    "long_term_power_stability": np.nan,
                    "long_term_measurement_duration_seconds": np.nan,
                }

                subset_df = power_measurement_df[
                    (power_measurement_df["light_source"] == light_source)
                    & (power_measurement_df["measurement_device"] == measurement_device)
                    & (power_measurement_df["measuring_location"] == measuring_location)
                ]
                subset_df = subset_df.set_index("acquisition_datetime")
                subset_df.sort_index(inplace=True)
                subset_df.reset_index(inplace=True)

                linearity_df = _find_linearity_subset(subset_df, REQ_NR_LINEARITY)
                stability_dfs = _find_stability_subsets(subset_df)

                # Catch the case where we have only one measurement
                if len(subset_df) == 1:
                    logging.info("Only one measurement found. Extracting basic statistics.")
                    subset_key_measurements |= _compute_basic_measurement(subset_df)
                    key_measurements.append(subset_key_measurements)

                    continue

                # Get basic statistics following these rules:
                # 1. If there is a single power set point with less than REQ_NR measurements, use it for basic statistics
                # 2. If there are a single power set point with more than REQ_NR measurements, use it for basic statistics
                # 3. throw an error otherwise

                power_set_point_counts = subset_df["power_set_point"].value_counts()
                linearity_set_point_counts = power_set_point_counts[power_set_point_counts == 1]
                basic_statistics_set_point_counts = power_set_point_counts[
                    (power_set_point_counts > 1) & (power_set_point_counts <= REQ_NR)
                ]
                stability_set_point_counts = power_set_point_counts[power_set_point_counts > REQ_NR]

                if len(basic_statistics_set_point_counts) == 1:
                    logging.warning(
                        "Some power measurements do not have enough values for stability analysis."
                        "These will be used for the basic statistics."
                    )
                    subset_key_measurements |= _compute_basic_measurement(
                        subset_df[
                            subset_df["power_set_point"].isin(
                                basic_statistics_set_point_counts.index
                            )
                        ]
                    )
                elif len(stability_set_point_counts) == 1:
                    logging.info("Getting basic statistics from stability measurements.")
                    subset_key_measurements |= _compute_basic_measurement(
                        subset_df[
                            subset_df["power_set_point"].isin(stability_set_point_counts.index)
                        ]
                    )
                else:
                    logging.error(
                        "Could not determine which measurements to use for basic statistics."
                    )

                if (
                    0 < len(stability_set_point_counts) < 3
                ):  # We might one or two power set points for stability
                    logging.info("Computing stability.")
                    subset_key_measurements |= _compute_stability(
                        short_long_term_threshold_seconds=input_parameters.short_long_term_threshold_seconds,
                        measurements=subset_df[
                            subset_df["power_set_point"].isin(stability_set_point_counts.index)
                        ],
                    )
                else:
                    logging.warning("Not enough measurements for stability analysis.")

                if len(linearity_set_point_counts) > 9:
                    logging.info("Computing linearity.")
                    subset_key_measurements |= _compute_linearity(
                        subset_df[
                            subset_df["power_set_point"].isin(linearity_set_point_counts.index)
                        ]
                    )
                else:
                    logging.warning("Not enough measurements for linearity analysis.")

                key_measurements.append(subset_key_measurements)

    key_measurements = {
        k: list(v)
        for k, v in zip(key_measurements[0], zip(*[d.values() for d in key_measurements]))
    }

    return mm_schema.LightSourcePowerKeyMeasurements(**key_measurements)


def analyse_light_source_power(dataset: mm_schema.LightSourcePowerDataset) -> bool:
    mm.analyses.validate_requirements()

    key_measurements = _compute_light_source_power_key_measurements(
        power_measurements=dataset.input_data.power_measurements,
        input_parameters=dataset.input_parameters,
    )

    dataset.output = mm_schema.LightSourcePowerOutput(
        processing_application="microscopemetrics",
        processing_version=mm.__version__,
        processing_datetime=datetime.now(),
        key_measurements=key_measurements,
    )

    dataset.processed = True

    return True
