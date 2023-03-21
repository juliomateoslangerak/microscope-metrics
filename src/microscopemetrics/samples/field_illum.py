
"""This file demonstrates how someone can create a new sample module. This example will create a fully functional
but naive analysis where lines are detected through a progressive probabilistic hough transform from scikit-image.
See official documentation at https://scikit-image.org/docs/0.7.0/api/skimage.transform.html#probabilistic-hough

The procedure to follow is, in short:
- import everything from the samples module
- import the types that you might be using from the typing module
- import any necessary libraries that you will need for your analysis
- Create one or more subclasses of the Analysis abstract class of samples. Within each class:
    - define your input requirements
    - define a 'run' method that will implement the logic of your analysis
    - if desired, define a 'plot' method returning a plot showing the results of the analysis
"""
import numpy as np

# import the sample functionality
from microscopemetrics.samples import *

# import utility function
#from microscopemetrics.utilities import is_saturated

# import the types that you may be using
from typing import Tuple

# import anything you will need for your analysis
from pandas import DataFrame
from skimage.transform import probabilistic_hough_line
from scipy.spatial import distance
from math import atan2
from pydantic.color import Color
from skimage import draw
from skimage.measure import regionprops


def get_norm_intensity_matrix(img):
    """
    get normalized intensity matrix: divide all the pixels' intensity
    by the maximum intensity.
    Parameters
    ----------
    img : np.array
        image on a 2d np.array format.
    Returns
    -------
    norm_intensity_profile : np.array
        2d np.array where pixel values are scaled by the max intensity of
        the original image.
    """

    max_intensity = np.max(img)
    # the rule of three : max_intensity->100%, pixel_intensity*100/max
    norm_intensity_profile = np.round(img/max_intensity * 100)
    return DataFrame(norm_intensity_profile)


def get_max_intensity_region_table(img):
    """
    this function finds the max intensity area of the given image
    in order to figure out the number of pixels,the center of mass and
    the max intensity of the corresponding area.
    Parameters
    ----------
    img : np.array.
        2d np.array.
    Returns
    -------
    center_of_mass: dict
        dict encolsing the number of pixels, the coordinates of the
        center of mass of the and the max intensity value of the max intensity
        area of the provided image.
    """

    max_intensity = np.max(img)

    # define the maximum intensity
    threshold_value = max_intensity-1

    # label pixels with max intesity values: binary matrix.
    labeled_foreground = (img > threshold_value).astype(int)

    # identify the region of max intensity
    properties = regionprops(labeled_foreground, img)

    # identify the center of mass of the max intensity area
    center_of_mass = (int(properties[0].centroid[0]),
                      int(properties[0].centroid[1]))

    # number of pixels of max intensity region
    nb_pixels = properties[0].area

    # organize info in dataframe
    max_region_info = {
        "nb pixels": [nb_pixels],
        "center of mass": [center_of_mass],
        "max intensity": [max_intensity]
        }

    return max_region_info


def get_norm_intensity_profile(img, save_path=""):
    """
    plots the normalized intensity profile of the image.
    the center of mass of the max intensity area is marked in red.
    If save_path is not empty, the generated figure will be saved as png in
    the provided path.
    Parameters
    ----------
    img : np.array
        image on a 2d np.array format.
    save_path : str, optional
        path to save the generated figure including filename.
        The default is "".
    Returns
    -------
    fig : matplotlib.figure.Figure
        returns the normalized intensity profile of the image with
        the center of mass of the max intensity area marked in red.
    """

    # normalized intensity array of the given image
    norm_intensity_profile = get_norm_intensity_matrix(img)
    # coordinates of center of mass of mac intensity area
    x_mass, y_mass = get_max_intensity_region_table(img)["center of mass"][0]

    # figure construction
    fig, ax = plt.subplots()
    ax.scatter(y_mass, x_mass, s=60, color="r", marker='+')
    plt.imshow(norm_intensity_profile)
    plt.colorbar()
    plt.title("normalized intensity profile", figure=fig)
    if save_path:
        plt.savefig(str(save_path),
                    bbox_inches='tight')

    return fig


# 3. intensity profiles


def get_pixel_values_of_line(img, x0, y0, xf, yf):
    """
    get the value of a line of pixels.
    the line defined by the user using the corresponding first and last
    pixel indices.
    Parameters
    ----------
    img : np.array.
        image on a 2d np.array format.
    x0 : int
        raw number of the starting pixel
    y0 : int
        column number of the starting pixel.
    xf : int
        raw number of the ending pixel.
    yf : int
        column number of the ending pixel.
    Returns
    -------
    line_pixel_values : np.array
        1d np.array representing the values of the chosen line of pixels.
    """
    rr, cc = np.array(draw.line(x0, y0, xf, yf))
    # line_pixel_values = [img[rr[i], cc[i]] for i in range(len(rr))]
    line_pixel_values = img[rr, cc]
    return line_pixel_values


def get_x_axis(y_axis):
    """
    get x axis values for the intensity plot given y values.
    Parameters
    ----------
    y : np.array
        1d np.array representing the y axis values of the intensity plot.
    Returns
    -------
    x_axis : np.array
        x axis values for the intensity plot.
    """
    nb_pixels = len(y_axis)
    # center the pixel value vector around 0
    x_axis = np.arange(round(-nb_pixels/2), round(nb_pixels/2+1), 1)
    # the center of the matrix is 4 pixels not one
    x_axis = x_axis[x_axis != 0]
    return x_axis


def get_intensity_plot(img, save_path=""):
    """
    get the distribution of pixel intensities of the mid
    vertical, mid horizontal and the two diagonal lines of a given image.
    the vertical line y=0 on the plot represent to the image center.
    If save_path is not empty, the generated figure will be saved as png in
    the provided path.
    Parameters
    ----------
    img : np.array
        image on a 2d np.array format.
    save_path : str, optional
        path to save the generated figure inluding file name.
        The default is "".
    Returns
    -------
    fig : matplotlib.figure.Figure
        distribution of pixel intensities of the mid vertical, mid horizontal
        and the two diagonal lines of a given image.
        the vertical line y=0 on the plot represent to the image center.
    fig_data : dict
        dict representing the data used to generate the fig.
        the 8 keys are organised by pair with x axis and y axis data:
            - x_axis_V_seg and y_axis_V_seg
            - x_axis_H_seg and y_axis_H_seg
            - x_axis_diagUD and y_axis_diagUD
            - x_axis_diagDU and y_axis_diagDU
    """

    xmax, ymax = np.shape(img)
    xmax = xmax-1
    ymax = ymax-1
    xmid = round(xmax/2)
    ymid = round(ymax/2)
    # mid vertical pixel segment
    V_seg = get_pixel_values_of_line(img, x0=0, y0=ymid, xf=xmax, yf=ymid)
    # mid horizontal pixel segment
    H_seg = get_pixel_values_of_line(img, x0=xmid, y0=0, xf=xmid, yf=ymax)
    # diagonal UpDown Left Right
    diagUD = get_pixel_values_of_line(img, x0=0, y0=0, xf=xmax, yf=ymax)
    # diagonal DownUp Left Right
    diagDU = get_pixel_values_of_line(img, x0=xmax, y0=0, xf=0, yf=ymax)

    # plot data into pandas array
    fig_data = {}
    fig_data["x_axis_V_seg"] = get_x_axis(V_seg)
    fig_data["y_axis_V_seg"] = V_seg

    fig_data["x_axis_H_seg"] = get_x_axis(H_seg)
    fig_data["y_axis_H_seg"] = H_seg

    fig_data["x_axis_diagUD"] = get_x_axis(diagUD)
    fig_data["y_axis_diagUD"] = diagUD

    fig_data["x_axis_diagDU"] = get_x_axis(diagDU)
    fig_data["y_axis_diagDU"] = diagDU

    # plot
    """
    fig = plt.figure()
    plt.plot(get_x_axis(V_seg), V_seg, color="b", label="V_seg", figure=fig)
    plt.plot(get_x_axis(H_seg), H_seg, color="g", label="H_seg", figure=fig)

    plt.plot(get_x_axis(diagUD), diagUD, color="r", label="Diag1", figure=fig)
    plt.plot(get_x_axis(diagDU), diagDU, color="y", label="Diag2", figure=fig)

    plt.axvline(0, linestyle='--')
    plt.title("Intensity Profiles", figure=fig)
    plt.xlim((min(get_x_axis(diagUD))-25, max(get_x_axis(diagUD))+25))
    plt.legend()

    if save_path:
        plt.savefig(str(save_path),
                    bbox_inches='tight')
    """
    return fig_data


# 4. profile statistics


def get_profile_statistics_table(img):
    """
    given an image in a 2d np.array format, this function return the pixel
    intensity values of 9 specific pixels and their ratio over the maximum
    intensity. The 9 concerned pixels are:
        - top-left corner
        - upper-middle pixel
        - top-right corner
        - left-middle pixel
        - maximum intensity pixel
        - right-middle pixel
        - bottom-left corner
        - bottom-middle pixel
        - bottom-right corner
    Parameters
    ----------
    img : np.array
        image on a 2d np.array format.
    Returns
    -------
    profiles_statistics : dict
        dict showing the intensity values of the concerned 9 pixels and
        their ratio over the maximum intensity value of the array.
    """

    # find the maximum intensity and the corresponding pixel.
    max_intensity = np.max(img)
    xx_max, yy_max = np.where(img == max_intensity)

    # if max intensity is in >1 pixels, we chose only the first localization
    x_index_max_intensity = xx_max[0]
    y_index_max_intensity = yy_max[0]

    max_found_at = [x_index_max_intensity, y_index_max_intensity]

    # 3 by 3 grid going through each corner and the middle of each line:

    # tl, um, tr
    # lm, cc, rm
    # bl, bm, br

    xx, yy = np.meshgrid([0, img.shape[0] // 2, -1],
                         [0, img.shape[1] // 2, -1])
    max_intensities = np.around(img[xx, yy].flatten(), 2)
    max_intensities_relative = np.around(max_intensities/max_intensity, 2)

    # replace central pixel value with max intensity
    max_intensities[4] = max_intensity
    max_intensities_relative[4] = 1.0

    # build dictionnary
    profiles_statistics_dict = {}
    profiles_statistics_dict["location"] = [
         "top-left corner",
         "upper-middle pixel",
         "top-right corner",
         "left-middle pixel",
         f"maximum found at {max_found_at}",
         "right-middle pixel",
         "bottom-left corner",
         "bottom-middle pixel",
         "bottom-right corner",
     ]

    profiles_statistics_dict["intensity"] = max_intensities
    profiles_statistics_dict["intensity relative to max"] = \
        max_intensities_relative

    return profiles_statistics_dict


@register_image_analysis
class FieldHomogeneityAnalysis(
    Analysis
):  # Subclass Analysis for each analysis you want to implement for a given sample
    """Write a good documentation:
    This analysis creates a report on field illumination homogeneity based on input images"""

    # Define the __init__
    def __init__(self):
        # Call the super __init__ method which takes a single argument: the description of the output
        super().__init__(output_description="This analysis returns...")

        # Add metadata requirements for the analysis
        self.add_data_requirement(
            name="image",
            description="An image with lines as a numpy array",
            data_type=np.ndarray,
        )
        self.add_metadata_requirement(
            name="bitDepth",
            description="Camera bitDepth",
            data_type=Tuple[float, float],  # We can use complex data types
            units="bits",  # You should specify units when necessary
            optional=True,  # This parameter will not be optional
        )
        self.add_metadata_requirement(
            name="threshold",
            description="Threshold for saturation",
            data_type=int,  # And we can use standard data types
            optional=True,  # When optional, this parameter will not have to be provided
            default=10,  # If a requirement is optional you may provide a default value that will be
        )  # used in case you dont provide any value


    # You must define a run method taking no parameters. This method will run the analysis
    def run(self):
        logger.info(
            "Validating requirements..."
        )  # You may use the logger function to log info

        # It is a good practice to verify all the requirements before running the analysis
        # This will verify that all the non optional requirements are provided
        if len(self.list_unmet_requirements()):
            # we can use the logger to report errors
            logger.error(
                f"The following metadata requirements ara not met: {self.list_unmet_requirements()}"
            )
            return (
                False  # The run method should return False upon unsuccessful execution
            )

        logger.info("Checking image saturation")

        """
        saturated = is_saturated(
            image=self.get_data_values(
                "image"
            ),  # The input image data is accessible through the input.data
            threshold=self.get_metadata_values(
                "threshold"
            ),  # You may access the metadata like this too
            bitDepth=self.get_metadata_values(
                "bitDepth"
            ),
        )

        if saturated:
            logger.info("Image is saturated")
            return False
        # 'lines' is now a list of lines defined by the coordinates ((x1, y1), (x2, y2))
        """
        image=self.get_data_values("image")
        # 1. get normalized intensity profile
        #norm_intensity_profile = get_norm_intensity_profile(image)
        norm_intensity_data = get_norm_intensity_matrix(image)

        # 3. get centers' locations
        max_intensity_region_table = get_max_intensity_region_table(image)

        # 4. get intensity profiles
        intensity_plot_data = get_intensity_plot(image)

        # 5. get profiles statistics
        profile_stat_table = get_profile_statistics_table(image)

        # We append the dataframe into the output
        self.output.append(
            model.Table(
                name="max_intensity_region_table",
                description="Dataframe containing coordinates",
                table=max_intensity_region_table,
            )
        )

        self.output.append(
            model.Table(
                name="norm_intensity_data",
                description="Dataframe containing coordinates",
                table=norm_intensity_data,
            )
        )

        self.output.append(
            model.Table(
                name="intensity_plot_data",
                description="Dataframe containing coordinates",
                table=intensity_plot_data,
            )
        )

        self.output.append(
            model.Table(
                name="profile_stat_table",
                description="Dataframe containing coordinates",
                table=profile_stat_table,
            )
        )



        # And that's about it. Don't forget to return True at the end
        return True
