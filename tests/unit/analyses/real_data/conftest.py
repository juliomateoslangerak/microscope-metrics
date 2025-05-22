"""
This file contains fixtures to create various invariable schema dataclasses for testing purposes.
"""

import datetime
import pathlib
import warnings

import imageio.v3 as iio
import microscopemetrics_schema.datamodel as mm_schema
import pytest
from linkml_runtime.dumpers import YAMLDumper
from linkml_runtime.loaders import YAMLLoader

from microscopemetrics.analyses import mappings, numpy_to_mm_image


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


def generate_missing_key_measurements(
    dataset: mm_schema.MetricsDataset,
) -> mm_schema.KeyMeasurements:
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


def build_dataset_from_dir(
    dataset_dir,
    microscope,
    experimenter,
    acquisition_datetime,
    input_parameters_target_class,
    input_data_target_class,
    input_images_field,
    output_target_class,
    key_measurements_target_class,
    dataset_target_class,
    do_generate_missing_input_parameters,
    do_generate_missing_key_measurements,
):
    loader = YAMLLoader()
    images = []
    dataset_input_parameters = None
    dataset_sample = None
    dataset_key_measurements = None

    for data_file in dataset_dir.iterdir():
        if not data_file.is_file():
            continue
        if data_file.suffix in [".tif", ".tiff"]:
            array = iio.imread(data_file)
            # We are assuming images here of an order zyx
            if len(array.shape) == 3 and array.shape[0] < array.shape[1]:
                array = array.reshape((1, array.shape[0], array.shape[1], array.shape[2], 1))
            else:
                raise ValueError(
                    f"Image {data_file} has an unexpected shape {array.shape}. Expected 3D image with zyx order."
                )
            images.append(
                numpy_to_mm_image(
                    array=array,
                    name=data_file.name[: -len(data_file.suffix)],
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

    if dataset_input_parameters is None:
        dataset_input_parameters = input_parameters_target_class()
        if do_generate_missing_input_parameters:
            warnings.warn(f"No input parameters found in {dataset_dir}. Generating defaults.")
            dumper = YAMLDumper()
            dumper.dump(
                dataset_input_parameters, str(dataset_dir / "dataset_input_parameters.yaml")
            )

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
            warnings.warn(f"Generating default key_measurements.")
            dataset_key_measurements = generate_missing_key_measurements(dataset)
            dataset.output.key_measurements = dataset_key_measurements
            dumper = YAMLDumper()
            dumper.dump(
                dataset_key_measurements, str(dataset_dir / "dataset_key_measurements.yaml")
            )
        else:
            raise ValueError(f"No key measurements found in {dataset_dir}")

    return dataset


@pytest.fixture
def dataset_tested(
    dataset_dir,
    microscope,
    experimenter,
    acquisition_datetime,
    request,
):
    params = request.param
    return build_dataset_from_dir(
        dataset_dir=dataset_dir,
        microscope=microscope,
        experimenter=experimenter,
        acquisition_datetime=acquisition_datetime,
        input_parameters_target_class=params["input_parameters_target_class"],
        input_data_target_class=params["input_data_target_class"],
        input_images_field=params["input_images_field"],
        output_target_class=params["output_target_class"],
        key_measurements_target_class=params["key_measurements_target_class"],
        dataset_target_class=params["dataset_target_class"],
        do_generate_missing_input_parameters=params["do_generate_missing_input_parameters"],
        do_generate_missing_key_measurements=params["do_generate_missing_key_measurements"],
    )


def pytest_generate_tests(metafunc):
    if "dataset_dir" in metafunc.fixturenames:
        data_root = (
            pathlib.Path(__file__).parent.parent.parent.parent / "data" / "psf_beads_datasets"
        )
        dataset_dirs = [p for p in data_root.iterdir() if p.is_dir() and not p.name.startswith("_")]
        metafunc.parametrize("dataset_dir", dataset_dirs)
