"""
This file contains fixtures to create various invariable schema dataclasses for testing purposes.
"""
import pytest

import pathlib
import numpy as np
from skimage import io
import microscopemetrics_schema.datamodel as mm_schema
import datetime

from linkml_runtime.loaders import YAMLLoader

from microscopemetrics.analyses import numpy_to_mm_image


@pytest.fixture(scope="session")
def microscope() -> mm_schema.Microscope:
    return mm_schema.Microscope(
        name="microscope_name",
        description="microscope_description",
        type="WIDEFIELD",
        manufacturer="microscope_manufacturer",
        model="microscope_model",
        serial_number="microscope_serial_number",
    )


@pytest.fixture(scope="session")
def experimenter() -> mm_schema.Experimenter:
    return mm_schema.Experimenter(
        name="John Doe",
        orcid="0123-4567-8901-2345",
    )


@pytest.fixture(scope="session")
def acquisition_datetime() -> str:
    return str(datetime.datetime.now())


@pytest.fixture
def images_dataset_generator(
    microscope,
    experimenter,
    acquisition_datetime,
    request,
):

    params = request.param  # Expecting a dictionary
    dataset_path =  \
        pathlib.Path(__file__).parent.parent.parent.parent / "data" / params["dataset_path"]
    dataset_target_class = params["dataset_target_class"]
    input_parameters_target_class = params["input_parameters_target_class"]
    input_data_target_class = params["input_data_target_class"]
    input_images_field = params["input_images_field"]
    key_measurements_target_class = params["key_measurements_target_class"]
    output_target_class = params["output_target_class"]

    loader = YAMLLoader()
    for data_dir in dataset_path.iterdir():
        images = []
        dataset_input_parameters = None
        dataset_key_measurements = None

        if not data_dir.is_dir():
            continue
        for data_file in data_dir.iterdir():
            if not data_file.is_file():
                continue
            if data_file.suffix == ".npy":
                images.append(
                    numpy_to_mm_image(
                        array=np.load(data_file),
                        name=data_file.name[:-len(data_file.suffix)],
                        description=f"test_description for image {len(images)}",
                    )
                )
            elif data_file.suffix == ".tif" or data_file.suffix == ".tiff":
                im = io.imread(data_file)
                # We are assuming for the moment czyx and we need to convert
                # to tzyxc
                if im.ndim == 4:
                    im = np.expand_dims(im, axis=0)

                images.append(
                    numpy_to_mm_image(
                        array=im,
                        name=data_file.name[:-len(data_file.suffix)],
                        description=f"test_description for image {len(images)}",
                    )
                )
            elif (
                data_file.name == "dataset_input_parameters.yaml"
                or data_file.name == "dataset_input_parameters.yml"
            ):
                dataset_input_parameters = loader.load_any(
                    source=str(data_file),
                    target_class=input_parameters_target_class,
                )
            elif (
                data_file.name == "dataset_key_measurements.yaml"
                or data_file.name == "dataset_key_measurements.yml"
            ):
                dataset_key_measurements = loader.load_any(
                    source=str(data_file),
                    target_class=key_measurements_target_class,
                )
            else:
                continue

        if dataset_input_parameters is None:
            # if no input parameters are present in the dataset directory we use defaults
            dataset_input_parameters = input_parameters_target_class()

        if dataset_key_measurements is None:
            raise ValueError("No key measurements found in the dataset directory")

        expected_data = dataset_target_class(
            microscope=microscope,
            experimenter=experimenter.orcid,
            acquisition_datetime=acquisition_datetime,
            input_parameters=dataset_input_parameters,
            input_data=input_data_target_class(**{input_images_field: images}),
            output=output_target_class(
                key_measurements=dataset_key_measurements,
                processing_application="microscopemetrics",
                processing_version="0.0.1",
                processing_datetime=str(datetime.datetime.now()),
            ),
        )

        yield expected_data














