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

# import the types that you may be using
from typing import Tuple

# import anything you will need for your analysis
from pandas import DataFrame
from skimage.transform import probabilistic_hough_line
from scipy.spatial import distance
from math import atan2
from pydantic.color import Color


class DetectLinesAnalysis(
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

        if (
            not self.input.line_length.value
        ):  # We check if the value of the line_length is None
            self.input.line_length.value = 50  # and if it is, we give it a value

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

        # We may add some rois to the output
        shapes = [
            model.Line(
                x1=x1, y1=y1, x2=x2, y2=y2, stroke_color=Color("red")
            )  # With some color
            for (x1, y1), (x2, y2) in lines
        ]
        self.output.append(
            model.Roi(
                name="lines",
                description="lines found using a progressive probabilistic hough transform",
                shapes=shapes,
            )
        )

        # We may create a table with the coordinates...
        lines_df = DataFrame.from_records(
            [(a, b, c, d) for (a, b), (c, d) in lines],
            columns=["x_1", "y_1", "x_2", "y_2"],
        )

        # ... and add some very interesting measurements
        lines_df["length"] = lines_df.apply(
            lambda l: distance.euclidean([l.x_1, l.y_1], [l.x_2, l.y_2]), axis=1
        )
        lines_df["angle"] = lines_df.apply(
            lambda l: atan2(l.x_1 - l.x_2, l.y_1 - l.y_2), axis=1
        )

        # We append the dataframe into the output
        self.output.append(
            model.Table(
                name="lines_table",
                description="Dataframe containing coordinates, length and angle for every line",
                table=lines_df,
            )
        )

        # Lets extract some statistics...
        stats = {
            "mean_length": lines_df.length.mean(),
            "median_length": lines_df.length.median(),
            "std_length": lines_df.length.std(),
            "mean_angle": lines_df.angle.mean(),
            "median_angle": lines_df.angle.median(),
            "std_angle": lines_df.angle.std(),
        }

        # ... and save them as key-value pairs
        self.output.append(
            model.KeyValues(
                name="stats",
                description="Some basic statistics about the lines found",
                key_values=stats,
            )
        )

        # And that's about it. Don't forget to return True at the end
        return True
