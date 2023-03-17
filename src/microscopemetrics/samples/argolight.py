from itertools import product
from typing import List, Tuple, Union

import numpy as np
import pandas as pd
from pandas import DataFrame
from scipy.interpolate import griddata
from scipy.optimize import curve_fit
from scipy.signal import find_peaks
from skimage.transform import hough_line  # hough_line_peaks, probabilistic_hough_line

from microscopemetrics.analysis.tools import (
    compute_distances_matrix,
    compute_spots_properties,
    segment_image,
)
from microscopemetrics.samples import *

from ..utilities.utilities import airy_fun, multi_airy_fun


@register_image_analysis
class ArgolightBAnalysis(Analysis):
    """This class handles the analysis of the Argolight sample pattern B"""

    def __init__(self):
        super().__init__(
            output_description="Analysis output of the 'SPOTS' matrix (pattern B) from the argolight sample. "
            "It contains chromatic shifts and homogeneity."
        )
        self.add_data_requirement(
            name="argolight_b",
            description="Input image in the form of a numpy array",
            data_type=np.ndarray,
        )
        self.add_metadata_requirement(
            name="spots_distance",
            description="Distance between argolight spots",
            data_type=float,
            units="MICRON",
            optional=False,
        )
        self.add_metadata_requirement(
            name="pixel_size",
            description="Physical size of the voxel in z, y and x",
            data_type=Tuple[float, float, float],
            units="MICRON",
            optional=False,
        )
        self.add_metadata_requirement(
            name="sigma",
            description="Smoothing factor for objects detection",
            data_type=Tuple[float, float, float],
            optional=True,
            default=(1, 3, 3),
        )
        self.add_metadata_requirement(
            name="lower_threshold_correction_factors",
            description="Correction factor for the lower thresholds. Must be a tuple with len = nr "
            "of channels or a float if all equal",
            data_type=Union[List[float], Tuple[float], float],
            optional=True,
            default=None,
        )
        self.add_metadata_requirement(
            name="upper_threshold_correction_factors",
            description="Correction factor for the upper thresholds. Must be a tuple with len = nr "
            "of channels or a float if all equal",
            data_type=Union[List[float], Tuple[float], float],
            optional=True,
            default=None,
        )
        self.add_metadata_requirement(
            name="remove_center_cross",
            description="Remove the center cross found in some Argolight patterns",
            data_type=bool,
            optional=True,
            default=False,
        )

    def run(self):
        logger.info("Validating requirements...")
        if not self.validate_requirements():
            logger.error("Metadata requirements are not valid")
            return False

        logger.info("Analyzing spots image...")

        # Calculating the distance between spots in pixels with a security margin
        min_distance = round(
            (self.get_metadata_values("spots_distance") * 0.3)
            / max(self.get_metadata_values("pixel_size")[-2:])
        )

        # Calculating the maximum tolerated distance in microns for the same spot in a different channels
        max_distance = self.get_metadata_values("spots_distance") * 0.4

        labels = segment_image(
            image=self.get_data_values("argolight_b"),
            min_distance=min_distance,
            sigma=self.get_metadata_values("sigma"),
            method="local_max",
            low_corr_factors=self.get_metadata_values(
                "lower_threshold_correction_factors"
            ),
            high_corr_factors=self.get_metadata_values(
                "upper_threshold_correction_factors"
            ),
        )

        self.output.append(
            model.Image(
                name=list(self.input.data.keys())[0],
                description="Labels image with detected spots. "
                "Image intensities correspond to roi labels.",
                data=labels,
            )
        )

        spots_properties, spots_positions = compute_spots_properties(
            image=self.get_data_values("argolight_b"),
            labels=labels,
            remove_center_cross=self.get_metadata_values("remove_center_cross"),
        )

        distances_df = compute_distances_matrix(
            positions=spots_positions,
            max_distance=max_distance,
            pixel_size=self.get_metadata_values("pixel_size"),
        )

        properties_kv = {}
        properties_ls = []

        for ch, ch_spot_props in enumerate(spots_properties):
            ch_df = DataFrame()
            ch_df["channel"] = [ch for _ in ch_spot_props]
            ch_df["mask_labels"] = [p["label"] for p in ch_spot_props]
            ch_df["volume"] = [p["area"] for p in ch_spot_props]
            ch_df["roi_volume_units"] = "VOXEL"
            ch_df["max_intensity"] = [p["max_intensity"] for p in ch_spot_props]
            ch_df["min_intensity"] = [p["min_intensity"] for p in ch_spot_props]
            ch_df["mean_intensity"] = [p["mean_intensity"] for p in ch_spot_props]
            ch_df["integrated_intensity"] = [
                p["integrated_intensity"] for p in ch_spot_props
            ]
            ch_df["z_weighted_centroid"] = [
                p["weighted_centroid"][0] for p in ch_spot_props
            ]
            ch_df["y_weighted_centroid"] = [
                p["weighted_centroid"][1] for p in ch_spot_props
            ]
            ch_df["x_weighted_centroid"] = [
                p["weighted_centroid"][2] for p in ch_spot_props
            ]
            ch_df["roi_weighted_centroid_units"] = "PIXEL"

            # Key metrics for spots intensities
            properties_kv[f"nr_of_spots_ch{ch:02d}"] = len(ch_df)
            properties_kv[f"max_intensity_ch{ch:02d}"] = (
                ch_df["integrated_intensity"].max().item()
            )
            properties_kv[f"max_intensity_roi_ch{ch:02d}"] = (
                ch_df["integrated_intensity"].argmax().item()
            )
            properties_kv[f"min_intensity_ch{ch:02d}"] = (
                ch_df["integrated_intensity"].min().item()
            )
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
                (ch_df["integrated_intensity"] - ch_df["integrated_intensity"].mean())
                .abs()
                .mean()
            )
            properties_kv[f"min-max_intensity_ratio_ch{ch:02d}"] = (
                properties_kv[f"min_intensity_ch{ch:02d}"]
                / properties_kv[f"max_intensity_ch{ch:02d}"]
            )

            properties_ls.append(ch_df)

            channel_shapes = [
                model.Point(
                    x=p["weighted_centroid"][2].item(),
                    y=p["weighted_centroid"][1].item(),
                    z=p["weighted_centroid"][0].item(),
                    c=ch,
                    label=f'{p["label"]}',
                )
                for p in ch_spot_props
            ]
            self.output.append(
                model.Roi(
                    name=f"Centroids_ch{ch:03d}",
                    description=f"weighted centroids channel {ch}",
                    shapes=channel_shapes,
                )
            )

        properties_df = pd.concat(properties_ls)

        distances_kv = {"distance_units": self.get_metadata_units("pixel_size")}

        for a, b in product(
            distances_df.channel_a.unique(), distances_df.channel_b.unique()
        ):
            temp_df = distances_df[
                (distances_df.channel_a == a) & (distances_df.channel_b == b)
            ]
            a = int(a)
            b = int(b)

            distances_kv[
                f"mean_3d_dist_ch{a:02d}_ch{b:02d}"
            ] = temp_df.dist_3d.mean().item()
            distances_kv[
                f"median_3d_dist_ch{a:02d}_ch{b:02d}"
            ] = temp_df.dist_3d.median().item()
            distances_kv[
                f"std_3d_dist_ch{a:02d}_ch{b:02d}"
            ] = temp_df.dist_3d.std().item()
            distances_kv[f"mad_3d_dist_ch{a:02d}_ch{b:02d}"] = (
                (temp_df.dist_3d - temp_df.dist_3d.mean()).abs().mean().item()
            )
            distances_kv[
                f"mean_z_dist_ch{a:02d}_ch{b:02d}"
            ] = temp_df.z_dist.mean().item()
            distances_kv[
                f"median_z_dist_ch{a:02d}_ch{b:02d}"
            ] = temp_df.z_dist.median().item()
            distances_kv[
                f"std_z_dist_ch{a:02d}_ch{b:02d}"
            ] = temp_df.z_dist.std().item()
            distances_kv[f"mad_z_dist_ch{a:02d}_ch{b:02d}"] = (
                (temp_df.z_dist - temp_df.z_dist.mean()).abs().mean().item()
            )

        self.output.append(
            model.KeyValues(
                name="Intensity Key Annotations",
                description="Key Intensity Measurements on Argolight D spots",
                key_values=properties_kv,
            )
        )

        self.output.append(
            model.KeyValues(
                name="Distances Key Annotations",
                description="Key Distance Measurements on Argolight D spots",
                key_values=distances_kv,
            )
        )

        self.output.append(
            model.Table(
                name="Properties",
                description="Analysis_argolight_D_properties",
                table=properties_df,
            )
        )

        self.output.append(
            model.Table(
                name="Distances",
                description="Analysis_argolight_D_distances",
                table=distances_df,
            )
        )

        return True


@register_image_analysis
class ArgolightEAnalysis(Analysis):
    """This class handles the analysis of the Argolight sample pattern E with lines along the X or Y axis"""

    def __init__(self):
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

    def run(self):
        """A intermediate function to specify the axis to be analyzed"""

        logger.info("Validating requirements...")
        if not self.validate_requirements():
            logger.error("Metadata requirements are not valid")
            return False

        logger.info("Analyzing resolution...")

        return self._analyze_resolution(
            image=self.get_data_values("argolight_e"),
            axis=self.get_metadata_values("axis"),
            measured_band=self.get_metadata_values("measured_band"),
            pixel_size=self.get_metadata_values("pixel_size"),
            pixel_size_units=self.get_metadata_units("pixel_size"),
        )

    def _analyze_resolution(
        self, image, axis, measured_band, pixel_size, pixel_size_units
    ):
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
                (peak_heights[ch][ind].item(), peak_heights[ch][ind + 1].item())
                for ind in indexes
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


def _profile_to_table(profile, channel):
    table = {f"raw_profile_ch{channel:02d}": [v.item() for v in profile[0, :]]}

    for p in range(1, profile.shape[0]):
        table.update(
            {
                f"fitted_profile_ch{channel:03d}_peak{p:03d}": [
                    v.item() for v in profile[p, :]
                ]
            }
        )

    return table


def _fit(
    profile, peaks_guess, amp=4, exp=2, lower_amp=3, upper_amp=5, center_tolerance=1
):
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
    channel, axis, prominence, measured_band, do_fitting=True, do_angle_refinement=False
):
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
        peak_positions, peak_heights, fitted_profiles = _fit(
            normalized_profile, peak_positions
        )
        normalized_profile = np.append(
            np.expand_dims(normalized_profile, 0), fitted_profiles, axis=0
        )

    # Find the closest peaks to return it as a measure of resolution
    peaks_distances = [
        abs(a - b) for a, b in zip(peak_positions[0:-2], peak_positions[1:-1])
    ]
    res = min(peaks_distances)  # TODO: capture here the case where there are no peaks!
    res_indices = [i for i, x in enumerate(peaks_distances) if x == res]

    return normalized_profile, z_focus, peak_positions, peak_heights, res, res_indices


def _compute_resolution(
    image, axis, measured_band, prominence, do_angle_refinement=False
):
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
