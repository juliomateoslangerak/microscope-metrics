import numpy as np
import pytest
import pathlib

from linkml_runtime.loaders import YAMLLoader

from microscopemetrics.analyses import numpy_to_mm_image
from microscopemetrics.analyses.field_illumination import analyse_field_illumination
from .fixtures import *
from microscopemetrics_schema.datamodel import (
    FieldIlluminationDataset,
    FieldIlluminationInputParameters,
    FieldIlluminationInputData,
    FieldIlluminationOutput,
    Image
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
):

    loader = YAMLLoader()
    for data_dir in data_path.iterdir():
        images = []
        expected_data = None
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
            elif data_file.suffix == ".yaml" or data_file.suffix == ".yml":
                expected_data = loader.load_any(
                    source=data_file,
                    target_class=FieldIlluminationDataset,
                )
            else:
                continue

            if expected_data is None:
                expected_data = FieldIlluminationDataset(
                    microscope=microscope,
                    experimenter=experimenter.orcid,
                    acquisition_datetime=acquisition_datetime,
                    input_parameters=field_illumination_input_parameters,
                    input_data=FieldIlluminationInputData(
                        field_illumination_image=images),
                )
            else:
                expected_data.input_data.field_illumination_image = images

            yield expected_data


@pytest.mark.real_data
def test_field_illumination(
    field_illumination_dataset,
):
    expected_output = field_illumination_dataset.output
    field_illumination_dataset.output = None
    assert analyse_field_illumination(field_illumination_dataset)
    assert field_illumination_dataset.processed



