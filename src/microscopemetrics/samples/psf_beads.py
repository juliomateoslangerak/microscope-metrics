from typing import Any, Dict, Tuple

import microscopemetrics_schema.datamodel as mm_schema
import numpy as np
import pandas as pd
from pandas import DataFrame
from skimage.feature import peak_local_max
from skimage.filters import gaussian

from microscopemetrics import FittingError, SaturationError
from microscopemetrics.samples import (
    AnalysisMixin,
    dict_to_table_inlined,
    logger,
    numpy_to_image_byref,
)
from microscopemetrics.utilities.utilities import fit_airy, is_saturated


def _calculate_bead_intensity_outliers(
    bead_crops: Dict, zscore_threshold: float
) -> Tuple[Dict, Dict]:
    bead_zscores = {}
    bead_considered_intensity_outlier = {}

    bead_max_intensities = [
        bead.max()
        for im_bead_crops in bead_crops.values()
        for ch_bead_crops in im_bead_crops
        for bead in ch_bead_crops
    ]

    mean = np.mean(bead_max_intensities)
    std = np.std(bead_max_intensities)

    for label, im_bead_crops in bead_crops.items():
        bead_zscores[label] = []
        bead_considered_intensity_outlier[label] = []
        for ch_bead_crops in im_bead_crops:
            ch_zscores = []
            ch_is_outlier = []
            for bead in ch_bead_crops:
                if len(bead_max_intensities) == 1:
                    ch_zscores.append(0)
                    ch_is_outlier.append(False)
                elif 1 < len(bead_max_intensities) < 6:
                    ch_zscores.append(abs(bead.max() - mean) / std)
                    ch_is_outlier.append(False)
                else:
                    ch_zscores.append(abs(bead.max() - mean) / std)
                    if ch_zscores[-1] > zscore_threshold:
                        ch_is_outlier.append(True)
                    else:
                        ch_is_outlier.append(False)
            bead_zscores[label].append(ch_zscores)
            bead_considered_intensity_outlier[label].append(ch_is_outlier)

    return bead_zscores, bead_considered_intensity_outlier


def _generate_key_values(
    bead_properties_df, discarded_positions_self_proximity, discarded_positions_lateral_edge
):
    return {
        "channel_nr": bead_properties_df.groupby("channel_nr")["channel_nr"].first().tolist(),
        "nr_of_beads_analyzed": bead_properties_df.groupby("channel_nr").size().tolist(),
        "nr_of_beads_discarded_lateral_edge": [
            sum(len(pos) for pos in ch) for ch in zip(*discarded_positions_lateral_edge.values())
        ],
        "nr_of_beads_discarded_self_proximity": [
            sum(len(pos) for pos in ch) for ch in zip(*discarded_positions_self_proximity.values())
        ],
        "nr_of_beads_considered_axial_edge": bead_properties_df.groupby("channel_nr")[
            "considered_axial_edge"
        ]
        .apply(lambda x: (x == True).sum())
        .tolist(),
        "nr_of_beads_considered_intensity_outlier": bead_properties_df.groupby("channel_nr")[
            "considered_intensity_outlier"
        ]
        .apply(lambda x: (x == True).sum())
        .tolist(),
        "nr_of_beads_considered_bad_z_fit": bead_properties_df.groupby("channel_nr")[
            "considered_bad_z_fit"
        ]
        .apply(lambda x: (x == True).sum())
        .tolist(),
        "nr_of_beads_considered_bad_y_fit": bead_properties_df.groupby("channel_nr")[
            "considered_bad_y_fit"
        ]
        .apply(lambda x: (x == True).sum())
        .tolist(),
        "nr_of_beads_considered_bad_x_fit": bead_properties_df.groupby("channel_nr")[
            "considered_bad_x_fit"
        ]
        .apply(lambda x: (x == True).sum())
        .tolist(),
        "fit_rss_z_mean": bead_properties_df.groupby("channel_nr")["z_fit_rss"].mean().tolist(),
        "fit_rss_z_median": bead_properties_df.groupby("channel_nr")["z_fit_rss"].median().tolist(),
        "fit_rss_z_std": bead_properties_df.groupby("channel_nr")["z_fit_rss"].std().tolist(),
        "fit_rss_y_mean": bead_properties_df.groupby("channel_nr")["y_fit_rss"].mean().tolist(),
        "fit_rss_y_median": bead_properties_df.groupby("channel_nr")["y_fit_rss"].median().tolist(),
        "fit_rss_y_std": bead_properties_df.groupby("channel_nr")["y_fit_rss"].std().tolist(),
        "fit_rss_x_mean": bead_properties_df.groupby("channel_nr")["x_fit_rss"].mean().tolist(),
        "fit_rss_x_median": bead_properties_df.groupby("channel_nr")["x_fit_rss"].median().tolist(),
        "fit_rss_x_std": bead_properties_df.groupby("channel_nr")["x_fit_rss"].std().tolist(),
        "resolution_mean_fwhm_z_pixels": bead_properties_df.groupby("channel_nr")["z_fwhm"]
        .mean()
        .tolist(),
        "resolution_median_fwhm_z_pixels": bead_properties_df.groupby("channel_nr")["z_fwhm"]
        .median()
        .tolist(),
        "resolution_std_fwhm_z_pixels": bead_properties_df.groupby("channel_nr")["z_fwhm"]
        .std()
        .tolist(),
        "resolution_mean_fwhm_y_pixels": bead_properties_df.groupby("channel_nr")["y_fwhm"]
        .mean()
        .tolist(),
        "resolution_median_fwhm_y_pixels": bead_properties_df.groupby("channel_nr")["y_fwhm"]
        .median()
        .tolist(),
        "resolution_std_fwhm_y_pixels": bead_properties_df.groupby("channel_nr")["y_fwhm"]
        .std()
        .tolist(),
        "resolution_mean_fwhm_x_pixels": bead_properties_df.groupby("channel_nr")["x_fwhm"]
        .mean()
        .tolist(),
        "resolution_median_fwhm_x_pixels": bead_properties_df.groupby("channel_nr")["x_fwhm"]
        .median()
        .tolist(),
        "resolution_std_fwhm_x_pixels": bead_properties_df.groupby("channel_nr")["x_fwhm"]
        .std()
        .tolist(),
        "resolution_mean_fwhm_z_microns": bead_properties_df.groupby("channel_nr")["z_fwhm_micron"]
        .mean()
        .tolist(),
        "resolution_median_fwhm_z_microns": bead_properties_df.groupby("channel_nr")[
            "z_fwhm_micron"
        ]
        .median()
        .tolist(),
        "resolution_std_fwhm_z_microns": bead_properties_df.groupby("channel_nr")["z_fwhm_micron"]
        .std()
        .tolist(),
        "resolution_mean_fwhm_y_microns": bead_properties_df.groupby("channel_nr")["y_fwhm_micron"]
        .mean()
        .tolist(),
        "resolution_median_fwhm_y_microns": bead_properties_df.groupby("channel_nr")[
            "y_fwhm_micron"
        ]
        .median()
        .tolist(),
        "resolution_std_fwhm_y_microns": bead_properties_df.groupby("channel_nr")["y_fwhm_micron"]
        .std()
        .tolist(),
        "resolution_mean_fwhm_x_microns": bead_properties_df.groupby("channel_nr")["x_fwhm_micron"]
        .mean()
        .tolist(),
        "resolution_median_fwhm_x_microns": bead_properties_df.groupby("channel_nr")[
            "x_fwhm_micron"
        ]
        .median()
        .tolist(),
        "resolution_std_fwhm_x_microns": bead_properties_df.groupby("channel_nr")["x_fwhm_micron"]
        .std()
        .tolist(),
        "resolution_mean_fwhm_lateral_asymmetry_ratio": bead_properties_df.groupby("channel_nr")[
            "fwhm_lateral_asymmetry_ratio"
        ]
        .mean()
        .tolist(),
        "resolution_median_fwhm_lateral_asymmetry_ratio": bead_properties_df.groupby("channel_nr")[
            "fwhm_lateral_asymmetry_ratio"
        ]
        .median()
        .tolist(),
        "resolution_std_fwhm_lateral_asymmetry_ratio": bead_properties_df.groupby("channel_nr")[
            "fwhm_lateral_asymmetry_ratio"
        ]
        .std()
        .tolist(),
    }


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
    z_fitted_profile, z_rss, z_fwhm, z_center_pos = fit_airy(z_profile)
    y_fitted_profile, y_rss, y_fwhm, y_center_pos = fit_airy(y_profile)
    x_fitted_profile, x_rss, x_fwhm, x_center_pos = fit_airy(x_profile)

    if all(voxel_size_micron):
        z_fwhm_micron = z_fwhm * voxel_size_micron[0]
        y_fwhm_micron = y_fwhm * voxel_size_micron[1]
        x_fwhm_micron = x_fwhm * voxel_size_micron[2]
    else:
        z_fwhm_micron = None
        y_fwhm_micron = None
        x_fwhm_micron = None

    considered_axial_edge = (
        z_center_pos - z_profile[0] < z_fwhm * 4 or z_profile[-1] - z_center_pos < z_fwhm * 4
    )

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
        channel = gaussian(image=channel, sigma=sigma, preserve_range=True)
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
        image=channel, threshold_rel=0.2, min_distance=int(min_distance)
    )
    positions_proximity_edge_filtered = peak_local_max(
        image=channel,
        threshold_rel=0.2,
        min_distance=int(min_distance),
        exclude_border=(1, int(min_distance // 2), int(min_distance // 2)),
        p_norm=2,
    )

    # Convert arrays to sets for easier comparison
    positions_all_set = set(map(tuple, positions_all))
    positions_proximity_filtered_set = set(map(tuple, positions_proximity_filtered))
    positions_proximity_edge_filtered_set = set(map(tuple, positions_proximity_edge_filtered))
    positions_edge_filtered_set = (
        positions_proximity_filtered_set & positions_proximity_edge_filtered_set
    )

    valid_positions_set = positions_proximity_edge_filtered_set
    discarded_positions_proximity_set = positions_all_set - positions_proximity_filtered_set
    discarded_positions_edge_set = positions_all_set - positions_edge_filtered_set
    discarded_positions_set = positions_all_set - positions_proximity_edge_filtered_set

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
            (pos[1] - int(min_distance // 2)) : (pos[1] + int(min_distance // 2)),
            (pos[2] - int(min_distance // 2)) : (pos[2] + int(min_distance // 2)),
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
            ch_consid_ax_edge_positions,
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
        bead_considered_axial_edge.append(ch_consid_ax_edge_positions)

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
        return self.input.min_lateral_distance_factor

    def _generate_centroids_roi(
        self, positions, root_name, color, stroke_width, positions_filter=None
    ):
        rois = {}

        # TODO: add a condition to not create the ROI if no beads are found?
        for image_label, input_image in self.input.psf_beads_images.items():
            shapes = {}
            for ch in range(input_image.data.shape[-1]):
                if positions_filter is None:
                    for i, pos in enumerate(positions[image_label][ch]):
                        shapes[f"ch{ch:02d}_b{i:02d}"] = mm_schema.Point(
                            label=f"ch{ch:02d}_b{i:02d}",
                            z=pos[0],
                            y=pos[1],
                            x=pos[2],
                            c=ch,
                            stroke_color=mm_schema.Color(
                                r=color[0], g=color[1], b=color[2], alpha=color[3]
                            ),
                            stroke_width=stroke_width,
                        )
                else:
                    for i, (pos, is_filtered) in enumerate(
                        zip(positions[image_label][ch], positions_filter[image_label][ch])
                    ):
                        if is_filtered:
                            shapes[f"ch{ch:02d}_b{i:02d}"] = mm_schema.Point(
                                label=f"ch{ch:02d}_b{i:02d}",
                                z=pos[0],
                                y=pos[1],
                                x=pos[2],
                                c=ch,
                                stroke_color=mm_schema.Color(
                                    r=color[0], g=color[1], b=color[2], alpha=color[3]
                                ),
                                stroke_width=stroke_width,
                            )
            label = f"{root_name}_{image_label}"
            rois[label] = mm_schema.RoiMassCenters(
                label=label,
                description=f"{root_name} in image {image_label}",
                image=image_label,
                shapes=shapes,
            )

        return rois

    def _generate_profiles_table(self, axis, raw_profiles, fitted_profiles):
        axis_names = ["z", "y", "x"]
        if len(raw_profiles) != len(fitted_profiles):
            logger.error(
                f"Raw and fitted profiles for axis {axis_names[axis]} must have the same number of images. Raising error."
            )
            raise ValueError(
                f"Raw and fitted profiles for axis {axis_names[axis]} must have the same image length"
            )

        if any(
            len(raw_profiles[image_label]) != len(fitted_profiles[image_label])
            for image_label in raw_profiles
        ):
            logger.error(
                f"Raw and fitted profiles for axis {axis_names[axis]} must have the same number of profiles. Raising error."
            )
            raise ValueError(
                f"Raw and fitted profiles for axis {axis_names[axis]} must have the same number of profiles."
            )

        if all(
            all(not ch_profiles for ch_profiles in raw_profiles[image_label])
            for image_label in raw_profiles
        ):
            logger.error(f"No profiles for axis {axis_names[axis]} available. No table generated.")
            return None

        profiles = {}
        descriptions = {}
        for image_label in self.input.psf_beads_images.keys():
            for ch in range(self.input.psf_beads_images[image_label].data.shape[-1]):
                for i, (raw, fitted) in enumerate(
                    zip(raw_profiles[image_label][ch], fitted_profiles[image_label][ch])
                ):
                    profiles[f"{image_label}_ch_{ch:02d}_bead_{i:02d}_raw"] = raw[axis].tolist()
                    descriptions[
                        f"{image_label}_ch_{ch:02d}_bead_{i:02d}_raw"
                    ] = f"Bead {i:02d} in channel {ch} of image {image_label} raw profile in {axis_names[axis]} axis"

                    profiles[f"{image_label}_ch_{ch:02d}_bead_{i:02d}_fitted"] = fitted[
                        axis
                    ].tolist()
                    descriptions[
                        f"{image_label}_ch_{ch:02d}_bead_{i:02d}_fitted"
                    ] = f"Bead {i:02d} in channel {ch} of image {image_label} fitted profile in {axis_names[axis]} axis"

        return dict_to_table_inlined(
            name=f"bead_profiles_{axis_names[axis]}",
            dictionary=profiles,
            table_description=f"Bead profiles in {axis_names[axis]} axis",
            column_description=descriptions,
        )

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
        bead_considered_bad_z_fit = {}
        bead_considered_bad_y_fit = {}
        bead_considered_bad_x_fit = {}

        # Prepare data
        for label, image in self.input.psf_beads_images.items():
            images[label] = image.data[0, ...]

            voxel_sizes_micron[label] = (
                image.voxel_size_z_micron,
                image.voxel_size_y_micron,
                image.voxel_size_x_micron,
            )
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
                f"    {len(image_output['bead_considered_axial_edge'])} beads considered as to close to the top or bottom of the image"
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
            bead_considered_bad_z_fit[image_label] = [
                [b_rss[0] > fitting_rss_threshold for b_rss in ch_rss]
                for ch_rss in image_output["bead_rsss"]
            ]
            bead_considered_bad_y_fit[image_label] = [
                [b_rss[1] > fitting_rss_threshold for b_rss in ch_rss]
                for ch_rss in image_output["bead_rsss"]
            ]
            bead_considered_bad_x_fit[image_label] = [
                [b_rss[2] > fitting_rss_threshold for b_rss in ch_rss]
                for ch_rss in image_output["bead_rsss"]
            ]

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
            # Image linked information
            for ch in range(input_image.data.shape[-1]):
                # Channel linked information
                for i, bead in enumerate(bead_crops[image_label][ch]):
                    output_bead_crops[
                        f"{input_image.name}_ch_{ch:02d}_bead_{i:02d}"
                    ] = numpy_to_image_byref(
                        array=np.expand_dims(bead, axis=(0, 4)),
                        image_url=f"{input_image.name}_ch_{ch:02d}_bead_{i:02d}",
                        name=f"{input_image.name}_ch_{ch:02d}_bead_{i:02d}",
                        description=f"Bead crop for bead nr {i}, on channel {ch}, image {image_label}",
                        source_image_url=self.input.psf_beads_images[image_label].image_url,
                    )

                    # Append data to beads table
                    bead_properties["image_label"].append(image_label)
                    bead_properties["image_name"].append(input_image.name)
                    bead_properties["channel_nr"].append(ch)
                    bead_properties["bead_nr"].append(i)
                    bead_properties["intensity_max"].append(bead.max())
                    bead_properties["min_intensity_min"].append(bead.min())
                    bead_properties["intensity_std"].append(bead.std())
                    bead_properties["intensity_zscore"].append(bead_zscores[image_label][ch][i])
                    bead_properties["considered_intensity_outlier"].append(
                        bead_considered_intensity_outlier[image_label][ch][i]
                    )
                    bead_properties["z_centroid"].append(bead_positions[image_label][ch][i][0])
                    bead_properties["y_centroid"].append(bead_positions[image_label][ch][i][1])
                    bead_properties["x_centroid"].append(bead_positions[image_label][ch][i][2])
                    bead_properties["z_fit_rss"].append(bead_rsss[image_label][ch][i][0])
                    bead_properties["y_fit_rss"].append(bead_rsss[image_label][ch][i][1])
                    bead_properties["x_fit_rss"].append(bead_rsss[image_label][ch][i][2])
                    bead_properties["considered_bad_z_fit"].append(
                        bead_rsss[image_label][ch][i][0] > fitting_rss_threshold
                    )
                    bead_properties["considered_bad_y_fit"].append(
                        bead_rsss[image_label][ch][i][1] > fitting_rss_threshold
                    )
                    bead_properties["considered_bad_x_fit"].append(
                        bead_rsss[image_label][ch][i][2] > fitting_rss_threshold
                    )
                    bead_properties["z_fwhm"].append(bead_fwhms[image_label][ch][i][0])
                    bead_properties["y_fwhm"].append(bead_fwhms[image_label][ch][i][1])
                    bead_properties["x_fwhm"].append(bead_fwhms[image_label][ch][i][2])
                    bead_properties["fwhm_lateral_asymmetry_ratio"].append(
                        max(bead_fwhms[image_label][ch][i][1], bead_fwhms[image_label][ch][i][2])
                        / min(bead_fwhms[image_label][ch][i][1], bead_fwhms[image_label][ch][i][2])
                    )
                    bead_properties["z_fwhm_micron"].append(
                        bead_fwhms_micron[image_label][ch][i][0]
                    )
                    bead_properties["y_fwhm_micron"].append(
                        bead_fwhms_micron[image_label][ch][i][1]
                    )
                    bead_properties["x_fwhm_micron"].append(
                        bead_fwhms_micron[image_label][ch][i][2]
                    )
                    bead_properties["considered_axial_edge"].append(
                        bead_considered_axial_edge[image_label][ch][i]
                    )

        self.output = mm_schema.PSFBeadsOutput(
            bead_crops=output_bead_crops,
            analyzed_bead_centroids=self._generate_centroids_roi(
                positions=bead_positions,
                root_name="analyzed_bead_centroids",
                color=(0, 255, 0, 100),
                stroke_width=8,
            ),
            discarded_bead_centroids_lateral_edge=self._generate_centroids_roi(
                positions=discarded_positions_lateral_edge,
                root_name="discarded_bead_centroids_lateral_edge",
                color=(255, 0, 0, 100),
                stroke_width=4,
            ),
            discarded_bead_centroids_self_proximity=self._generate_centroids_roi(
                positions=discarded_positions_self_proximity,
                root_name="discarded_bead_centroids_self_proximity",
                color=(255, 0, 0, 100),
                stroke_width=4,
            ),
            considered_bead_centroids_axial_edge=self._generate_centroids_roi(
                positions=bead_positions,
                root_name="considered_bead_centroids_axial_edge",
                color=(0, 0, 255, 100),
                stroke_width=4,
                positions_filter=bead_considered_axial_edge,
            ),
            considered_bead_centroids_intensity_outlier=self._generate_centroids_roi(
                positions=bead_positions,
                root_name="considered_bead_centroids_intensity_outlier",
                color=(0, 0, 255, 100),
                stroke_width=4,
                positions_filter=bead_considered_intensity_outlier,
            ),
            considered_bead_centroids_z_fit_quality=self._generate_centroids_roi(
                positions=bead_positions,
                root_name="considered_bead_centroids_z_fit_quality",
                color=(0, 0, 255, 100),
                stroke_width=4,
                positions_filter=bead_considered_bad_z_fit,
            ),
            considered_bead_centroids_y_fit_quality=self._generate_centroids_roi(
                positions=bead_positions,
                root_name="considered_bead_centroids_y_fit_quality",
                color=(0, 0, 255, 100),
                stroke_width=4,
                positions_filter=bead_considered_bad_y_fit,
            ),
            considered_bead_centroids_x_fit_quality=self._generate_centroids_roi(
                positions=bead_positions,
                root_name="considered_bead_centroids_x_fit_quality",
                color=(0, 0, 255, 100),
                stroke_width=4,
                positions_filter=bead_considered_bad_x_fit,
            ),
            key_values=mm_schema.PSFBeadsKeyMeasurements(
                **_generate_key_values(
                    bead_properties_df=pd.DataFrame(bead_properties),
                    discarded_positions_self_proximity=discarded_positions_self_proximity,
                    discarded_positions_lateral_edge=discarded_positions_lateral_edge,
                )
            ),
            bead_properties=dict_to_table_inlined(bead_properties, "bead_properties"),
            bead_z_profiles=self._generate_profiles_table(
                axis=0, raw_profiles=bead_profiles, fitted_profiles=bead_fitted_profiles
            ),
            bead_y_profiles=self._generate_profiles_table(
                axis=1, raw_profiles=bead_profiles, fitted_profiles=bead_fitted_profiles
            ),
            bead_x_profiles=self._generate_profiles_table(
                axis=2, raw_profiles=bead_profiles, fitted_profiles=bead_fitted_profiles
            ),
        )

        self.processed = True

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
