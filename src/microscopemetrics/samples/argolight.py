from datetime import datetime
from itertools import product
from typing import Dict, List, Tuple, Union

import numpy as np
import pandas as pd
from numpy import float64, int64, ndarray
from pandas import DataFrame
from scipy.interpolate import griddata
from scipy.optimize import curve_fit
from scipy.signal import find_peaks
from skimage.transform import hough_line  # hough_line_peaks, probabilistic_hough_line

import microscopemetrics.data_schema.samples.argolight_schema as schema
from microscopemetrics.analysis.tools import (
    compute_distances_matrix,
    compute_spots_properties,
    segment_image,
)
from microscopemetrics.data_schema import core_schema
from microscopemetrics.samples import (
    AnalysisMixin,
    logger,
    numpy_to_inlined_image,
    numpy_to_inlined_mask,
)
from microscopemetrics.utilities.utilities import airy_fun, is_saturated, multi_airy_fun


class ArgolightBAnalysis(schema.ArgolightBDataset, AnalysisMixin):
    """This class handles the analysis of the Argolight sample pattern B"""

    def run(self) -> bool:
        self.validate_requirements()

        # Check image shape
        logger.info("Checking image shape...")
        image = self.argolight_b_image.data
        if len(image.shape) != 5:
            logger.error("Image must be 5D")
            return False

        # Check image saturation
        logger.info("Checking image saturation...")
        saturated_channels = []
        for c in range(image.shape[-1]):
            if is_saturated(
                channel=image[:, :, :, :, c],
                threshold=self.saturation_threshold,
                detector_bit_depth=self.bit_depth,
            ):
                logger.error(f"Channel {c} is saturated")
                saturated_channels.append(c)
        if len(saturated_channels):
            logger.error(f"Channels {saturated_channels} are saturated")
            return False

        # Calculating the distance between spots in pixels with a security margin
        min_distance = round(self.spots_distance * 0.3)

        # Calculating the maximum tolerated distance in microns for the same spot in a different channels
        max_distance = self.spots_distance * 0.4

        labels = segment_image(
            image=image,
            min_distance=min_distance,
            sigma=(self.sigma_z, self.sigma_y, self.sigma_x),
            method="local_max",
            low_corr_factors=self.lower_threshold_correction_factors,
            high_corr_factors=self.upper_threshold_correction_factors,
        )

        self.spots_labels_image = schema.ImageAsNumpy(
            data=labels,
            name=f"{self.argolight_b_image.name}_spots_labels",
            description=f"Spots labels of {self.argolight_b_image.uri}",
            uri=None,
        )

        spots_properties, spots_positions = compute_spots_properties(
            image=image,
            labels=labels,
            remove_center_cross=self.remove_center_cross,
        )

        distances_df = compute_distances_matrix(
            positions=spots_positions,
            max_distance=max_distance,
        )

        properties_kv = {}
        properties_ls = []
        spots_centroids = []

        for ch, ch_spot_props in enumerate(spots_properties):
            ch_df = DataFrame()
            ch_df["channel"] = [ch for _ in ch_spot_props]
            ch_df["mask_labels"] = [p["label"] for p in ch_spot_props]
            ch_df["volume"] = [p["area"] for p in ch_spot_props]
            ch_df["roi_volume_units"] = "VOXEL"
            ch_df["max_intensity"] = [p["max_intensity"] for p in ch_spot_props]
            ch_df["min_intensity"] = [p["min_intensity"] for p in ch_spot_props]
            ch_df["mean_intensity"] = [p["mean_intensity"] for p in ch_spot_props]
            ch_df["integrated_intensity"] = [p["integrated_intensity"] for p in ch_spot_props]
            ch_df["z_weighted_centroid"] = [p["weighted_centroid"][0] for p in ch_spot_props]
            ch_df["y_weighted_centroid"] = [p["weighted_centroid"][1] for p in ch_spot_props]
            ch_df["x_weighted_centroid"] = [p["weighted_centroid"][2] for p in ch_spot_props]
            ch_df["roi_weighted_centroid_units"] = "PIXEL"

            # Key metrics for spots intensities
            properties_kv[f"nr_of_spots_ch{ch:02d}"] = len(ch_df)
            properties_kv[f"max_intensity_ch{ch:02d}"] = ch_df["integrated_intensity"].max().item()
            properties_kv[f"max_intensity_roi_ch{ch:02d}"] = (
                ch_df["integrated_intensity"].argmax().item()
            )
            properties_kv[f"min_intensity_ch{ch:02d}"] = ch_df["integrated_intensity"].min().item()
            properties_kv[f"min_intensity_roi_ch{ch:02d}"] = (
                ch_df["integrated_intensity"].argmin().item()
            )
            properties_kv[f"mean_intensity_ch{ch:02d}"] = (
                ch_df["integrated_intensity"].mean().item()
            )
            properties_kv[f"median_intensity_ch{ch:02d}"] = (
                ch_df["integrated_intensity"].median().item()
            )
            properties_kv[f"std_mean_intensity_ch{ch:02d}"] = (
                ch_df["integrated_intensity"].std().item()
            )
            properties_kv[f"mad_mean_intensity_ch{ch:02d}"] = (
                (ch_df["integrated_intensity"] - ch_df["integrated_intensity"].mean()).abs().mean()
            )
            properties_kv[f"min-max_intensity_ratio_ch{ch:02d}"] = (
                properties_kv[f"min_intensity_ch{ch:02d}"]
                / properties_kv[f"max_intensity_ch{ch:02d}"]
            )

            properties_ls.append(ch_df)

            channel_shapes = [
                core_schema.Point(
                    x=p["weighted_centroid"][2].item(),
                    y=p["weighted_centroid"][1].item(),
                    z=p["weighted_centroid"][0].item(),
                    c=ch,
                    label=f'{p["label"]}',
                    # TODO: put some color
                )
                for p in ch_spot_props
            ]

            spots_centroids.append(
                schema.ROI(
                    label=f"Centroids_ch{ch:03d}",
                    image=self.argolight_b_image,
                    shapes=channel_shapes,
                )
            )

        properties_df = pd.concat(properties_ls)

        distances_kv = {"distance_units": "PIXEL"}

        for a, b in product(distances_df.channel_a.unique(), distances_df.channel_b.unique()):
            temp_df = distances_df[(distances_df.channel_a == a) & (distances_df.channel_b == b)]
            a = int(a)
            b = int(b)

            distances_kv[f"mean_3d_dist_ch{a:02d}_ch{b:02d}"] = temp_df.dist_3d.mean().item()
            distances_kv[f"median_3d_dist_ch{a:02d}_ch{b:02d}"] = temp_df.dist_3d.median().item()
            distances_kv[f"std_3d_dist_ch{a:02d}_ch{b:02d}"] = temp_df.dist_3d.std().item()
            distances_kv[f"mad_3d_dist_ch{a:02d}_ch{b:02d}"] = (
                (temp_df.dist_3d - temp_df.dist_3d.mean()).abs().mean().item()
            )
            distances_kv[f"mean_z_dist_ch{a:02d}_ch{b:02d}"] = temp_df.z_dist.mean().item()
            distances_kv[f"median_z_dist_ch{a:02d}_ch{b:02d}"] = temp_df.z_dist.median().item()
            distances_kv[f"std_z_dist_ch{a:02d}_ch{b:02d}"] = temp_df.z_dist.std().item()
            distances_kv[f"mad_z_dist_ch{a:02d}_ch{b:02d}"] = (
                (temp_df.z_dist - temp_df.z_dist.mean()).abs().mean().item()
            )

        self.intensity_measurements = core_schema.KeyValues(
            keys=[k for k in properties_kv.keys()],
            values=[v for v in properties_kv.values()],
        )

        self.distance_measurements = core_schema.KeyValues(
            keys=[k for k in distances_kv.keys()],
            values=[v for v in distances_kv.values()],
        )

        self.spots_properties = schema.TableAsPandasDF(
            name="spots_properties",
            description="This table contains data describing the intensity measurements of the spots",
            df=properties_df,
        )

        self.spots_distances = schema.TableAsPandasDF(
            name="spots_distances",
            description="This table contains data describing the distance measurements between the spots in the different channels",
            df=distances_df,
        )

        self.spots_centroids = spots_centroids
        breakpoint()

        self.processing_date = datetime.today()
        self.processed = True

        return True


class ArgolightEAnalysis(AnalysisMixin):
    """This class handles the analysis of the Argolight sample pattern E with lines along the X or Y axis"""

    def __init__(self) -> None:
        super().__init__(
            output_description="Analysis output of the lines (pattern E) from the argolight sample. "
            "It contains resolution data on the axis indicated:"
            "- axis 1 = Y resolution = lines along X axis"
            "- axis 2 = X resolution = lines along Y axis"
        )
        self.add_data_requirement(
            name="argolight_e",
            description="Input image in the form of a numpy array",
            data_type=np.ndarray,
        )
        self.add_metadata_requirement(
            name="pixel_size",
            description="Physical size of the voxel in z, y and x",
            data_type=Tuple[float, float, float],
            units="MICRON",
            optional=False,
        )
        self.add_metadata_requirement(
            name="axis",
            description="axis along which resolution is being measured. 1=Y, 2=X",
            data_type=int,
            optional=False,
        )
        self.add_metadata_requirement(
            name="measured_band",
            description="Fraction of the image across which intensity profiles are measured",
            data_type=float,
            optional=True,
            default=0.4,
        )

    def _run(self) -> bool:
        """A intermediate function to specify the axis to be analyzed"""
        return self._analyze_resolution(
            image=self.get_data_values("argolight_e"),
            axis=self.get_metadata_values("axis"),
            measured_band=self.get_metadata_values("measured_band"),
            pixel_size=self.get_metadata_values("pixel_size"),
            pixel_size_units=self.get_metadata_units("pixel_size"),
        )

    def _analyze_resolution(
        self,
        image: ndarray,
        axis: int,
        measured_band: float,
        pixel_size: Tuple[float, float, float],
        pixel_size_units: str,
    ) -> bool:
        (
            profiles,
            z_planes,
            peak_positions,
            peak_heights,
            resolution_values,
            resolution_indexes,
            resolution_method,
        ) = _compute_resolution(
            image=image,
            axis=axis,
            measured_band=measured_band,
            prominence=0.264,
            do_angle_refinement=False,
        )
        # resolution in native units
        resolution_values = [x * pixel_size[axis] for x in resolution_values]

        key_values = {
            f"ch{ch:02d}_{resolution_method}_resolution": res.item()
            for ch, res in enumerate(resolution_values)
        }

        key_values["resolution_units"] = pixel_size_units
        key_values["resolution_axis"] = axis
        key_values["measured_band"] = measured_band

        for ch, indexes in enumerate(resolution_indexes):
            key_values[f"peak_positions_ch{ch:02d}"] = [
                (peak_positions[ch][ind].item(), peak_positions[ch][ind + 1].item())
                for ind in indexes
            ]
            key_values[f"peak_heights_ch{ch:02d}"] = [
                (peak_heights[ch][ind].item(), peak_heights[ch][ind + 1].item()) for ind in indexes
            ]
            key_values[f"focus_ch{ch:02d}"] = z_planes[ch].item()

        out_tables = {}

        # Populate tables and rois
        for ch, profile in enumerate(profiles):
            out_tables.update(_profile_to_table(profile, ch))
            shapes = []
            for pos in key_values[f"peak_positions_ch{ch:02d}"]:
                for peak in pos:
                    # Measurements are taken at center of pixel so we add .5 pixel to peak positions
                    if axis == 1:  # Y resolution -> horizontal rois
                        axis_len = image.shape[-2]
                        x1_pos = int((axis_len / 2) - (axis_len * measured_band / 2))
                        y1_pos = peak + 0.5
                        x2_pos = int((axis_len / 2) + (axis_len * measured_band / 2))
                        y2_pos = peak + 0.5
                    elif axis == 2:  # X resolution -> vertical rois
                        axis_len = image.shape[-1]
                        y1_pos = int((axis_len / 2) - (axis_len * measured_band / 2))
                        x1_pos = peak + 0.5
                        y2_pos = int((axis_len / 2) + (axis_len * measured_band / 2))
                        x2_pos = peak + 0.5

                    shapes.append(
                        model.Line(
                            x1=x1_pos,
                            y1=y1_pos,
                            x2=x2_pos,
                            y2=y2_pos,
                            z=z_planes[ch],
                            c=ch,
                        )
                    )

            self.output.append(
                model.Roi(
                    name=f"Peaks_ch{ch:03d}",
                    description=f"Lines where highest Rayleigh resolution was found in channel {ch}",
                    shapes=shapes,
                )
            )
        self.output.append(
            model.KeyValues(
                name="Key-Value Annotations",
                description=f"Measurements on Argolight E pattern along axis={axis}",
                key_values=key_values,
            )
        )
        self.output.append(
            model.Table(
                name="Profiles",
                description="Raw and fitted profiles across the center of the image along the "
                "defined axis",
                table=DataFrame.from_dict(out_tables),
            )
        )

        return True


def _profile_to_table(profile: ndarray, channel: int) -> Dict[str, List[float]]:
    table = {f"raw_profile_ch{channel:02d}": [v.item() for v in profile[0, :]]}

    for p in range(1, profile.shape[0]):
        table.update(
            {f"fitted_profile_ch{channel:03d}_peak{p:03d}": [v.item() for v in profile[p, :]]}
        )

    return table


def _fit(
    profile: ndarray,
    peaks_guess: List[int64],
    amp: int = 4,
    exp: int = 2,
    lower_amp: int = 3,
    upper_amp: int = 5,
    center_tolerance: int = 1,
) -> Tuple[ndarray, ndarray, ndarray]:
    guess = []
    lower_bounds = []
    upper_bounds = []
    for p in peaks_guess:
        guess.append(p)  # peak center
        guess.append(amp)  # peak amplitude
        lower_bounds.append(p - center_tolerance)
        lower_bounds.append(lower_amp)
        upper_bounds.append(p + center_tolerance)
        upper_bounds.append(upper_amp)

    x = np.linspace(0, profile.shape[0], profile.shape[0], endpoint=False)

    popt, pcov = curve_fit(
        multi_airy_fun, x, profile, p0=guess, bounds=(lower_bounds, upper_bounds)
    )

    opt_peaks = popt[::2]
    # opt_amps = [a / 4 for a in popt[1::2]]  # We normalize back the amplitudes to the unity
    opt_amps = popt[1::2]

    fitted_profiles = np.zeros((len(peaks_guess), profile.shape[0]))
    for i, (c, a) in enumerate(zip(opt_peaks, opt_amps)):
        fitted_profiles[i, :] = airy_fun(x, c, a)

    return opt_peaks, opt_amps, fitted_profiles


def _compute_channel_resolution(
    channel: ndarray,
    axis: int,
    prominence: float,
    measured_band: float,
    do_fitting: bool = True,
    do_angle_refinement: bool = False,
) -> Tuple[ndarray, int64, ndarray, ndarray, float64, List[int]]:
    """Computes the resolution on a pattern of lines with increasing separation"""
    # find the most contrasted z-slice
    z_stdev = np.std(channel, axis=(1, 2))
    z_focus = np.argmax(z_stdev)
    focus_slice = channel[z_focus]

    # TODO: verify angle and correct
    if do_angle_refinement:
        # Set a precision of 0.1 degree.
        tested_angles = np.linspace(-np.pi / 2, np.pi / 2, 1800)
        h, theta, d = hough_line(focus_slice, theta=tested_angles)

    # Cut a band of that found peak
    # Best we can do now is just to cut a band in the center
    # We create a profiles along which we average signal
    axis_len = focus_slice.shape[-axis]
    weight_profile = np.zeros(axis_len)
    # Calculates a band of relative width 'image_fraction' to integrate the profile
    weight_profile[
        int((axis_len / 2) - (axis_len * measured_band / 2)) : int(
            (axis_len / 2) + (axis_len * measured_band / 2)
        )
    ] = 1
    profile = np.average(focus_slice, axis=-axis, weights=weight_profile)

    normalized_profile = (profile - np.min(profile)) / np.ptp(profile)

    # Find peaks: We implement Rayleigh limits that will be refined downstream
    peak_positions, properties = find_peaks(
        normalized_profile,
        height=0.3,
        distance=2,
        prominence=prominence / 4,
    )

    # From the properties we are interested in the amplitude
    # peak_heights = [h for h in properties['peak_heights']]
    ray_filtered_peak_pos = []
    ray_filtered_peak_heights = []

    for peak, height, prom in zip(
        peak_positions, properties["peak_heights"], properties["prominences"]
    ):
        if (
            prom / height
        ) > prominence:  # This is calculating the prominence in relation to the local intensity
            ray_filtered_peak_pos.append(peak)
            ray_filtered_peak_heights.append(height)

    peak_positions = ray_filtered_peak_pos
    peak_heights = ray_filtered_peak_heights

    if do_fitting:
        peak_positions, peak_heights, fitted_profiles = _fit(normalized_profile, peak_positions)
        normalized_profile = np.append(
            np.expand_dims(normalized_profile, 0), fitted_profiles, axis=0
        )

    # Find the closest peaks to return it as a measure of resolution
    peaks_distances = [abs(a - b) for a, b in zip(peak_positions[0:-2], peak_positions[1:-1])]
    res = min(peaks_distances)  # TODO: capture here the case where there are no peaks!
    res_indices = [i for i, x in enumerate(peaks_distances) if x == res]

    return normalized_profile, z_focus, peak_positions, peak_heights, res, res_indices


def _compute_resolution(
    image: ndarray,
    axis: int,
    measured_band: float,
    prominence: float,
    do_angle_refinement: bool = False,
) -> Tuple[
    List[ndarray], List[int64], List[ndarray], List[ndarray], List[float64], List[List[int]], str
]:
    profiles = list()
    z_planes = []
    peaks_positions = list()
    peaks_heights = []
    resolution_values = []
    resolution_indexes = []
    resolution_method = "rayleigh"

    for c in range(image.shape[1]):  # TODO: Deal with Time here
        prof, zp, pk_pos, pk_heights, res, res_ind = _compute_channel_resolution(
            channel=np.squeeze(image[:, c, ...]),
            axis=axis,
            prominence=prominence,
            measured_band=measured_band,
            do_angle_refinement=do_angle_refinement,
        )
        profiles.append(prof)
        z_planes.append(zp)
        peaks_positions.append(pk_pos)
        peaks_heights.append(pk_heights)
        resolution_values.append(res)
        resolution_indexes.append(res_ind)

    return (
        profiles,
        z_planes,
        peaks_positions,
        peaks_heights,
        resolution_values,
        resolution_indexes,
        resolution_method,
    )


# Calculate 2D FFT
# slice_2d = raw_img[17, ...].reshape([1, n_channels, x_size, y_size])
# fft_2D = fft_2d(slice_2d)

# Calculate 3D FFT
# fft_3D = fft_3d(spots_image)
#
# plt.imshow(np.log(fft_3D[2, :, :, 1]))  # , cmap='hot')
# # plt.imshow(np.log(fft_3D[2, 23, :, :]))  # , cmap='hot')
# plt.show()
#
