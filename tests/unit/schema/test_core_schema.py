from typing import List

import pytest
from linkml_runtime.dumpers import YAMLDumper
from linkml_runtime.loaders import YAMLLoader

from microscopemetrics.data_schema import core_schema


@pytest.fixture
def experimenter_1_fixture():
    return core_schema.Experimenter(name="name_experimenter_1", orcid="0000-0000-0000-0001")


@pytest.fixture
def experimenter_2_fixture():
    return core_schema.Experimenter(name="name_experimenter_2", orcid="0000-0000-0000-0002")


@pytest.fixture
def protocol_fixture(experimenter_1_fixture, experimenter_2_fixture):
    return core_schema.Protocol(
        name="Protocol001",
        description="A test protocol",
        version="1.0.0",
        authors=[experimenter_1_fixture.orcid, experimenter_2_fixture.orcid],
        url="https://example.com/protocol001",
    )


@pytest.fixture
def sample_fixture(protocol_fixture):
    return core_schema.Sample(
        name="Sample001",
        description="A test sample",
        type="FieldIllumination",
        protocol=protocol_fixture,
    )


@pytest.fixture
def metrics_dataset_fixture(sample_fixture, experimenter_1_fixture):
    return core_schema.MetricsDataset(
        name="MetricsDataset001",
        description="A test metrics dataset",
        sample=sample_fixture.type,
        experimenter=experimenter_1_fixture.orcid,
        acquisition_date="2021-01-01",
        processed=True,
        processing_date="2021-01-02",
        processing_log="A test processing log",
    )


def test_experimenter_creation(experimenter_1_fixture):
    experimenter = core_schema.Experimenter(
        name=experimenter_1_fixture.name, orcid=experimenter_1_fixture.orcid
    )

    assert experimenter == experimenter_1_fixture


def test_experimenter_attributes_required():
    # Test that required attributes are indeed required
    with pytest.raises(ValueError):
        # name is a required attribute, so this should raise an exception
        experimenter = core_schema.Experimenter(orcid="0000-0000-0000-0001")


def test_experimenter_attribute_types(experimenter_1_fixture):
    # Check the types of the attributes
    assert isinstance(experimenter_1_fixture.name, str)
    assert isinstance(experimenter_1_fixture.orcid, str)


def test_experimenter_attribute_values(experimenter_1_fixture):
    # Check if the orcid is a valid orcid
    assert len(experimenter_1_fixture.orcid) == 19


def test_experimenter_validity(experimenter_1_fixture):
    # For the moment, we'll just check if the experimenter can be dumped to YAML and reloaded
    dumper = YAMLDumper()
    loader = YAMLLoader()
    yaml_string = dumper.dumps(experimenter_1_fixture)
    loaded_experimenter = loader.loads(yaml_string, target_class=core_schema.Experimenter)

    assert experimenter_1_fixture == loaded_experimenter


def test_protocol_creation(protocol_fixture):
    protocol = core_schema.Protocol(
        name=protocol_fixture.name,
        description=protocol_fixture.description,
        version=protocol_fixture.version,
        authors=protocol_fixture.authors,
        url=protocol_fixture.url,
    )

    assert protocol == protocol_fixture


def test_protocol_attributes_required():
    # Test that required attributes are indeed required
    with pytest.raises(ValueError):
        # Version and url are required attributes, so this should raise an exception
        protocol = core_schema.Protocol(
            name="protocol", description="A test protocol", url="https://example.com/protocol001"
        )
        protocol = core_schema.Protocol(
            name="protocol", description="A test protocol", version="1.0.0"
        )


def test_protocol_attribute_types(protocol_fixture):
    # Check the types of the attributes
    assert isinstance(protocol_fixture.name, str)
    assert isinstance(protocol_fixture.description, str)
    assert isinstance(protocol_fixture.version, str)
    assert isinstance(protocol_fixture.authors, list)
    assert isinstance(protocol_fixture.url, str)


def test_protocol_attribute_values(protocol_fixture):
    class NotAString:
        def __str__(self):
            pass

    not_a_string = NotAString()

    # Check the values of the attributes
    with pytest.raises(TypeError):
        # Version is restricted to a number of permissible values
        protocol = core_schema.Protocol(
            name="protocol",
            description="A test protocol",
            url="https://example.com/protocol001",
            version=not_a_string,
        )


def test_protocol_validity(protocol_fixture):
    # For the moment, we'll just check if the protocol can be dumped to YAML and reloaded
    dumper = YAMLDumper()
    loader = YAMLLoader()
    yaml_string = dumper.dumps(protocol_fixture)
    loaded_protocol = loader.loads(yaml_string, target_class=core_schema.Protocol)

    assert protocol_fixture == loaded_protocol


def test_sample_creation(sample_fixture):
    sample = core_schema.Sample(
        name=sample_fixture.name,
        description=sample_fixture.description,
        type=sample_fixture.type,
        protocol=sample_fixture.protocol,
    )

    assert sample == sample_fixture


def test_sample_attributes_required(protocol_fixture):
    # Test that required attributes are indeed required
    with pytest.raises(ValueError):
        # Type and protocol are required attributes, so this should raise an exception
        sample = core_schema.Sample(description="A test sample", protocol=protocol_fixture)
        sample = core_schema.Sample(description="A test sample", type="FieldIllumination")


def test_sample_attribute_types(sample_fixture):
    # Check the types of the attributes
    assert isinstance(sample_fixture.name, str)
    assert isinstance(sample_fixture.description, str)
    assert isinstance(sample_fixture.type, str)
    assert isinstance(sample_fixture.protocol, core_schema.Protocol)


def test_sample_attribute_values(sample_fixture):
    # Check the values of the attributes
    with pytest.raises(ValueError):
        # Type is restricted to a number of permissible values
        sample = core_schema.Sample(description="A test sample", type="UnknownType")


def test_sample_validity(sample_fixture):
    # For the moment, we'll just check if the sample can be dumped to YAML and reloaded
    dumper = YAMLDumper()
    loader = YAMLLoader()
    yaml_string = dumper.dumps(sample_fixture)
    loaded_sample = loader.loads(yaml_string, core_schema.Sample)

    assert sample_fixture == loaded_sample


def test_metrics_dataset_creation(metrics_dataset_fixture):
    metrics_dataset = core_schema.MetricsDataset(
        name=metrics_dataset_fixture.name,
        description=metrics_dataset_fixture.description,
        sample=metrics_dataset_fixture.sample,
        experimenter=metrics_dataset_fixture.experimenter,
        acquisition_date=metrics_dataset_fixture.acquisition_date,
        processed=metrics_dataset_fixture.processed,
        processing_date=metrics_dataset_fixture.processing_date,
        processing_log=metrics_dataset_fixture.processing_log,
    )

    assert metrics_dataset == metrics_dataset_fixture


def test_metrics_dataset_attributes_required(metrics_dataset_fixture, experimenter_1_fixture):
    # Test that required attributes are indeed required
    # Processed is a required attribute but there is a default value provided
    pass


def test_metrics_dataset_attribute_types(metrics_dataset_fixture):
    # Check the types of the attributes
    assert isinstance(metrics_dataset_fixture.name, str)
    assert isinstance(metrics_dataset_fixture.description, str)
    assert isinstance(metrics_dataset_fixture.sample, str)
    assert isinstance(metrics_dataset_fixture.experimenter, list)
    assert isinstance(metrics_dataset_fixture.acquisition_date, str)
    assert isinstance(metrics_dataset_fixture.processed, bool)
    assert isinstance(metrics_dataset_fixture.processing_date, str)
    assert isinstance(metrics_dataset_fixture.processing_log, str)


def test_metrics_dataset_attribute_values(metrics_dataset_fixture):
    # Check the values of the attributes
    with pytest.raises(ValueError):
        # Processed is restricted to a number of permissible values
        metrics_dataset = core_schema.MetricsDataset(
            name="metrics_dataset",
            description="A test metrics dataset",
            sample="sample",
            experimenter="experimenter",
            acquisition_date="2021-01-01",
            processed="Unknown",
        )


def test_metrics_dataset_validity(metrics_dataset_fixture):
    # For the moment, we'll just check if the metrics dataset can be dumped to YAML and reloaded
    dumper = YAMLDumper()
    loader = YAMLLoader()
    yaml_string = dumper.dumps(metrics_dataset_fixture)
    loaded_metrics_dataset = loader.loads(yaml_string, core_schema.MetricsDataset)

    assert metrics_dataset_fixture == loaded_metrics_dataset
