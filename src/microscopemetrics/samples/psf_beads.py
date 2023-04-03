import logging
from typing import Tuple

import numpy as np
from pandas import DataFrame
from pydantic.color import Color
from scipy.optimize import curve_fit, fsolve
from skimage.feature import peak_local_max
from skimage.filters import gaussian

from microscopemetrics.samples import *

from ..utilities.utilities import airy_fun, gaussian_fun

module_logger = logging.getLogger("metrics.samples.psf_beads")


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
    popt, pcov = curve_fit(airy_fun, x, profile, guess)

    fitted_profile = airy_fun(x, popt[0], popt[1])

    def _f(d):
        return airy_fun(d, popt[0], popt[1]) - (fitted_profile.max() - fitted_profile.min()) / 2

    guess = np.array([fitted_profile.argmax() - 1, fitted_profile.argmax() + 1])
    v = fsolve(_f, guess)
    fwhm = abs(v[1] - v[0])

    return fitted_profile, fwhm


@register_image_analysis
class PSFBeadsAnalysis(Analysis):
    """This class handles a PSF beads sample"""

    def __init__(self, config=None):
        super().__init__(
            output_description="Analysis output of samples containing PSF grade fluorescent beads. "
            "It contains information about resolution."
        )
        self.add_data_requirement(
            name="beads_image",
            description="The image containing the beads in teh form of a numpy array",
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
            name="min_lateral_distance_factor",
            description="Minimal distance that has to separate laterally the beads represented as the "
            "number of times the theoretical resolution.",
            data_type=int,
            optional=True,
            default=20,
        )
        self.add_metadata_requirement(
            name="theoretical_fwhm_lateral_res",
            description="Theoretical FWHM lateral resolution of the sample.",
            data_type=float,
            units="MICRON",
            optional=False,
        )
        self.add_metadata_requirement(
            name="theoretical_fwhm_axial_res",
            description="Theoretical FWHM axial resolution of the sample.",
            data_type=float,
            units="MICRON",
            optional=False,
        )
        self.add_metadata_requirement(
            name="sigma",
            description="When provided, smoothing sigma to be applied to image prior to bead detection."
            "Does not apply to resolution measurements",
            data_type=float,
            optional=True,
            default=None,
        )

    @staticmethod
    def _analyze_bead(image):
        # Find the strongest sections to generate profiles
        x_max = np.max(image, axis=(0, 1))
        x_focus = np.argmax(x_max)
        y_max = np.max(image, axis=(0, 2))
        y_focus = np.argmax(y_max)
        z_max = np.max(image, axis=(1, 2))
        z_focus = np.argmax(z_max)

        # Generate profiles
        x_profile = np.squeeze(image[z_focus, y_focus, :])
        y_profile = np.squeeze(image[z_focus, :, x_focus])
        z_profile = np.squeeze(image[:, y_focus, x_focus])

        # Fitting the profiles
        x_fitted_profile, x_fwhm = _fit_airy(x_profile)
        y_fitted_profile, y_fwhm = _fit_airy(y_profile)
        z_fitted_profile, z_fwhm = _fit_airy(z_profile)

        return (
            (z_profile, y_profile, x_profile),
            (z_fitted_profile, y_fitted_profile, x_fitted_profile),
            (z_fwhm, y_fwhm, x_fwhm),
        )

    @staticmethod
    def _find_beads(image, min_distance, sigma=None):

        image = np.squeeze(image)
        image_mip = np.max(image, axis=0)

        if sigma is not None:
            image_mip = gaussian(
                image=image_mip, multichannel=False, sigma=sigma, preserve_range=True
            )

        # Find bead centers
        positions_2d = peak_local_max(image=image_mip, threshold_rel=0.2, min_distance=5)
        # Add the mas intensity value in z
        positions_3d = np.insert(
            positions_2d[:],
            0,
            np.argmax(image[:, positions_2d[:, 0], positions_2d[:, 1]], axis=0),
            axis=1,
        )

        nr_beads = positions_2d.shape[0]
        module_logger.info(f"Beads found: {nr_beads}")

        # Exclude beads too close to the edge
        edge_keep_mask = (
            (positions_2d[:, 0] > min_distance)
            & (positions_2d[:, 0] < image_mip.shape[0] - min_distance)
            & (positions_2d[:, 1] > min_distance)
            & (positions_2d[:, 1] < image_mip.shape[1] - min_distance)
        )
        module_logger.info(f"Beads too close to the edge: {nr_beads - np.sum(edge_keep_mask)}")

        # Exclude beads too close to each other
        proximity_keep_mask = np.ones((nr_beads, nr_beads), dtype=bool)
        for i, pos in enumerate(positions_2d):
            proximity_keep_mask[i] = (abs(positions_2d[:, 0] - pos[0]) > min_distance) | (
                abs(positions_2d[:, 1] - pos[1]) > min_distance
            )
            proximity_keep_mask[i, i] = True  # Correcting the diagonal
        proximity_keep_mask = np.all(proximity_keep_mask, axis=0)
        module_logger.info(
            f"Beads too close to each other: {nr_beads - np.sum(proximity_keep_mask)}"
        )

        # Exclude beads too intense or too weak
        intensity_keep_mask = np.ones(nr_beads, dtype=bool)
        # TODO: Implement beads intensity filter
        module_logger.info(
            f"Beads too intense (probably more than one bead): {nr_beads - np.sum(intensity_keep_mask)}"
        )

        keep_mask = edge_keep_mask & proximity_keep_mask & intensity_keep_mask
        module_logger.info(f"Beads kept for analysis: {np.sum(keep_mask)}")

        positions = positions_3d[keep_mask, :]
        pos_edge_disc = positions_3d[np.logical_not(edge_keep_mask), :]
        pos_proximity_disc = positions_3d[np.logical_not(proximity_keep_mask), :]
        pos_intensity_disc = positions_3d[np.logical_not(intensity_keep_mask), :]

        bead_images = [
            image[
                :,
                (pos[1] - (min_distance // 2)) : (pos[1] + (min_distance // 2)),
                (pos[2] - (min_distance // 2)) : (pos[2] + (min_distance // 2)),
            ]
            for pos in positions
        ]
        return (
            bead_images,
            positions,
            pos_edge_disc,
            pos_proximity_disc,
            pos_intensity_disc,
        )

    def estimate_min_bead_distance(self):
        # TODO: get the resolution somewhere or pass it as a metadata
        res = 3  # theoretical resolution in pixels
        distance = self.get_metadata_values("min_lateral_distance_factor")
        return res * distance

    def _run(self):
        """Analyzes images of sub-resolution beads in order to extract data on the optical
        performance of the microscope.
        """
        # Verify that image is not saturated
        if np.issubdtype(self.get_data_values("beads_image").dtype, np.integer):
            if (
                self.get_data_values("beads_image").max()
                == np.iinfo(self.get_data_values("beads_image").dtype).max
            ):
                logger.error("Image is saturated. No attempt to find beads will be done.")
                return False
        elif np.issubdtype(self.get_data_values("beads_image").dtype, np.float):
            if (
                self.get_data_values("beads_image").max()
                == np.finfo(self.get_data_values("beads_image").dtype).max
            ):
                logger.error("Image is saturated. No attempt to find beads will be done.")
                return False

        # Get some analysis_config parameters
        pixel_size_units = self.get_metadata_units("pixel_size")
        pixel_size = self.get_metadata_values("pixel_size")
        min_bead_distance = self.estimate_min_bead_distance()

        # Remove all negative intensities. eg. 3D-SIM images may contain negative values.
        image_data = np.clip(self.get_data_values("beads_image"), a_min=0, a_max=None)

        # Validating nyquist
        try:
            if pixel_size[1] > (2 * self.get_metadata_values("theoretical_fwhm_lateral_res")):
                module_logger.warning("Nyquist criterion is not fulfilled in the lateral direction")
            if pixel_size[0] > (2 * self.get_metadata_values("theoretical_fwhm_axial_res")):
                module_logger.warning("Nyquist criterion is not fulfilled in the axial direction")
        except (TypeError, IndexError) as e:
            module_logger.error("Could not validate Nyquist sampling criterion")

        (
            bead_images,
            positions,
            positions_edge_discarded,
            positions_proximity_discarded,
            positions_intensity_discarded,
        ) = self._find_beads(
            image=image_data,
            min_distance=min_bead_distance,
            sigma=self.get_metadata_values("sigma"),
        )

        for i, bead_image in enumerate(bead_images):
            self.output.append(
                model.Image(
                    name=f"bead_nr{i:02d}",
                    description=f"PSF bead crop for bead nr {i}",
                    data=np.expand_dims(bead_image, axis=(1, 2)),
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
            for pos in positions_edge_discarded
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
            for pos in positions_proximity_discarded
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

        # Generate profiles and measure FWHM
        raw_profiles = []
        fitted_profiles = []
        fwhm_values = []
        for bead_image in bead_images:
            opr, fpr, fwhm = self._analyze_bead(bead_image)
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

        self.output.append(
            model.Table(
                name="Analysis_PSF_properties",
                description="Properties associated with the analysis",
                table=properties_df,
            )
        )

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
