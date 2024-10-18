# run pytest with --hypothesis-profile=dev to load a profile
from datetime import datetime

import pytest
from pathlib import Path
from hypothesis import HealthCheck, Verbosity, settings
from microscopemetrics_schema import datamodel as mm_schema
from linkml_runtime.loaders.yaml_loader import YAMLLoader

settings.register_profile(
    "push",
    max_examples=1,
    suppress_health_check=[
        HealthCheck.too_slow,
        HealthCheck.large_base_example,
        HealthCheck.data_too_large,
    ],
    deadline=100000,
)
settings.register_profile(
    "pull_request",
    max_examples=50,
    suppress_health_check=[
        HealthCheck.too_slow,
        HealthCheck.large_base_example,
        HealthCheck.data_too_large,
    ],
    deadline=100000,
)
settings.register_profile(
    "pre_release",
    max_examples=100,
    suppress_health_check=[
        HealthCheck.too_slow,
        HealthCheck.large_base_example,
        HealthCheck.data_too_large,
    ],
    deadline=100000,
)
settings.register_profile(
    "dev",
    max_examples=1,
    suppress_health_check=[
        HealthCheck.too_slow,
        HealthCheck.large_base_example,
        HealthCheck.data_too_large,
    ],
    deadline=100000,
    verbosity=Verbosity.verbose,
    print_blob=True,
)
settings.register_profile(
    "debug",
    max_examples=10,
    suppress_health_check=[
        HealthCheck.too_slow,
        HealthCheck.large_base_example,
        HealthCheck.data_too_large,
    ],
    deadline=100000,
    verbosity=Verbosity.verbose,
    print_blob=True,
)


def _load_schema(loader: YAMLLoader, target_class: mm_schema.MetricsObject, path: Path, depth=3) -> mm_schema.MetricsObject:
    if not path.exists():
        raise FileNotFoundError(f"File {path} not found")

    class_name = target_class.class_name.lower()
    file_path = path / f"{class_name}.yaml"
    if file_path.is_file():
        return loader.load_any(
            source=str(file_path),
            target_class=target_class
        )
    if depth == 0:
        raise FileNotFoundError(f"File {file_path} not found")
    return _load_schema(loader, target_class, path.parent, depth=depth-1)


def _load_data_schema(loader: YAMLLoader, target_class: mm_schema.MetricsInputData, path: Path) -> mm_schema.MetricsInputData:
    return None


def _dataset_from_dir(
        loader: YAMLLoader,
        target_class,
        path: Path
) -> mm_schema.MetricsDataset:
    input_parameters_mappings = {
        mm_schema.FieldIlluminationDataset: mm_schema.FieldIlluminationInputParameters,
        mm_schema.PSFBeadsDataset: mm_schema.PSFBeadsInputParameters,
    }
    input_data_mappings = {
        mm_schema.FieldIlluminationDataset: mm_schema.FieldIlluminationInputData,
        mm_schema.PSFBeadsDataset: mm_schema.PSFBeadsInputData,
    }
    input_data = input_data_mappings[target_class]
    return target_class(
        name=path.name,
        microscope=_load_schema(loader, mm_schema.Microscope, path),
        sample=_load_schema(loader, mm_schema.Sample, path),
        experimenter=_load_schema(loader, mm_schema.Experimenter, path),
        acquisition_datetime=datetime.now(),
        input_parameters=_load_schema(
            loader, input_parameters_mappings[target_class], path
        ),
        input_data=_load_data_schema(loader, target_class, path),
        processed=False,
    )


@pytest.fixture(scope="session")
def get_datasets(target_class, data_path: str):
    """A generator fixture to get all datasets in a directory"""
    loader = YAMLLoader()
    data_path = Path(data_path)
    for path in data_path.iterdir():
        if path.is_dir():
            yield _dataset_from_dir(loader, target_class, path)
        else:
            continue
