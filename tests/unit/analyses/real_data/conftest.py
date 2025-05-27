"""
This file contains fixtures to create various invariable schema dataclasses for testing purposes.
"""

import datetime
import pathlib
import warnings

import imageio.v3 as iio
import microscopemetrics_schema.datamodel as mm_schema
import numpy as np
import pytest
from linkml_runtime.dumpers import YAMLDumper
from linkml_runtime.loaders import YAMLLoader

from microscopemetrics.analyses import mappings, numpy_to_mm_image


def gen_microscope() -> mm_schema.Microscope:
    return mm_schema.Microscope(
        name="microscope_name",
        description="microscope_description",
        microscope_type="WIDEFIELD",
        manufacturer="microscope_manufacturer",
        model="microscope_model",
        serial_number="microscope_serial_number",
    )


def gen_sample() -> mm_schema.Sample:
    return mm_schema.Sample(
        name="sample_name",
        description="sample_description",
        manufacturer="sample_manufacturer",
        preparation_protocol="https://example.com/preparation_protocol",
    )


def gen_experimenter() -> mm_schema.Experimenter:
    return mm_schema.Experimenter(
        name="John Doe",
        orcid="0123-4567-8901-2345",
    )


def gen_acquisition_datetime() -> str:
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

    raise ValueError(f"No analysis function found for the {dataset.class_name} dataset type.")


def build_dataset_from_dir(
    dataset_dir,
    dataset_target_class,
    input_parameters_target_class,
    input_data_target_class,
    output_target_class,
    key_measurements_target_class,
    sample_target_class=None,
    microscope=None,
    experimenter=None,
    input_images_field=None,
    acquisition_datetime=None,
    do_generate_missing_input_parameters=False,
    do_generate_missing_key_measurements=False,
):
    loader = YAMLLoader()
    images = []
    input_parameters = None
    sample = None
    key_measurements = None

    for data_file in dataset_dir.iterdir():
        if not data_file.is_file():
            continue
        if data_file.suffix in [".tif", ".tiff"]:
            array = iio.imread(data_file)
            # We are assuming images here of an order zyx
            if len(array.shape) == 3:
                array = np.expand_dims(array, (0, -1))
                if array.shape[1] > array.shape[2]:
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
            input_parameters = loader.load_any(
                source=str(data_file),
                target_class=input_parameters_target_class,
            )
        elif data_file.name in [
            "dataset_key_measurements.yaml",
            "dataset_key_measurements.yml",
        ]:
            key_measurements = loader.load_any(
                source=str(data_file),
                target_class=key_measurements_target_class,
            )
        elif data_file.name in ["dataset_microscope.yaml", "dataset_microscope.yml"]:
            if microscope is None:
                microscope = loader.load_any(
                    source=str(data_file),
                    target_class=mm_schema.Microscope,
                )
        elif data_file.name in ["dataset_sample.yaml", "dataset_sample.yml"]:
            if sample_target_class is not None:
                sample = loader.load_any(
                    source=str(data_file),
                    target_class=sample_target_class,
                )

    if input_parameters is None:
        input_parameters = input_parameters_target_class()
        if do_generate_missing_input_parameters:
            warnings.warn(f"No input parameters found in {dataset_dir}. Generating defaults.")
            dumper = YAMLDumper()
            dumper.dump(input_parameters, str(dataset_dir / "dataset_input_parameters.yaml"))

    if key_measurements is None:
        key_measurements = key_measurements_target_class()
        if do_generate_missing_key_measurements:
            warnings.warn(f"No key measurements found in {dataset_dir}. Generating defaults.")
            dumper = YAMLDumper()
            dumper.dump(key_measurements, str(dataset_dir / "dataset_key_measurements.yaml"))

    dataset = dataset_target_class(
        microscope=microscope or gen_microscope(),
        experimenter=experimenter or gen_experimenter(),
        acquisition_datetime=acquisition_datetime or gen_acquisition_datetime(),
        sample=sample or gen_sample(),
        input_parameters=input_parameters,
        input_data=input_data_target_class(**{input_images_field: images}),
        output=output_target_class(
            key_measurements=key_measurements,
            processing_application="microscopemetrics",
            processing_version="0.0.1",
            processing_datetime=str(datetime.datetime.now()),
        ),
    )

    if key_measurements is None:
        if do_generate_missing_key_measurements:
            warnings.warn(f"Generating default key_measurements.")
            key_measurements = generate_missing_key_measurements(dataset)
            dataset.output.key_measurements = key_measurements
            dumper = YAMLDumper()
            dumper.dump(key_measurements, str(dataset_dir / "dataset_key_measurements.yaml"))
        else:
            raise ValueError(f"No key measurements found in {dataset_dir}")

    return dataset


def get_test_subdirectories(test_dir):
    """
    Get all subdirectories in the test directory that do not start with an underscore.
    """
    data_root = pathlib.Path(__file__).parent.parent.parent.parent / "data" / test_dir
    return [p for p in data_root.iterdir() if p.is_dir() and not p.name.startswith("_")]
