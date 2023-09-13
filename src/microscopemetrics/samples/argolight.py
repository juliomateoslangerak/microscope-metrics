from datetime import datetime
from itertools import product
from typing import Any, Dict, List, Tuple, Union

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
from microscopemetrics.samples import AnalysisMixin, logger
from microscopemetrics.utilities.utilities import airy_fun, is_saturated, multi_airy_fun


class ArgolightBAnalysis(schema.ArgolightBDataset, AnalysisMixin):
    """This class handles the analysis of the Argolight sample pattern B"""

    def run(self) -> bool:
        self.validate_requirements()

        # Check image shape
        logger.info("Checking image shape...")
        image = self.input.argolight_b_image.data
        if len(image.shape) != 5:
            logger.error("Image must be 5D")
            return False

        # Check image saturation
        logger.info("Checking image saturation...")
        saturated_channels = []
        for c in range(image.shape[-1]):
            if is_saturated(
                channel=image[:, :, :, :, c],
                threshold=self.input.saturation_threshold,
                detector_bit_depth=self.input.bit_depth,
            ):
                logger.error(f"Channel {c} is saturated")
                saturated_channels.append(c)
        if len(saturated_channels):
            logger.error(f"Channels {saturated_channels} are saturated")
            return False

        # Calculating the distance between spots in pixels with a security margin
        min_distance = round(self.input.spots_distance * 0.3)

        # Calculating the maximum tolerated distance in microns for the same spot in a different channels
        max_distance = self.input.spots_distance * 0.4

        labels = segment_image(
            image=image,
            min_distance=min_distance,
            sigma=(self.input.sigma_z, self.input.sigma_y, self.input.sigma_x),
            method="local_max",
            low_corr_factors=self.input.lower_threshold_correction_factors,
            high_corr_factors=self.input.upper_threshold_correction_factors,
        )

        self.output.spots_labels_image = schema.ImageAsNumpy(  # TODO: this should be a mask
            data=labels,
            name=f"{self.input.argolight_b_image.name}_spots_labels",
            description=f"Spots labels of {self.input.argolight_b_image.image_url}",
            image_url=self.input.argolight_b_image.image_url,
            source_image_url=self.input.argolight_b_image.image_url,
        )

        spots_properties, spots_positions = compute_spots_properties(
            image=image,
            labels=labels,
            remove_center_cross=self.input.remove_center_cross,
        )

        distances_df = compute_distances_matrix(
            positions=spots_positions,
            max_distance=max_distance,
        )

        properties_kv = []
        properties_ls = []
        distances_kv = []
        spots_centroids = []

        for ch, ch_spot_props in enumerate(spots_properties):
            ch_df = DataFrame()
            ch_properties_kv = {}
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
            ch_properties_kv["channel"] = ch
            ch_properties_kv["nr_of_spots"] = len(ch_df)
            ch_properties_kv["intensity_max_spot"] = ch_df["integrated_intensity"].max().item()
            ch_properties_kv["intensity_max_spot_roi"] = ch_df["integrated_intensity"].argmax().item()
            ch_properties_kv["intensity_min_spot"] = ch_df["integrated_intensity"].min().item()
            ch_properties_kv["intensity_min_spot_roi"] = ch_df["integrated_intensity"].argmin().item()
            ch_properties_kv["mean_intensity"] = ch_df["integrated_intensity"].mean().item()
            ch_properties_kv["median_intensity"] = ch_df["integrated_intensity"].median().item()
            ch_properties_kv["std_mean_intensity"] = ch_df["integrated_intensity"].std().item()
            ch_properties_kv["mad_mean_intensity"] = (
                (ch_df["integrated_intensity"] - ch_df["integrated_intensity"].mean()).abs().mean()
            )
            ch_properties_kv["min_max_intensity_ratio"] = (
                ch_properties_kv["min_intensity"] / ch_properties_kv["max_intensity"]
            )

            properties_ls.append(ch_df)
            properties_kv.append(ch_properties_kv)

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
                schema.Roi(
                    label=f"Centroids_ch{ch:02}",
                    image=self.input.argolight_b_image.image_url,
                    shapes=channel_shapes,
                )
            )
        properties_kv = {k: [i[k] for i in properties_kv] for k in properties_kv[0]}
        properties_df = pd.concat(properties_ls)

        for a, b in product(
            distances_df.channel_a.explode().unique(),
            distances_df.channel_b.explode().unique(),
        ):
            temp_df = distances_df[(distances_df.channel_a == a) & (distances_df.channel_b == b)]
            a = int(a)
            b = int(b)

            pr_distances_kv = {
                "channel_A": a,
                "channel_B": b,
                "mean_3d_dist": temp_df.dist_3d.mean(),
                "median_3d_dist": temp_df.dist_3d.median(),
                "std_3d_dist": temp_df.dist_3d.std(),
                "mad_3d_dist": (temp_df.dist_3d - temp_df.dist_3d.mean()).abs().mean(),
                "mean_z_dist": temp_df.z_dist.mean(),
                "median_z_dist": temp_df.z_dist.median(),
                "std_z_dist": temp_df.z_dist.std(),
                "mad_z_dist": (temp_df.z_dist - temp_df.z_dist.mean()).abs().mean(),
            }

            distances_kv.append(pr_distances_kv)

        distances_kv = {k: [i[k] for i in distances_kv] for k in distances_kv[0]}

        self.output.intensity_measurements = schema.ArgolightBIntensityKeyValues(**properties_kv)

        self.output.distance_measurements = schema.ArgolightBDistanceKeyValues(**distances_kv)

        self.output.spots_properties = schema.TableAsDict(
            name="spots_properties",
            columns=[
                core_schema.Column(name=k, values=v)
                for k, v in properties_df.to_dict(orient="list").items()
            ],
        )

        self.output.spots_distances = schema.TableAsDict(
            name="spots_distances",
            columns=[
                core_schema.Column(name=k, values=v)
                for k, v in distances_df.to_dict(orient="list").items()
            ],
        )

        self.output.spots_centroids = spots_centroids

        self.processing_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.processed = True

        return True


class ArgolightEAnalysis(schema.ArgolightEDataset, AnalysisMixin):
    """This class handles the analysis of the Argolight sample pattern E with lines along the X or Y axis"""

    def run(self) -> bool:
        self.validate_requirements()

        # Check image shape
        pass  # TODO: implement

        # Check image saturation
        pass  # TODO: implement

        # Check for axis value
        pass  # TODO: implement

        image = self.input.argolight_e_image.data
        image = image[0]  # if there is a time dimension, take the first one
        axis = self.input.axis
        measured_band = self.input.measured_band

        (
            profiles,
            z_slices,
            peak_positions,
            peak_heights,
            peak_prominences,
            resolution_values,
            resolution_indexes,
        ) = _compute_resolution(
            image=image,
            axis=axis,
            measured_band=measured_band,
            prominence=self.input.prominence_threshold,
            do_angle_refinement=False,  # TODO: implement angle refinement
        )
        key_values = {
            "channel": [c for c in range(image.shape[-1])],
            "rayleigh_resolution": resolution_values,
            "peak_position_A": [
                peak_positions[ch][ind].item() for ch, ind in enumerate(resolution_indexes)
            ],
            "peak_position_B": [
                peak_positions[ch][ind + 1].item() for ch, ind in enumerate(resolution_indexes)
            ],
            "peak_height_A": [
                peak_heights[ch][ind].item() for ch, ind in enumerate(resolution_indexes)
            ],
            "peak_height_B": [
                peak_heights[ch][ind + 1].item() for ch, ind in enumerate(resolution_indexes)
            ],
            "peak_prominence_A": [
                peak_prominences[ch][ind].item() for ch, ind in enumerate(resolution_indexes)
            ],
            "peak_prominence_B": [
                peak_prominences[ch][ind + 1].item() for ch, ind in enumerate(resolution_indexes)
            ],
            "focus_slice": z_slices,
        }

        out_tables = []
        rois = []

        # Populate tables and rois
        for ch, profile in enumerate(profiles):
            out_tables.append(_profile_to_columns(profile, ch))
            shapes = []
            pos_a, pos_b = (
                key_values["peak_position_A"][ch],
                key_values["peak_position_B"][ch],
            )
            for peak in (pos_a, pos_b):
                # Measurements are taken at center of pixel so we add .5 pixel to peak positions
                if axis == 1:  # Y resolution -> horizontal rois
                    axis_len = image.shape[2]
                    x1_pos = (axis_len / 2) - (axis_len * measured_band / 2)
                    y1_pos = peak + 0.5
                    x2_pos = (axis_len / 2) + (axis_len * measured_band / 2)
                    y2_pos = peak + 0.5
                elif axis == 2:  # X resolution -> vertical rois
                    axis_len = image.shape[1]
                    y1_pos = (axis_len / 2) - (axis_len * measured_band / 2)
                    x1_pos = peak + 0.5
                    y2_pos = (axis_len / 2) + (axis_len * measured_band / 2)
                    x2_pos = peak + 0.5

                shapes.append(
                    core_schema.Line(
                        label=f"ch{ch:02}_resolution_{resolution_values[ch]:.2f}",
                        x1=x1_pos,
                        y1=y1_pos,
                        x2=x2_pos,
                        y2=y2_pos,
                        z=z_slices[ch],
                        c=ch,
                    )
                )
            rois.append(
                core_schema.Roi(
                    label=f"ch{ch:02}_peaks",
                    shapes=shapes,
                    image=self.input.argolight_e_image.image_url,
                )
            )
        self.output.peaks_rois = rois

        self.output.key_measurements = schema.ArgolightEKeyValues(**key_values)

        self.output.intensity_profiles = [
            schema.TableAsDict(name=f"intensity_profiles_ch{c:02}", columns=out_tables[c])
            for c in range(len(out_tables))
        ]

        self.processing_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.processed = True

        return True


def _profile_to_columns(profile: ndarray, channel: int) -> List[Dict[str, Dict[str, List[float]]]]:
    table = [{f"raw_profile_ch{channel:02}": {"values": [v.item() for v in profile[0, :]]}}]

    for p in range(1, profile.shape[0]):
        table.append(
            {
                f"fitted_profile_ch{channel:02}_peak{p:03d}": {
                    "values": [v.item() for v in profile[p, :]]
                }
            }
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
        f=multi_airy_fun,
        xdata=x,
        ydata=profile,
        p0=guess,
        bounds=(lower_bounds, upper_bounds),
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
    prominence_threshold: float,
    measured_band: float,
    do_fitting: bool = True,
    do_angle_refinement: bool = False,
) -> Tuple[ndarray, int64, ndarray, ndarray, ndarray, float64, int]:
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

    peak_positions, properties = find_peaks(
        normalized_profile,
        height=0.3,
        distance=2,
        prominence=prominence_threshold / 4,
    )

    # From the properties we are interested in the amplitude
    # peak_heights = [h for h in properties['peak_heights']]
    ray_filtered_peak_pos = []
    ray_filtered_peak_heights = []
    ray_filtered_peak_prominences = []

    for peak, height, prom in zip(
        peak_positions, properties["peak_heights"], properties["prominences"]
    ):
        if (
            prom / height
        ) > prominence_threshold:  # This is calculating the prominence in relation to the local intensity
            ray_filtered_peak_pos.append(peak)
            ray_filtered_peak_heights.append(height)
            ray_filtered_peak_prominences.append(prom)

    peak_positions = ray_filtered_peak_pos
    peak_heights = ray_filtered_peak_heights
    peak_prominences = ray_filtered_peak_prominences

    if do_fitting:
        peak_positions, peak_heights, fitted_profiles = _fit(normalized_profile, peak_positions)
        normalized_profile = np.append(
            np.expand_dims(normalized_profile, 0), fitted_profiles, axis=0
        )

    # Find the closest peaks to return it as a measure of resolution
    peaks_distances = [abs(a - b) for a, b in zip(peak_positions[0:-2], peak_positions[1:-1])]
    if len(peaks_distances) == 0:
        res = None
        res_index = None
    else:
        res = min(peaks_distances)
        res_index = peaks_distances.index(res)

    return (
        normalized_profile,
        z_focus,
        peak_positions,
        peak_heights,
        peak_prominences,
        res,
        res_index,
    )


def _compute_resolution(
    image: ndarray,
    axis: int,
    measured_band: float,
    prominence: float,
    do_angle_refinement: bool = False,
) -> Tuple[
    List[ndarray],
    List[int],
    List[ndarray],
    List[ndarray],
    List[ndarray],
    List[float],
    List[int],
]:
    profiles = []
    z_planes = []
    peaks_positions = []
    peaks_heights = []
    peaks_prominences = []
    resolution_values = []
    resolution_indexes = []

    for c in range(image.shape[-1]):
        (
            prof,
            zp,
            pk_pos,
            pk_heights,
            pk_prominences,
            res,
            res_index,
        ) = _compute_channel_resolution(
            channel=image[..., c],
            axis=axis,
            prominence_threshold=prominence,
            measured_band=measured_band,
            do_angle_refinement=do_angle_refinement,
        )
        profiles.append(prof)
        z_planes.append(zp.item())
        peaks_positions.append(pk_pos)
        peaks_heights.append(pk_heights)
        peaks_prominences.append(pk_prominences)
        resolution_values.append(res.item())
        resolution_indexes.append(res_index)

    return (
        profiles,
        z_planes,
        peaks_positions,
        peaks_heights,
        peaks_prominences,
        resolution_values,
        resolution_indexes,
    )
