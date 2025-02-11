from typing import Any, Generator

import numpy as np
import pytest
import pathlib

from linkml_runtime.loaders import YAMLLoader
from dataclasses import asdict

from microscopemetrics.analyses import numpy_to_mm_image
from microscopemetrics.analyses.field_illumination import analyse_field_illumination
from .fixtures import *
from microscopemetrics_schema.datamodel import (
    FieldIlluminationDataset,
    FieldIlluminationInputParameters,
    FieldIlluminationInputData,
    FieldIlluminationOutput,
    Image, FieldIlluminationKeyMeasurements
)


@pytest.fixture
def field_illumination_input_parameters(params=None) -> FieldIlluminationInputParameters:
    if params is None:
        return FieldIlluminationInputParameters()
    return FieldIlluminationInputParameters(**params)


@pytest.fixture
def field_illumination_input_data(images) -> FieldIlluminationInputData:
    return_images = []

    for image in images:
        return_images.append(
            numpy_to_mm_image(
                array=image,
                name="test_image",
                description="test_description",
            )
        )

    return FieldIlluminationInputData(field_illumination_image=images)


@pytest.fixture
def field_illumination_dataset(
    microscope,
    experimenter,
    acquisition_datetime,
    field_illumination_input_parameters,
    data_path=pathlib.Path(__file__).parent.parent.parent.parent / "data" / "field_illumination_datasets"
) -> Generator[FieldIlluminationDataset, Any, None]:

    loader = YAMLLoader()
    for data_dir in data_path.iterdir():
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
                        name="test_image",
                        description="test_description",
                    )
                )
            elif data_file.suffix == ".tif" or data_file.suffix == ".tiff":
                images.append(
                    numpy_to_mm_image(
                        array=np.load(data_file),
                        name="test_image",
                        description="test_description",
                    )
                )
            elif data_file.name == "dataset_input_parameters.yaml" or data_file.name == "dataset_input_parameters.yml":
                dataset_input_parameters = loader.load_any(
                    source=str(data_file),
                    target_class=FieldIlluminationInputParameters,
                )
            elif data_file.name == "dataset_key_measurements.yaml" or data_file.name == "dataset_key_measurements.yml":
                dataset_key_measurements = loader.load_any(
                    source=str(data_file),
                    target_class=FieldIlluminationKeyMeasurements,
                )
            else:
                continue

        if dataset_input_parameters is None:
            # if no input parameters are present in the dataset directory we use defaults
            dataset_input_parameters = FieldIlluminationInputParameters()

        if dataset_key_measurements is None:
            raise ValueError("No key measurements found in the dataset directory")

        expected_data = FieldIlluminationDataset(
            microscope=microscope,
            experimenter=experimenter.orcid,
            acquisition_datetime=acquisition_datetime,
            input_parameters=dataset_input_parameters,
            input_data=FieldIlluminationInputData(
                field_illumination_image=images),
            output=FieldIlluminationOutput(
                key_measurements=dataset_key_measurements,
                processing_application="Automated testing",
                processing_version="0.0.1",
                processing_datetime=str(datetime.datetime.now()),
            )
        )

        yield expected_data


@pytest.mark.real_data
def test_field_illumination(
    field_illumination_dataset,
):
    expected_output = asdict(field_illumination_dataset.output)
    field_illumination_dataset.output = None
    assert analyse_field_illumination(field_illumination_dataset)
    assert field_illumination_dataset.processed

    analyzed_output = asdict(field_illumination_dataset.output)

    analyzed_output = filter_dict(
        expected=expected_output,
        analyzed=analyzed_output,
    )
    expected_output = remove_np_pd_data(expected_output)
    analyzed_output = remove_np_pd_data(analyzed_output)

    assert analyzed_output["key_measurements"] == expected_output["key_measurements"]



