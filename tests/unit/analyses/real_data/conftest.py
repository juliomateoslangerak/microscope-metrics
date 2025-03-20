"""
This file contains fixtures to create various invariable schema dataclasses for testing purposes.
"""
import pytest

import pathlib
import warnings

import imageio.v3 as iio
import microscopemetrics_schema.datamodel as mm_schema
import datetime

from linkml_runtime.dumpers import YAMLDumper
from linkml_runtime.loaders import YAMLLoader

from microscopemetrics.analyses import numpy_to_mm_image, mappings


@pytest.fixture(scope="session")
def microscope() -> mm_schema.Microscope:
    return mm_schema.Microscope(
        name="microscope_name",
        description="microscope_description",
        microscope_type="WIDEFIELD",
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


def generate_missing_key_measurements(dataset: mm_schema.MetricsDataset) -> mm_schema.KeyMeasurements:
    dataset = analyse_dataset(dataset)
    dataset.output.key_measurements.table_data = None
    return dataset.output.key_measurements


def analyse_dataset(dataset: mm_schema.MetricsDataset):
    mapping = mappings.MAPPINGS
    for m in mapping:
        if isinstance(dataset, m.dataset_class):
            # We are ignoring here the sample class for the moment.
            m.analysis_function(dataset)
            return dataset


@pytest.fixture
def images_dataset_generator(
    microscope,
    experimenter,
    acquisition_datetime,
    request,
):
    # We are naming parameters as "dataset_xxx" when they have to be specified in the dataset directory
    # or otherwise just "xxx" when they are fixed, not relevant for the tests.
    params = request.param  # Expecting a dictionary
    dataset_path =  \
        pathlib.Path(__file__).parent.parent.parent.parent / "data" / params["dataset_path"]
    dataset_target_class = params["dataset_target_class"]
    sample_target_class = params["sample_target_class"]
    input_parameters_target_class = params["input_parameters_target_class"]
    input_data_target_class = params["input_data_target_class"]
    input_images_field = params["input_images_field"]
    key_measurements_target_class = params["key_measurements_target_class"]
    output_target_class = params["output_target_class"]
    do_generate_missing_key_measurements = params["do_generate_missing_key_measurements"]
    do_generate_missing_input_parameters = params["do_generate_missing_input_parameters"]

    loader = YAMLLoader()
    for data_dir in dataset_path.iterdir():
        # For convenience, we can preceed a directory name with "_" to ignore it
        if data_dir.name.startswith("_"):
            continue
        images = []
        dataset_input_parameters = None
        dataset_sample = None
        dataset_key_measurements = None

        if not data_dir.is_dir():
            continue
        for data_file in data_dir.iterdir():
            if not data_file.is_file():
                continue
            if data_file.suffix in [".tif", ".tiff"]:
                images.append(
                    numpy_to_mm_image(
                        array=iio.imread(data_file),
                        name=data_file.name[:-len(data_file.suffix)],
                        description=f"test_description for image {len(images)}",
                    )
                )
            elif data_file.name in [
                "dataset_input_parameters.yaml",
                "dataset_input_parameters.yml",
            ]:
                dataset_input_parameters = loader.load_any(
                    source=str(data_file),
                    target_class=input_parameters_target_class,
                )
            elif data_file.name in [
                "dataset_key_measurements.yaml",
                "dataset_key_measurements.yml",
            ]:
                dataset_key_measurements = loader.load_any(
                    source=str(data_file),
                    target_class=key_measurements_target_class,
                )
            elif data_file.name in ["dataset_microscope.yaml", "dataset_microscope.yml"]:
                microscope = loader.load_any(
                    source=str(data_file),
                    target_class=mm_schema.Microscope,
                )
            else:
                continue

        if dataset_input_parameters is None:
            # if no input parameters are present in the dataset directory we use defaults
            dataset_input_parameters = input_parameters_target_class()
            if do_generate_missing_input_parameters:
                warnings.warn(f"No input parameters found in {data_dir}."
                              f"Generating default input parameters.")
                dumper = YAMLDumper()
                dumper.dump(dataset_input_parameters, str(data_dir / "dataset_input_parameters.yaml"))

        dataset = dataset_target_class(
            microscope=microscope,
            experimenter=experimenter.orcid,
            acquisition_datetime=acquisition_datetime,
            sample=dataset_sample,
            input_parameters=dataset_input_parameters,
            input_data=input_data_target_class(**{input_images_field: images}),
            output=output_target_class(
                key_measurements=dataset_key_measurements,
                processing_application="microscopemetrics",
                processing_version="0.0.1",
                processing_datetime=str(datetime.datetime.now()),
            ),
        )

        if dataset_key_measurements is None:
            if do_generate_missing_key_measurements:
                warnings.warn(f"No key measurements found in {data_dir}."
                              f"Generating default key measurements.")
                dataset_key_measurements = generate_missing_key_measurements(dataset)
                dataset.output.key_measurements = dataset_key_measurements
                dumper = YAMLDumper()
                dumper.dump(dataset_key_measurements, str(data_dir / "dataset_key_measurements.yaml"))
            else:
                raise ValueError(f"No key measurements found in {data_dir}")

        yield dataset

