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


def test_experimenter_creation(experimenter_1_fixture):
    experimenter = experimenter_1_fixture

    # Check if the attributes were set correctly
    assert experimenter.name == experimenter_1_fixture.name
    assert experimenter.orcid == experimenter_1_fixture.orcid


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
    assert isinstance(sample_fixture.type, core_schema.SampleType)
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


from pandas import DataFrame
from pydantic import ValidationError


@pytest.fixture
def empty_input_dataset():
    class Dataset(model.MetricsDataset):
        def __init__(self):
            super().__init__()

    metrics_dataset = Dataset()
    return metrics_dataset


@pytest.fixture
def filled_input_dataset():
    class Dataset(model.MetricsDataset):
        def __init__(self):
            super().__init__()

    metrics_dataset = Dataset()
    metrics_dataset.add_data_requirement(
        name="some_data",
        description="the description of some data",
        data_type=List[list],
        optional=False,
        replace=False,
    )
    metrics_dataset.add_metadata_requirement(
        name="pixel_size",
        description="Well you bet how big this is...",
        data_type=List[float],
        optional=False,
    )
    metrics_dataset.add_metadata_requirement(
        name="wavelength",
        description="Well you bet what color this is...",
        data_type=float,
        optional=True,
    )

    return metrics_dataset


@pytest.fixture
def metrics_output():
    metrics_output = model.MetricsOutput(description="Test_output")

    shapes = [
        model.Point(x=5, y=5),
        model.Line(x1=5, y1=5, x2=12, y2=12),
        model.Rectangle(x=5, y=5, h=12, w=12),
        model.Ellipse(x=5, y=5, x_rad=12, y_rad=12),
        model.Polygon(points=[(5, 5), (12, 12), (9, 9)]),
    ]

    roi = model.Roi(shapes=shapes, name="roi_name", description="roi_description")
    metrics_output.append(roi)

    tag1 = model.Tag(tag_value="test_tag1", name="tag1_name", description="tag1_description")
    metrics_output.append(tag1)

    tag2 = model.Tag(tag_value="test_tag2", name="tag2_name", description="tag2_description")
    metrics_output.append(tag2)

    key_values = model.KeyValues(
        key_values={"key": 42},
        name="key_value_name",
        description="key_value_description",
    )
    metrics_output.append(key_values)

    df = DataFrame.from_dict({"col_1": [3, 2, 1, 0], "col_2": ["a", "b", "c", "d"]})
    table = model.Table(table=df, name="table_name", description="table_description")
    metrics_output.append(table)

    comment = model.Comment(
        comment="A beautiful image",
        name="comment_name",
        description="comment_description",
    )
    metrics_output.append(comment)

    return metrics_output


def test_constructor_MetricsDataset():
    metrics_dataset = model.MetricsDataset()
    assert isinstance(metrics_dataset, model.MetricsDataset)


def test_set_get_input_data(empty_input_dataset):
    empty_input_dataset.data = 5
    assert empty_input_dataset.data == 5
    empty_input_dataset.data = 42
    assert empty_input_dataset.data == 42


def test_add_remove_input_metadata_requirements(empty_input_dataset):
    empty_input_dataset.add_metadata_requirement(
        name="pixel_size",
        description="Well you bet what this is...",
        data_type=List[float],
        optional=False,
    )
    assert empty_input_dataset.get_metadata_values("pixel_size") is None
    assert empty_input_dataset.metadata["pixel_size"].description == "Well you bet what this is..."
    assert empty_input_dataset.metadata["pixel_size"].__fields__["value"].outer_type_ == List[float]
    assert empty_input_dataset.metadata["pixel_size"] is empty_input_dataset.pixel_size
    assert not empty_input_dataset.metadata["pixel_size"].optional
    empty_input_dataset.remove_metadata_requirement("pixel_size")
    assert len(empty_input_dataset.metadata) == 0


def test_set_get_del(filled_input_dataset):
    filled_input_dataset.set_data_values("some_data", [[1, 2, 3], [4, 5, 6]])
    assert filled_input_dataset.get_data_values("some_data") == [[1, 2, 3], [4, 5, 6]]
    filled_input_dataset.set_data_values("some_data", [[1, 2, 3], [4, 5, 8]])
    assert filled_input_dataset.get_data_values("some_data") == [[1, 2, 3], [4, 5, 8]]
    with pytest.raises(ValidationError):
        filled_input_dataset.set_data_values("some_data", [[1, 2, 3], 3])

    filled_input_dataset.set_metadata_values("pixel_size", [0.2, 0.2, 0.5])
    assert filled_input_dataset.get_metadata_values("pixel_size") == [0.2, 0.2, 0.5]
    filled_input_dataset.set_metadata_values("pixel_size", [0.2, 0.2, 2])
    assert filled_input_dataset.get_metadata_values("pixel_size") == [0.2, 0.2, 2]
    with pytest.raises(ValidationError):
        filled_input_dataset.set_metadata_values("pixel_size", [0.2, 0.2, "not"])

    filled_input_dataset.set_metadata_values("wavelength", 488)
    assert filled_input_dataset.get_metadata_values("wavelength") == 488.0
    filled_input_dataset.set_metadata_values("wavelength", 488.7)
    assert filled_input_dataset.get_metadata_values("wavelength") == 488.7
    with pytest.raises(ValidationError):
        filled_input_dataset.set_metadata_values("wavelength", "blue")
    filled_input_dataset.del_metadata_values("wavelength")
    assert filled_input_dataset.get_metadata_values("wavelength") is None


def test_describe_requirements(filled_input_dataset):
    description = filled_input_dataset.describe_requirements()
    assert description == (
        "DATA requirements:\n"
        "\n"
        "----------\n"
        "Name: some_data\n"
        "Description: the description of some data\n"
        "Optional: False\n"
        "----------\n"
        "\n"
        "METADATA requirements:\n"
        "\n"
        "----------\n"
        "Name: pixel_size\n"
        "Description: Well you bet how big this is...\n"
        "Optional: False\n"
        "Units: None\n"
        "Default: None\n"
        "----------\n"
        "Name: wavelength\n"
        "Description: Well you bet what color this is...\n"
        "Optional: True\n"
        "Units: None\n"
        "Default: None\n"
        "----------"
    )


def test_constructor_MetricsOutput():
    metrics_output = model.MetricsOutput("This is a description")
    assert isinstance(metrics_output, model.MetricsOutput)


def test_constructor_Roi():
    point = model.Point(5, 5)
    roi = model.Roi(shapes=[point], name="ROI", description="This is an important object")
    assert isinstance(roi, model.Roi)


def test_constructor_Tag():
    tag = model.Tag(tag_value="test_tag", name="123", description="This is an important tag")
    assert isinstance(tag, model.Tag)


def test_constructor_KeyValues():
    key_values = model.KeyValues(
        key_values={"a_key": 42}, name="a_name", description="Important keys and values"
    )
    assert isinstance(key_values, model.KeyValues)


def test_constructor_Table():
    df = DataFrame()
    table = model.Table(table=df, name="Table", description="Description of content")
    assert isinstance(table, model.Table)
    with pytest.raises(ValidationError):
        table = model.Table(table=5, name="WrongTable", description="Not a table")


# TODO: replace this with a log
def test_constructor_Comment():
    comment = model.Comment(comment="A beautiful image", name="This is a comment", description="")
    assert isinstance(comment, model.Comment)


def test_reading_metrics_output(metrics_output):

    assert isinstance(metrics_output.get_property("key_value_name"), model.KeyValues)

    assert len(metrics_output.get_tags()) == 2
    metrics_output.delete("tag2_name")
    assert len(metrics_output.get_tags()) == 1
    tag2 = model.Tag(tag_value="test_tag2", name="tag2_name", description="tag2_description")
    metrics_output.append(tag2)
    assert len(metrics_output.get_tags()) == 2
    tag_list = [
        model.Tag(tag_value="test_tag3", name="tag3_name", description="tag3_description"),
        model.Tag(tag_value="test_tag4", name="tag4_name", description="tag4_description"),
    ]
    metrics_output.extend(tag_list)
    assert len(metrics_output.get_tags()) == 4

    assert (
        f"{metrics_output.get_tags()[3].describe()}"
        == "Name: tag4_name\nType: Tag\nDescription: tag4_description"
    )

    assert len(metrics_output.get_images()) == 0
    assert len(metrics_output.get_rois()) == 1
    assert len(metrics_output.get_tags()) == 4
    assert len(metrics_output.get_key_values()) == 1
    assert len(metrics_output.get_tables()) == 1
    assert len(metrics_output.get_comments()) == 1


def test_reading_output_properties(metrics_output):
    pass
