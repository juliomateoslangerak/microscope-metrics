from typing import Any, Dict, Tuple

import microscopemetrics_schema.datamodel as mm_schema
import numpy as np
import pandas as pd
from pandas import DataFrame
from pydantic.color import Color
from scipy.optimize import curve_fit, fsolve
from skimage.feature import peak_local_max
from skimage.filters import gaussian

from microscopemetrics import FittingError, SaturationError
from microscopemetrics.samples import (
    AnalysisMixin,
    dict_to_table_inlined,
    logger,
    numpy_to_image_byref,
)
from microscopemetrics.utilities.utilities import airy_fun, gaussian_fun, is_saturated


def _fit_gaussian(profile, guess=None):
    if guess is None:
        guess = [profile.min(), profile.max(), profile.argmax(), 0.8]
    x = np.linspace(0, profile.shape[0], profile.shape[0], endpoint=False)
    popt, pcov = curve_fit(gaussian_fun, x, profile, guess)

    fitted_profile = gaussian_fun(x, popt[0], popt[1], popt[2], popt[3])
    fwhm = popt[3] * 2.35482

    return fitted_profile, fwhm


def _fit_airy(profile, guess=None):
    if guess is None:
        guess = [profile.argmax(), 4 * profile.max()]
    x = np.linspace(0, profile.shape[0], profile.shape[0], endpoint=False)
    popt, pcov = curve_fit(f=airy_fun, xdata=x, ydata=profile, p0=guess)

    fitted_profile = airy_fun(x, popt[0], popt[1])

    def _f(d):
        return airy_fun(d, popt[0], popt[1]) - (fitted_profile.max() - fitted_profile.min()) / 2

    guess = np.array([fitted_profile.argmax() - 1, fitted_profile.argmax() + 1])
    v = fsolve(_f, guess)
    fwhm = abs(v[1] - v[0])

    # Calculate the fit quality
    residuals = profile - fitted_profile
    rss = np.sum(residuals**2)

    return fitted_profile, rss, fwhm


def _calculate_bead_intensity_outliers(
    bead_crops: Dict, zscore_threshold: float
) -> Tuple[Dict, Dict]:
    bead_max_intensities = []
    bead_zscores = {}
    bead_considered_intensity_outlier = {}
    for _, im_bead_crops in bead_crops.items():
        for ch_bead_crops in im_bead_crops:
            for bead in ch_bead_crops:
                bead_max_intensities.append(bead.max())

    mean = np.mean(bead_max_intensities)
    std = np.std(bead_max_intensities)

    for label, im_bead_crops in bead_crops.items():
        bead_considered_intensity_outlier[label] = []
        for ch_bead_crops in im_bead_crops:
            ch_is_outlier = []
            ch_zscores = []
            for bead in ch_bead_crops:
                zscore = abs(bead.max() - mean) / std
                ch_zscores.append(zscore)
                if zscore > zscore_threshold:
                    ch_is_outlier.append(True)
                else:
                    ch_is_outlier.append(False)
            bead_considered_intensity_outlier[label].append(ch_is_outlier)

    return bead_zscores, bead_considered_intensity_outlier


def _process_bead(bead: np.ndarray, voxel_size_micron: Tuple[float, float, float]):
    # Find the strongest sections to generate profiles
    # TODO: We should use the center of the bead image for x and y, for the z we should do the fit first
    z_max = np.max(bead, axis=(1, 2))
    z_focus = np.argmax(z_max)
    y_max = np.max(bead, axis=(0, 2))
    y_focus = np.argmax(y_max)
    x_max = np.max(bead, axis=(0, 1))
    x_focus = np.argmax(x_max)

    # Generate profiles
    z_profile = np.squeeze(bead[:, y_focus, x_focus])
    y_profile = np.squeeze(bead[z_focus, :, x_focus])
    x_profile = np.squeeze(bead[z_focus, y_focus, :])

    # Fitting the profiles
    z_fitted_profile, z_rss, z_fwhm = _fit_airy(z_profile)
    y_fitted_profile, y_rss, y_fwhm = _fit_airy(y_profile)
    x_fitted_profile, x_rss, x_fwhm = _fit_airy(x_profile)

    if all(voxel_size_micron):
        z_fwhm_micron = z_fwhm * voxel_size_micron[0]
        y_fwhm_micron = y_fwhm * voxel_size_micron[1]
        x_fwhm_micron = x_fwhm * voxel_size_micron[2]
    else:
        z_fwhm_micron = None
        y_fwhm_micron = None
        x_fwhm_micron = None

    # TODO: Implement the discarding of beads that are too close to the edge in Z
    considered_axial_edge = False

    return (
        (z_profile, y_profile, x_profile),
        (z_fitted_profile, y_fitted_profile, x_fitted_profile),
        (z_rss, y_rss, x_rss),
        (z_fwhm, y_fwhm, x_fwhm),
        (z_fwhm_micron, y_fwhm_micron, x_fwhm_micron),
        considered_axial_edge,
    )


def _find_beads(channel: np.ndarray, sigma: Tuple[float, float, float], min_distance: float):
    logger.debug(f"Finding beads in channel of shape {channel.shape}")

    if all(sigma):
        logger.debug(f"Applying Gaussian filter with sigma {sigma}")
        image_mip = gaussian(image=channel, sigma=sigma, preserve_range=True)
    else:
        logger.debug("No Gaussian filter applied")

    # Find bead centers
    positions_all = peak_local_max(image=channel, threshold_rel=0.2)

    # Find beads min distance filtered
    # We need to remove the beads that are close to each other before the
    # ones that are close to the edge in order to avoid keeping beads that
    # are close to each other but far from the edge. If an edge bead is
    # removed, the other bead that was close to it will be kept.
    positions_proximity_filtered = peak_local_max(
        image=channel, threshold_rel=0.2, min_distance=min_distance
    )

    # find beads edge filtered
    positions_edge_filtered = positions_all[
        (positions_proximity_filtered[:, 2] > min_distance // 2)
        & (positions_proximity_filtered[:, 2] < channel.shape[2] - min_distance // 2)
        & (positions_proximity_filtered[:, 1] > min_distance // 2)
        & (positions_proximity_filtered[:, 1] < channel.shape[1] - min_distance // 2)
    ]

    # Convert arrays to sets for easier comparison
    positions_all_set = set(map(tuple, positions_all))
    positions_proximity_filtered_set = set(map(tuple, positions_proximity_filtered))
    positions_edge_filtered_set = set(map(tuple, positions_edge_filtered))

    valid_positions_set = positions_proximity_filtered_set & positions_edge_filtered_set
    discarded_positions_proximity_set = positions_all_set - positions_proximity_filtered_set
    discarded_positions_edge_set = positions_all_set - positions_edge_filtered_set
    discarded_positions_set = discarded_positions_proximity_set | discarded_positions_edge_set

    logger.debug(f"Beads found: {len(positions_all)}")
    logger.debug(f"Beads kept for analysis: {len(valid_positions_set)}")
    logger.debug(f"Beads discarded: {len(discarded_positions_set)}")
    logger.debug(
        f"Beads discarded for being to close to the edge: {len(discarded_positions_edge_set)}"
    )
    logger.debug(
        f"Beads discarded for being to close to each other: {len(discarded_positions_proximity_set)}"
    )

    # Convert back to numpy arrays
    valid_positions = np.array(list(valid_positions_set))
    discarded_positions_proximity = np.array(list(discarded_positions_proximity_set))
    discarded_positions_edge = np.array(list(discarded_positions_edge_set))

    bead_images = [
        channel[
            :,
            (pos[1] - (min_distance // 2)) : (pos[1] + (min_distance // 2)),
            (pos[2] - (min_distance // 2)) : (pos[2] + (min_distance // 2)),
        ]
        for pos in valid_positions
    ]
    return (
        bead_images,
        valid_positions,
        discarded_positions_proximity,
        discarded_positions_edge,
    )


def _process_channel(
    channel: np.ndarray,
    sigma: Tuple[float, float, float],
    min_bead_distance: float,
    snr_threshold: float,
    fitting_rss_threshold: float,
    voxel_size_micron: Tuple[float, float, float],
) -> Tuple:
    (
        beads,
        bead_positions,
        discarded_self_proximity_positions,
        discarded_lateral_edge_positions,
    ) = _find_beads(
        channel=channel,
        sigma=sigma,
        min_distance=min_bead_distance,
    )

    bead_profiles = []
    bead_fitted_profiles = []
    bead_rsss = []
    bead_fwhms = []
    bead_fwhms_micron = []
    considered_axial_edge = []

    for bead, pos in zip(beads, bead_positions):
        try:
            bpr, fpr, rss, fwhm, fwhm_micron, ax_edge = _process_bead(
                bead=bead, voxel_size_micron=voxel_size_micron
            )
            bead_profiles.append(bpr)
            bead_fitted_profiles.append(fpr)
            bead_rsss.append(rss)
            bead_fwhms.append(fwhm)
            bead_fwhms_micron.append(fwhm_micron)
            considered_axial_edge.append(ax_edge)
        except FittingError as e:
            logger.error(f"Could not fit bead at position: {pos}: {e}")
            raise e

    return (
        beads,
        bead_positions,
        bead_profiles,
        bead_fitted_profiles,
        bead_rsss,
        bead_fwhms,
        bead_fwhms_micron,
        discarded_self_proximity_positions,
        discarded_lateral_edge_positions,
        considered_axial_edge,
    )


def _process_image(
    image: np.ndarray,
    sigma: Tuple[float, float, float],
    min_bead_distance: float,
    snr_threshold: float,
    fitting_rss_threshold: float,
    voxel_size_micron: Tuple[float, float, float],
) -> Dict[str, Any]:
    # Some images (e.g. OMX-3D-SIM) may contain negative values.
    image = np.clip(image, a_min=0, a_max=None)

    nr_channels = image.shape[-1]

    bead_images = []
    bead_positions = []
    bead_profiles = []
    bead_fitted_profiles = []
    bead_rsss = []
    bead_fwhms = []
    bead_fwhms_micron = []
    discarded_positions_self_proximity = []
    discarded_positions_lateral_edge = []
    bead_considered_axial_edge = []

    for ch in range(nr_channels):
        (
            ch_bead_images,
            ch_bead_positions,
            ch_bead_profiles,
            ch_bead_fitted_profiles,
            ch_bead_rsss,
            ch_bead_fwhms,
            ch_bead_fwhms_micron,
            ch_disc_prox_positions,
            ch_disc_lat_edge_positions,
            ch_disc_ax_edge_positions,
        ) = _process_channel(
            channel=image[..., ch],
            sigma=sigma,
            min_bead_distance=min_bead_distance,
            snr_threshold=snr_threshold,
            fitting_rss_threshold=fitting_rss_threshold,
            voxel_size_micron=voxel_size_micron,
        )

        bead_images.append(ch_bead_images)
        bead_positions.append(ch_bead_positions)
        bead_profiles.append(ch_bead_profiles)
        bead_fitted_profiles.append(ch_bead_fitted_profiles)
        bead_rsss.append(ch_bead_rsss)
        bead_fwhms.append(ch_bead_fwhms)
        bead_fwhms_micron.append(ch_bead_fwhms_micron)
        discarded_positions_self_proximity.append(ch_disc_prox_positions)
        discarded_positions_lateral_edge.append(ch_disc_lat_edge_positions)
        bead_considered_axial_edge.append(ch_disc_ax_edge_positions)

    return {
        "bead_images": bead_images,
        "bead_positions": bead_positions,
        "bead_profiles": bead_profiles,
        "bead_fitted_profiles": bead_fitted_profiles,
        "bead_rsss": bead_rsss,
        "bead_fwhms": bead_fwhms,
        "bead_fwhms_micron": bead_fwhms_micron,
        "discarded_positions_self_proximity": discarded_positions_self_proximity,
        "discarded_positions_lateral_edge": discarded_positions_lateral_edge,
        "bead_considered_axial_edge": bead_considered_axial_edge,
    }


class PSFBeadsAnalysis(mm_schema.PSFBeadsDataset, AnalysisMixin):
    """Analysis of PSF beads images to extract resolution information."""

    def _estimate_min_bead_distance(self):
        # TODO: get the resolution somewhere or pass it as a metadata
        return 3 * self.input.min_lateral_distance_factor

    def _generate_centroids_roi(
        self, positions, root_name, color, stroke_width, positions_filter=None
    ):
        rois = {}
        for image_label, input_image in self.input.psf_beads_images.items():
            for ch in range(input_image.data.shape[-1]):
                shapes = {}
                if positions_filter is None:
                    for i, pos in enumerate(positions[image_label][ch]):
                        shapes[f"{i:02d}"] = mm_schema.Point(
                            z=pos[0],
                            y=pos[1],
                            x=pos[2],
                            c=ch,
                            stroke_color=color,
                            stroke_width=stroke_width,
                        )
                    label = f"{root_name}_{image_label}_ch_{ch:02d}"
                    rois[label] = mm_schema.RoiMassCenters(
                        label=label,
                        description=f"{root_name} channel {ch} in image {image_label}",
                        image=image_label,
                        shapes=shapes,
                    )
                else:
                    for i, (pos, is_filtered) in enumerate(
                        zip(positions[image_label][ch], positions_filter[image_label][ch])
                    ):
                        if is_filtered:
                            shapes[f"{i:02d}"] = mm_schema.Point(
                                z=pos[0],
                                y=pos[1],
                                x=pos[2],
                                c=ch,
                                stroke_color=color,
                                stroke_width=stroke_width,
                            )
                    label = f"{root_name}_{image_label}_ch_{ch:02d}"
                    rois[label] = mm_schema.RoiMassCenters(
                        label=label,
                        description=f"{root_name} channel {ch} in image {image_label}",
                        image=image_label,
                        shapes=shapes,
                    )

        return rois

    # def _generate_key_values(self, bead_properties_df):
    #     key_values = {
    #         "nr_of_beads_analyzed": len(bead_properties_df),
    #         "nr_of_beads_discarded_lateral_edge": len(
    #             bead_properties_df[bead_properties_df["considered_axial_edge"] == True]
    #         ),
    #         "nr_of_beads_discarded_axial_edge": len(
    #             bead_properties_df[bead_properties_df["considered_axial_edge"] == True]
    #         ),
    #         "nr_of_beads_discarded_self_proximity
    #         "nr_of_beads_discarded_cluster
    #         "nr_of_beads_discarded_fit_quality
    #         "fit_quality_z_mean
    #         "fit_quality_z_median
    #         "fit_quality_z_stdev
    #         "fit_quality_y_mean
    #         "fit_quality_y_median
    #         "fit_quality_y_stdev
    #         "fit_quality_x_mean
    #         "fit_quality_x_median
    #         "fit_quality_x_stdev
    #         "resolution_mean_fwhm_z_pixels
    #         "resolution_median_fwhm_z_pixels
    #         "resolution_stdev_fwhm_z_pixels
    #         "resolution_mean_fwhm_y_pixels
    #         "resolution_median_fwhm_y_pixels
    #         "resolution_stdev_fwhm_y_pixels
    #         "resolution_mean_fwhm_x_pixels
    #         "resolution_median_fwhm_x_pixels
    #         "resolution_stdev_fwhm_x_pixels
    #         "resolution_mean_fwhm_z_microns
    #         "resolution_median_fwhm_z_microns
    #         "resolution_stdev_fwhm_z_microns
    #         "resolution_mean_fwhm_y_microns
    #         "resolution_median_fwhm_y_microns
    #         "resolution_stdev_fwhm_y_microns
    #         "resolution_mean_fwhm_x_microns
    #         "resolution_median_fwhm_x_microns
    #         "resolution_stdev_fwhm_x_microns
    #         "resolution_mean_fwhm_lateral_asymmetry_ratio
    #         "resolution_median_fwhm_lateral_asymmetry_ratio
    #         "resolution_stdev_fwhm_lateral_asymmetry_ratio

    def run(self) -> bool:
        self.validate_requirements()
        # TODO: Implement Nyquist validation??

        # Containers for input data and input parameters
        images = {}
        voxel_sizes_micron = {}
        min_bead_distance = self._estimate_min_bead_distance()
        intensity_zscore_threshold = self.input.intensity_zscore_threshold
        snr_threshold = self.input.snr_threshold
        fitting_rss_threshold = self.input.fitting_rss_threshold

        # Containers for output data
        saturated_channels = {}
        bead_crops = {}
        bead_positions = {}
        bead_profiles = {}
        bead_fitted_profiles = {}
        bead_rsss = {}
        bead_fwhms = {}
        bead_fwhms_micron = {}
        discarded_positions_self_proximity = {}
        discarded_positions_lateral_edge = {}
        bead_considered_axial_edge = {}

        # Prepare data
        for label, image in self.input.psf_beads_images.items():
            images[label] = image.data[0, ...]

            voxel_sizes_micron[label] = (image.voxel_size_z, image.voxel_size_y, image.voxel_size_x)
            saturated_channels[label] = []

            # Check image shape
            logger.info(f"Checking image {label} shape...")
            if len(image.data.shape) != 5:
                logger.error(f"Image {label} must be 5D")
                return False
            if image.data.shape[0] != 1:
                logger.warning(
                    f"Image {label} must be in TZYXC order and single time-point. Using first time-point."
                )

            # Check image saturation
            logger.info(f"Checking image {label} saturation...")
            for c in range(image.data.shape[-1]):
                if is_saturated(
                    channel=image.data[..., c],
                    threshold=self.input.saturation_threshold,
                    detector_bit_depth=self.input.bit_depth,
                ):
                    logger.error(f"Image {label}: channel {c} is saturated")
                    saturated_channels[label].append(c)

        if any(len(saturated_channels[name]) for name in saturated_channels):
            logger.error(f"Channels {saturated_channels} are saturated")
            raise SaturationError(f"Channels {saturated_channels} are saturated")

        # Main image loop
        for image_label, image in images.items():
            logger.info(f"Processing image {image_label}...")
            image_output = _process_image(
                image=image,
                sigma=(self.input.sigma_z, self.input.sigma_y, self.input.sigma_x),
                min_bead_distance=min_bead_distance,
                snr_threshold=snr_threshold,
                fitting_rss_threshold=fitting_rss_threshold,
                voxel_size_micron=voxel_sizes_micron[image_label],
            )
            logger.info(
                f"Image {image_label} processed:"
                f"    {len(image_output['bead_positions'])} beads found"
                f"    {len(image_output['discarded_positions_self_proximity'])} beads discarded for being to close to each other"
                f"    {len(image_output['discarded_positions_lateral_edge'])} beads discarded for being to close to the edge"
                f"    {len(image_output['discarded_positions_axial_edge'])} beads considered as to close to the top or bottom of the image"
            )

            bead_crops[image_label] = image_output["bead_images"]
            bead_positions[image_label] = image_output["bead_positions"]
            bead_profiles[image_label] = image_output["bead_profiles"]
            bead_fitted_profiles[image_label] = image_output["bead_fitted_profiles"]
            bead_rsss[image_label] = image_output["bead_rsss"]
            bead_fwhms[image_label] = image_output["bead_fwhms"]
            bead_fwhms_micron[image_label] = image_output["bead_fwhms_micron"]
            discarded_positions_self_proximity[image_label] = image_output[
                "discarded_positions_self_proximity"
            ]
            discarded_positions_lateral_edge[image_label] = image_output[
                "discarded_positions_lateral_edge"
            ]
            bead_considered_axial_edge[image_label] = image_output["bead_considered_axial_edge"]

        # Validate bead intensity
        bead_zscores, bead_considered_intensity_outlier = _calculate_bead_intensity_outliers(
            bead_crops=bead_crops, zscore_threshold=intensity_zscore_threshold
        )

        ## Populate output
        output_bead_crops = {}
        bead_properties = {
            "image_label": [],
            "image_name": [],
            "channel_nr": [],
            "bead_nr": [],
            "intensity_max": [],
            "min_intensity_min": [],
            "intensity_std": [],
            "intensity_zscore": [],
            "considered_intensity_outlier": [],
            "z_centroid": [],
            "y_centroid": [],
            "x_centroid": [],
            "z_fit_rss": [],
            "y_fit_rss": [],
            "x_fit_rss": [],
            "considered_bad_z_fit": [],
            "considered_bad_y_fit": [],
            "considered_bad_x_fit": [],
            "z_fwhm": [],
            "y_fwhm": [],
            "x_fwhm": [],
            "fwhm_lateral_asymmetry_ratio": [],
            "z_fwhm_micron": [],
            "y_fwhm_micron": [],
            "x_fwhm_micron": [],
            "considered_axial_edge": [],
        }

        for image_label, input_image in self.input.psf_beads_images.items():
            ## Image linked information
            for ch in range(input_image.data.shape[-1]):
                ## Channel linked information
                # Bead crops
                for i, bead in enumerate(bead_crops[image_label][ch]):
                    output_bead_crops[
                        f"{input_image.name}_ch_{ch:02d}_bead_{i:02d}"
                    ] = numpy_to_image_byref(
                        array=bead,
                        name=f"{input_image.name}_ch_{ch:02d}_bead_{i:02d}",
                        description=f"Bead crop for bead nr {i}, on channel {ch}, image {image_label}",
                        source_image_url=self.input.psf_beads_images[image_label].image_url,
                    )

                    # Append data to beads table
                    bead_properties["image_label"] = image_label
                    bead_properties["image_name"] = input_image.name
                    bead_properties["channel_nr"] = ch
                    bead_properties["bead_nr"] = i
                    bead_properties["intensity_max"] = bead.max()
                    bead_properties["min_intensity_min"] = bead.min()
                    bead_properties["intensity_std"] = bead.std()
                    bead_properties["intensity_zscore"] = bead_zscores[image_label][ch][i]
                    bead_properties[
                        "considered_intensity_outlier"
                    ] = bead_considered_intensity_outlier[image_label][ch][i]
                    bead_properties["z_centroid"] = bead_positions[image_label][ch][i][0]
                    bead_properties["y_centroid"] = bead_positions[image_label][ch][i][1]
                    bead_properties["x_centroid"] = bead_positions[image_label][ch][i][2]
                    bead_properties["z_fit_rss"] = bead_rsss[image_label][ch][i]
                    bead_properties["y_fit_rss"] = bead_rsss[image_label][ch][i]
                    bead_properties["x_fit_rss"] = bead_rsss[image_label][ch][i]
                    bead_properties["considered_bad_z_fit"] = (
                        bead_rsss[image_label][ch][i][0] > fitting_rss_threshold
                    )
                    bead_properties["considered_bad_y_fit"] = (
                        bead_rsss[image_label][ch][i][1] > fitting_rss_threshold
                    )
                    bead_properties["considered_bad_x_fit"] = (
                        bead_rsss[image_label][ch][i][2] > fitting_rss_threshold
                    )
                    bead_properties["z_fwhm"] = bead_fwhms[image_label][ch][i][0]
                    bead_properties["y_fwhm"] = bead_fwhms[image_label][ch][i][1]
                    bead_properties["x_fwhm"] = bead_fwhms[image_label][ch][i][2]
                    bead_properties["fwhm_lateral_asymmetry_ratio"] = max(
                        bead_fwhms[image_label][ch][i][1], bead_fwhms[image_label][ch][i][2]
                    ) / min(bead_fwhms[image_label][ch][i][1], bead_fwhms[image_label][ch][i][2])
                    bead_properties["z_fwhm_micron"] = (bead_fwhms_micron[image_label][ch][i][0],)
                    bead_properties["y_fwhm_micron"] = (bead_fwhms_micron[image_label][ch][i][1],)
                    bead_properties["x_fwhm_micron"] = (bead_fwhms_micron[image_label][ch][i][2],)
                    bead_properties["considered_axial_edge"] = (
                        bead_considered_axial_edge[image_label][ch][i],
                    )

        self.output.bead_properties = dict_to_table_inlined(bead_properties)

        bead_properties_df = pd.DataFrame(bead_properties)

        self.output.analyzed_bead_crops = output_bead_crops

        self.output.analyzed_bead_centroids = self._generate_centroids_roi(
            positions=bead_positions,
            root_name="analyzed_bead_centroids",
            color=Color((0, 255, 0, 100)),
            stroke_width=8,
        )

        self.output.discarded_bead_centroids_lateral_edge = self._generate_centroids_roi(
            positions=discarded_positions_lateral_edge,
            root_name="discarded_bead_centroids_lateral_edge",
            color=Color((255, 0, 0, 100)),
            stroke_width=4,
        )

        self.output.discarded_bead_centroids_self_proximity = self._generate_centroids_roi(
            positions=discarded_positions_self_proximity,
            root_name="discarded_bead_centroids_self_proximity",
            color=Color((255, 0, 0, 100)),
            stroke_width=4,
        )

        self.output.considered_bead_centroids_axial_edge = self._generate_centroids_roi(
            positions=bead_positions,
            root_name="considered_bead_centroids_axial_edge",
            color=Color((0, 0, 255, 100)),
            stroke_width=4,
            positions_filter=bead_considered_axial_edge,
        )

        self.output.considered_bead_centroids_intensity_outlier = self._generate_centroids_roi(
            positions=bead_positions,
            root_name="considered_bead_centroids_intensity_outlier",
            color=Color((0, 0, 255, 100)),
            stroke_width=4,
            positions_filter=bead_considered_intensity_outlier,
        )

        """
      discarded_bead_centroids_fit_quality:
        range: RoiMassCenters
        description: >-
          The centroids of the beads detected but discarded as the fit quality was not good enough.
          One point will be provided per bead.
          One ROI per channel.
        multivalued: true
        inlined: true
      key_values:
        range: PSFBeadsKeyMeasurements
        description: >-
          The key measurements of the PSF beads analysis.
        multivalued: False
        inlined: true
      bead_properties:
        range: TableAsDict
        description: >-
          Properties associated with the analysis of the beads. This properties include:
          dataset_id
          image_id
          roi_id
          channel_nr
          fit_parameters
          fit_quality_z
          fit_quality_y
          fit_quality_x
          resolution_fwhm_z_pixels
          resolution_fwhm_y_pixels
          resolution_fwhm_x_pixels
          resolution_fwhm_z_microns
          resolution_fwhm_y_microns
          resolution_fwhm_x_microns
          resolution_lateral_asymmetry_ratio
        multivalued: false
        inlined: true
      bead_z_profiles:
        range: TableAsDict
        description: >-
          The intensity profiles along the z axis of the analyzed beads as well as the fits.
        multivalued: false
        inlined: true
      bead_y_profiles:
        range: TableAsDict
        description: >-
          The intensity profiles along the y axis of the analyzed beads as well as the fits.
        multivalued: false
        inlined: true
      bead_x_profiles:
        """


"""
                bead_images[image_label].append(beads)
                valid_positions[image_label].append(val_pos)
                discarded_positions_self_proximity[image_label].append(disc_prox_pos)
                discarded_positions_lateral_edge[image_label].append(disc_edge_pos)

                # Generate profiles and measure FWHM
                raw_profiles = []
                fitted_profiles = []
                fwhm_values = []
                for bead in bead_images:
                    opr, fpr, fwhm = self._analyze_bead(bead)
                    raw_profiles.append(opr)
                    fitted_profiles.append(fpr)
                    fwhm = tuple(f * ps for f, ps in zip(fwhm, pixel_size))
                    fwhm_values.append(fwhm)

                properties_df = DataFrame()
                properties_df["bead_nr"] = range(len(bead_images))
                properties_df["max_intensity"] = [e.max() for e in bead_images]
                properties_df["min_intensity"] = [e.min() for e in bead_images]
                properties_df["z_centroid"] = [e[0] for e in positions]
                properties_df["y_centroid"] = [e[1] for e in positions]
                properties_df["x_centroid"] = [e[2] for e in positions]
                properties_df["centroid_units"] = "PIXEL"
                properties_df["z_fwhm"] = [e[0] for e in fwhm_values]
                properties_df["y_fwhm"] = [e[1] for e in fwhm_values]
                properties_df["x_fwhm"] = [e[2] for e in fwhm_values]
                properties_df["fwhm_units"] = pixel_size_units

                profiles_z_df = DataFrame()
                profiles_y_df = DataFrame()
                profiles_x_df = DataFrame()

                for i, (raw_profile, fitted_profile) in enumerate(zip(raw_profiles, fitted_profiles)):
                    profiles_z_df[f"raw_z_profile_bead_{i:02d}"] = raw_profile[0]
                    profiles_z_df[f"fitted_z_profile_bead_{i:02d}"] = fitted_profile[0]
                    profiles_y_df[f"raw_y_profile_bead_{i:02d}"] = raw_profile[1]
                    profiles_y_df[f"fitted_y_profile_bead_{i:02d}"] = fitted_profile[1]
                    profiles_x_df[f"raw_x_profile_bead_{i:02d}"] = raw_profile[2]
                    profiles_x_df[f"fitted_x_profile_bead_{i:02d}"] = fitted_profile[2]

                    psf_properties
                    psf_z_profiles
                    psf_y_profiles
                    psf_x_profiles

        for i, bead in enumerate(beads):
            self.output.append(
                model.Image(
                    name=f"bead_nr{i:02d}",
                    description=f"PSF bead crop for bead nr {i}",
                    data=np.expand_dims(bead, axis=(1, 2)),
                )
            )

        for i, position in enumerate(positions):
            self.output.append(
                model.Roi(
                    name=f"bead_nr{i:02d}_centroid",
                    description=f"Weighted centroid of bead nr {i}",
                    shapes=[
                        model.Point(
                            z=position[0].item(),
                            y=position[1].item(),
                            x=position[2].item(),
                            stroke_color=Color((0, 255, 0, 0.0)),
                            fill_color=Color((50, 255, 50, 0.1)),
                        )
                    ],
                )
            )

        edge_points = [
            model.Point(
                z=pos[0].item(),
                y=pos[1].item(),
                x=pos[2].item(),
                stroke_color=Color((255, 0, 0, 0.6)),
                fill_color=Color((255, 50, 50, 0.1)),
            )
            for pos in disc_edge_pos
        ]
        self.output.append(
            model.Roi(
                name="Discarded_edge",
                description="Beads discarded for being to close to the edge of the image",
                shapes=edge_points,
            )
        )

        proximity_points = [
            model.Point(
                z=pos[0].item(),
                y=pos[1].item(),
                x=pos[2].item(),
                stroke_color=Color((255, 0, 0, 0.6)),
                fill_color=Color((255, 50, 50, 0.1)),
            )
            for pos in disc_prox_pos
        ]
        self.output.append(
            model.Roi(
                name="Discarded_proximity",
                description="Beads discarded for being to close to each other",
                shapes=proximity_points,
            )
        )

        intensity_points = [
            model.Point(
                z=pos[0].item(),
                y=pos[1].item(),
                x=pos[2].item(),
                stroke_color=Color((255, 0, 0, 0.6)),
                fill_color=Color((255, 50, 50, 0.1)),
            )
            for pos in positions_intensity_discarded
        ]
        self.output.append(
            model.Roi(
                name="Discarded_intensity",
                description="Beads discarded for being to intense or to weak. "
                "Suspected not being single beads",
                shapes=intensity_points,
            )
        )


        self.output.append(
            model.Table(
                name="Analysis_PSF_properties",
                description="Properties associated with the analysis",
                table=properties_df,
            )
        )


        self.output.append(
            model.Table(
                name="Analysis_PSF_Z_profiles",
                description="Raw and fitted profiles along Z axis of beads",
                table=profiles_z_df,
            )
        )

        self.output.append(
            model.Table(
                name="Analysis_PSF_Y_profiles",
                description="Raw and fitted profiles along Y axis of beads",
                table=profiles_y_df,
            )
        )

        self.output.append(
            model.Table(
                name="Analysis_PSF_X_profiles",
                description="Raw and fitted profiles along X axis of beads",
                table=profiles_x_df,
            )
        )

        key_values = {"nr_of_beads_analyzed": positions.shape[0]}

        if key_values["nr_of_beads_analyzed"] == 0:
            key_values["resolution_mean_fwhm_z"] = "None"
            key_values["resolution_mean_fwhm_y"] = "None"
            key_values["resolution_mean_fwhm_x"] = "None"
            key_values["resolution_mean_fwhm_units"] = "None"
        else:
            key_values["resolution_mean_fwhm_z"] = properties_df["z_fwhm"].mean()
            key_values["resolution_median_fwhm_z"] = properties_df["z_fwhm"].median()
            key_values["resolution_stdev_fwhm_z"] = properties_df["z_fwhm"].std()
            key_values["resolution_mean_fwhm_y"] = properties_df["y_fwhm"].mean()
            key_values["resolution_median_fwhm_y"] = properties_df["y_fwhm"].median()
            key_values["resolution_stdev_fwhm_y"] = properties_df["y_fwhm"].std()
            key_values["resolution_mean_fwhm_x"] = properties_df["x_fwhm"].mean()
            key_values["resolution_median_fwhm_x"] = properties_df["x_fwhm"].median()
            key_values["resolution_stdev_fwhm_x"] = properties_df["x_fwhm"].std()
        key_values["resolution_theoretical_fwhm_lateral"] = self.get_metadata_values(
            "theoretical_fwhm_lateral_res"
        )
        key_values["resolution_theoretical_fwhm_lateral_units"] = self.get_metadata_units(
            "theoretical_fwhm_lateral_res"
        )
        key_values["resolution_theoretical_fwhm_axial"] = self.get_metadata_values(
            "theoretical_fwhm_axial_res"
        )
        key_values["resolution_theoretical_fwhm_axial_units"] = self.get_metadata_units(
            "theoretical_fwhm_axial_res"
        )

        self.output.append(
            model.KeyValues(
                name="Measurements_results",
                description="Output measurements",
                key_values=key_values,
            )
        )

        return True


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
"""
