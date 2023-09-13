from typing import List

import numpy as np
import pytest
from linkml_runtime.dumpers import YAMLDumper
from linkml_runtime.loaders import YAMLLoader

import microscopemetrics_schema.datamodel as mm_schema
from microscopemetrics.samples import numpy_to_inlined_image, numpy_to_inlined_mask


@pytest.fixture
def experimenter_1_fixture():
    return mm_schema.Experimenter(name="name_experimenter_1", orcid="0000-0000-0000-0001")


@pytest.fixture
def experimenter_2_fixture():
    return mm_schema.Experimenter(name="name_experimenter_2", orcid="0000-0000-0000-0002")


@pytest.fixture
def protocol_fixture(experimenter_1_fixture, experimenter_2_fixture):
    return mm_schema.Protocol(
        name="Protocol001",
        description="A test protocol",
        version="1.0.0",
        authors=[experimenter_1_fixture.orcid, experimenter_2_fixture.orcid],
        url="https://example.com/protocol001",
    )


@pytest.fixture
def sample_fixture(protocol_fixture):
    return mm_schema.Sample(
        name="Sample001",
        description="A test sample",
        type="FieldIllumination",
        protocol=protocol_fixture,
    )


@pytest.fixture
def metrics_dataset_fixture(sample_fixture, experimenter_1_fixture):
    return mm_schema.MetricsDataset(
        name="MetricsDataset001",
        description="A test metrics dataset",
        sample=sample_fixture.type,
        experimenter=experimenter_1_fixture.orcid,
        acquisition_date="2021-01-01",
        processed=True,
        processing_date="2021-01-02",
        processing_log="A test processing log",
    )


@pytest.fixture
def numpy_2d_mask_ndarray_fixture():
    return np.ones((3, 3), dtype=bool)


@pytest.fixture
def numpy_2d_ndarray_fixture():
    return np.ones((3, 3))


@pytest.fixture
def numpy_5d_ndarray_fixture():
    return np.ones((3, 3, 3, 3, 3))


@pytest.fixture
def image_as_numpy_2d_fixture(numpy_2d_ndarray_fixture):
    return mm_schema.ImageAsNumpy(
        name="ImageAsNumpy001",
        description="A test image as numpy",
        image_url="https://example.com/image001",
        source_image_url="https://example.com/source_image002",
        data=numpy_2d_ndarray_fixture,
    )


@pytest.fixture
def image_as_numpy_5d_fixture(numpy_5d_ndarray_fixture):
    return mm_schema.ImageAsNumpy(
        name="ImageAsNumpy001",
        description="A test image as numpy",
        image_url="https://example.com/image001",
        source_image_url="https://example.com/source_image002",
        data=numpy_5d_ndarray_fixture,
    )


@pytest.fixture
def image_mask_fixture(numpy_2d_mask_ndarray_fixture):
    return numpy_to_inlined_mask(
        array=numpy_2d_mask_ndarray_fixture,
        name="ImageMask001",
        description="A test image mask",
        image_url="https://example.com/image001",
        source_image_url="https://example.com/source_image002",
    )


@pytest.fixture
def image_2d_fixture(numpy_2d_ndarray_fixture):
    return numpy_to_inlined_image(
        array=numpy_2d_ndarray_fixture,
        name="Image2D001",
        description="A test image 2D",
        image_url="https://example.com/image001",
        source_image_url="https://example.com/source_image002",
    )


@pytest.fixture
def image_5d_fixture(numpy_5d_ndarray_fixture):
    return numpy_to_inlined_image(
        array=numpy_5d_ndarray_fixture,
        name="Image5D001",
        description="A test image 5D",
        image_url="https://example.com/image001",
        source_image_url="https://example.com/source_image002",
    )


def test_experimenter_creation(experimenter_1_fixture):
    experimenter = mm_schema.Experimenter(
        name=experimenter_1_fixture.name, orcid=experimenter_1_fixture.orcid
    )

    assert experimenter == experimenter_1_fixture


def test_experimenter_attributes_required():
    with pytest.raises(ValueError):
        experimenter = mm_schema.Experimenter(orcid="0000-0000-0000-0001")


def test_experimenter_attribute_types(experimenter_1_fixture):
    assert isinstance(experimenter_1_fixture.name, str)
    assert isinstance(experimenter_1_fixture.orcid, str)


def test_experimenter_attribute_values(experimenter_1_fixture):
    assert len(experimenter_1_fixture.orcid) == 19


def test_experimenter_validity(experimenter_1_fixture):
    # For the moment, we'll just check if the experimenter can be dumped to YAML and reloaded
    dumper = YAMLDumper()
    loader = YAMLLoader()
    yaml_string = dumper.dumps(experimenter_1_fixture)
    loaded_experimenter = loader.loads(yaml_string, target_class=mm_schema.Experimenter)

    assert experimenter_1_fixture == loaded_experimenter


def test_protocol_creation(protocol_fixture):
    protocol = mm_schema.Protocol(
        name=protocol_fixture.name,
        description=protocol_fixture.description,
        version=protocol_fixture.version,
        authors=protocol_fixture.authors,
        url=protocol_fixture.url,
    )

    assert protocol == protocol_fixture


def test_protocol_attributes_required():
    with pytest.raises(ValueError):
        protocol = mm_schema.Protocol(
            name="protocol",
            description="A test protocol",
            url="https://example.com/protocol001",
        )
    with pytest.raises(ValueError):
        protocol = mm_schema.Protocol(
            name="protocol", description="A test protocol", version="1.0.0"
        )


def test_protocol_attribute_types(protocol_fixture):
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

    with pytest.raises(TypeError):
        protocol = mm_schema.Protocol(
            name="protocol",
            description="A test protocol",
            url="https://example.com/protocol001",
            version=not_a_string,
        )


def test_protocol_validity(protocol_fixture):
    dumper = YAMLDumper()
    loader = YAMLLoader()
    yaml_string = dumper.dumps(protocol_fixture)
    loaded_protocol = loader.loads(yaml_string, target_class=mm_schema.Protocol)

    assert protocol_fixture == loaded_protocol


def test_sample_creation(sample_fixture):
    sample = mm_schema.Sample(
        name=sample_fixture.name,
        description=sample_fixture.description,
        type=sample_fixture.type,
        protocol=sample_fixture.protocol,
    )

    assert sample == sample_fixture


def test_sample_attributes_required(protocol_fixture):
    with pytest.raises(ValueError):
        sample = mm_schema.Sample(description="A test sample", protocol=protocol_fixture.url)
    with pytest.raises(ValueError):
        sample = mm_schema.Sample(description="A test sample", type="FieldIllumination")


def test_sample_attribute_types(sample_fixture):
    assert isinstance(sample_fixture.name, str)
    assert isinstance(sample_fixture.description, str)
    assert isinstance(sample_fixture.type, str)
    assert isinstance(sample_fixture.protocol, mm_schema.ProtocolUrl)


def test_sample_attribute_values(sample_fixture):
    with pytest.raises(ValueError):
        # Type is restricted to a number of permissible values
        sample = mm_schema.Sample(description="A test sample", type="UnknownType")


def test_sample_validity(sample_fixture):
    dumper = YAMLDumper()
    loader = YAMLLoader()
    yaml_string = dumper.dumps(sample_fixture)
    loaded_sample = loader.loads(yaml_string, mm_schema.Sample)

    assert sample_fixture == loaded_sample


def test_metrics_dataset_creation(metrics_dataset_fixture):
    metrics_dataset = mm_schema.MetricsDataset(
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
    assert isinstance(metrics_dataset_fixture.name, str)
    assert isinstance(metrics_dataset_fixture.description, str)
    assert isinstance(metrics_dataset_fixture.sample, str)
    assert isinstance(metrics_dataset_fixture.experimenter, list)
    assert isinstance(metrics_dataset_fixture.acquisition_date, str)
    assert isinstance(metrics_dataset_fixture.processed, bool)
    assert isinstance(metrics_dataset_fixture.processing_date, str)
    assert isinstance(metrics_dataset_fixture.processing_log, str)


def test_metrics_dataset_attribute_values(metrics_dataset_fixture):
    with pytest.raises(ValueError):
        # Processed is restricted to a number of permissible values
        metrics_dataset = mm_schema.MetricsDataset(
            name="metrics_dataset",
            description="A test metrics dataset",
            sample="sample",
            experimenter="experimenter",
            acquisition_date="2021-01-01",
            processed="Unknown",
        )


def test_metrics_dataset_validity(metrics_dataset_fixture):
    dumper = YAMLDumper()
    loader = YAMLLoader()
    yaml_string = dumper.dumps(metrics_dataset_fixture)
    loaded_metrics_dataset = loader.loads(yaml_string, mm_schema.MetricsDataset)

    assert metrics_dataset_fixture == loaded_metrics_dataset


def test_image_as_numpy_creation(image_as_numpy_2d_fixture, image_as_numpy_5d_fixture):
    image_as_numpy_2d = mm_schema.ImageAsNumpy(
        name=image_as_numpy_2d_fixture.name,
        description=image_as_numpy_2d_fixture.description,
        image_url=image_as_numpy_2d_fixture.image_url,
        source_image_url=image_as_numpy_2d_fixture.source_image_url,
        data=image_as_numpy_2d_fixture.data,
    )
    image_as_numpy_5d = mm_schema.ImageAsNumpy(
        name=image_as_numpy_5d_fixture.name,
        description=image_as_numpy_5d_fixture.description,
        image_url=image_as_numpy_5d_fixture.image_url,
        source_image_url=image_as_numpy_5d_fixture.source_image_url,
        data=image_as_numpy_5d_fixture.data,
    )

    assert image_as_numpy_2d == image_as_numpy_2d_fixture
    assert image_as_numpy_5d == image_as_numpy_5d_fixture


@pytest.mark.skip(reason="no way of currently testing this")
def test_image_as_numpy_attributes_required():
    with pytest.raises(ValueError):
        # Data is a required attribute, so this should raise an exception but as it
        # is defined as any, it is not possible to check this
        image_as_numpy = mm_schema.ImageAsNumpy(
            name="image_as_numpy",
            description="A test image as numpy",
            image_url="https://example.com/image_as_numpy001",
            source_image_url="https://example.com/image002",
        )


def test_image_as_numpy_attribute_types(image_as_numpy_2d_fixture, image_as_numpy_5d_fixture):
    assert isinstance(image_as_numpy_2d_fixture.name, str)
    assert isinstance(image_as_numpy_2d_fixture.description, str)
    assert isinstance(image_as_numpy_2d_fixture.image_url, str)
    assert isinstance(image_as_numpy_2d_fixture.source_image_url, list)
    assert isinstance(image_as_numpy_2d_fixture.data, np.ndarray)
    assert isinstance(image_as_numpy_5d_fixture.name, str)
    assert isinstance(image_as_numpy_5d_fixture.description, str)
    assert isinstance(image_as_numpy_5d_fixture.image_url, str)
    assert isinstance(image_as_numpy_5d_fixture.source_image_url, list)
    assert isinstance(image_as_numpy_5d_fixture.data, np.ndarray)


@pytest.mark.skip(reason="no way of currently testing this")
def test_image_as_numpy_attribute_values(image_as_numpy_2d_fixture, image_as_numpy_5d_fixture):
    with pytest.raises(ValueError):
        # Data is restricted to a number of permissible values
        image_as_numpy = mm_schema.ImageAsNumpy(
            name="image_as_numpy",
            description="A test image as numpy",
            image_url="https://example.com/image_as_numpy001",
            source_image_url="https://example.com/image002",
            data="Unknown",
        )


@pytest.mark.skip(reason="no way of currently testing this")
def test_image_as_numpy_validity(image_as_numpy_2d_fixture, image_as_numpy_5d_fixture):
    dumper = YAMLDumper()
    loader = YAMLLoader()
    yaml_string = dumper.dumps(image_as_numpy_2d_fixture)
    loaded_image_as_numpy = loader.loads(yaml_string, mm_schema.ImageAsNumpy)

    assert image_as_numpy_2d_fixture == loaded_image_as_numpy

    yaml_string = dumper.dumps(image_as_numpy_5d_fixture)
    loaded_image_as_numpy = loader.loads(yaml_string, mm_schema.ImageAsNumpy)

    assert image_as_numpy_5d_fixture == loaded_image_as_numpy


def test_image_mask_creation(image_mask_fixture):
    image_mask = mm_schema.ImageMask(
        name=image_mask_fixture.name,
        description=image_mask_fixture.description,
        image_url=image_mask_fixture.image_url,
        source_image_url=image_mask_fixture.source_image_url,
        data=image_mask_fixture.data,
        y=image_mask_fixture.y,
        x=image_mask_fixture.x,
    )

    assert image_mask == image_mask_fixture


def test_image_mask_attributes_required(image_mask_fixture):
    with pytest.raises(ValueError):
        image_mask = mm_schema.ImageMask(
            name=image_mask_fixture.name,
            description=image_mask_fixture.description,
            image_url=image_mask_fixture.image_url,
            source_image_url=image_mask_fixture.source_image_url,
            y=image_mask_fixture.y,
            x=image_mask_fixture.x,
        )
    with pytest.raises(ValueError):
        image_mask = mm_schema.ImageMask(
            name=image_mask_fixture.name,
            description=image_mask_fixture.description,
            image_url=image_mask_fixture.image_url,
            source_image_url=image_mask_fixture.source_image_url,
            data=image_mask_fixture.data,
            x=image_mask_fixture.x,
        )
    with pytest.raises(ValueError):
        image_mask = mm_schema.ImageMask(
            name=image_mask_fixture.name,
            description=image_mask_fixture.description,
            image_url=image_mask_fixture.image_url,
            source_image_url=image_mask_fixture.source_image_url,
            data=image_mask_fixture.data,
            y=image_mask_fixture.y,
        )


def test_image_mask_attribute_types(image_mask_fixture):
    assert isinstance(image_mask_fixture.name, str)
    assert isinstance(image_mask_fixture.description, str)
    assert isinstance(image_mask_fixture.image_url, str)
    assert isinstance(image_mask_fixture.source_image_url, list)
    assert isinstance(image_mask_fixture.data, list)
    assert isinstance(image_mask_fixture.y, mm_schema.PixelSeries)
    assert isinstance(image_mask_fixture.x, mm_schema.PixelSeries)


def test_image_mask_attribute_values(image_mask_fixture):
    with pytest.raises(ValueError):
        image_mask = mm_schema.ImageMask(
            name=image_mask_fixture.name,
            description=image_mask_fixture.description,
            image_url=image_mask_fixture.image_url,
            source_image_url=image_mask_fixture.source_image_url,
            data="Unknown",
            y=image_mask_fixture.y,
            x=image_mask_fixture.x,
        )
    with pytest.raises(TypeError):
        # Y must be a PixelSeries
        image_mask = mm_schema.ImageMask(
            name=image_mask_fixture.name,
            description=image_mask_fixture.description,
            image_url=image_mask_fixture.image_url,
            source_image_url=image_mask_fixture.source_image_url,
            data=image_mask_fixture.data,
            y=[2, 3],
            x=image_mask_fixture.x,
        )
    with pytest.raises(TypeError):
        # X must be a PixelSeries
        image_mask = mm_schema.ImageMask(
            name=image_mask_fixture.name,
            description=image_mask_fixture.description,
            image_url=image_mask_fixture.image_url,
            source_image_url=image_mask_fixture.source_image_url,
            data=image_mask_fixture.data,
            y=image_mask_fixture.y,
            x="wrong type",
        )


def test_image_mask_validity(image_mask_fixture):
    dumper = YAMLDumper()
    loader = YAMLLoader()
    yaml_string = dumper.dumps(image_mask_fixture)
    loaded_image_mask = loader.loads(yaml_string, mm_schema.ImageMask)

    assert image_mask_fixture == loaded_image_mask


def test_image_2d_creation(image_2d_fixture):
    image_2d = mm_schema.Image2D(
        name=image_2d_fixture.name,
        description=image_2d_fixture.description,
        image_url=image_2d_fixture.image_url,
        source_image_url=image_2d_fixture.source_image_url,
        data=image_2d_fixture.data,
        y=image_2d_fixture.y,
        x=image_2d_fixture.x,
    )

    assert image_2d == image_2d_fixture


def test_image_2d_attributes_required(image_2d_fixture):
    # no data
    with pytest.raises(ValueError):
        image_2d = mm_schema.Image2D(
            name=image_2d_fixture.name,
            description=image_2d_fixture.description,
            image_url=image_2d_fixture.image_url,
            source_image_url=image_2d_fixture.source_image_url,
            y=image_2d_fixture.y,
            x=image_2d_fixture.x,
        )
    # no y
    with pytest.raises(ValueError):
        image_2d = mm_schema.Image2D(
            name=image_2d_fixture.name,
            description=image_2d_fixture.description,
            image_url=image_2d_fixture.image_url,
            source_image_url=image_2d_fixture.source_image_url,
            data=image_2d_fixture.data,
            x=image_2d_fixture.x,
        )
    # no x
    with pytest.raises(ValueError):
        image_2d = mm_schema.Image2D(
            name=image_2d_fixture.name,
            description=image_2d_fixture.description,
            image_url=image_2d_fixture.image_url,
            source_image_url=image_2d_fixture.source_image_url,
            data=image_2d_fixture.data,
            y=image_2d_fixture.y,
        )


def test_image_2d_attribute_types(image_2d_fixture):
    assert isinstance(image_2d_fixture.name, str)
    assert isinstance(image_2d_fixture.description, str)
    assert isinstance(image_2d_fixture.image_url, str)
    assert isinstance(image_2d_fixture.source_image_url, list)
    assert isinstance(image_2d_fixture.data, list)
    assert isinstance(image_2d_fixture.y, mm_schema.PixelSeries)
    assert isinstance(image_2d_fixture.x, mm_schema.PixelSeries)


def test_image_2d_attribute_values(image_2d_fixture):
    with pytest.raises(ValueError):
        image_2d = mm_schema.Image2D(
            name=image_2d_fixture.name,
            description=image_2d_fixture.description,
            image_url=image_2d_fixture.image_url,
            source_image_url=image_2d_fixture.source_image_url,
            data="Unknown",
            y=image_2d_fixture.y,
            x=image_2d_fixture.x,
        )
    with pytest.raises(TypeError):
        # Y must be a PixelSeries
        image_2d = mm_schema.Image2D(
            name=image_2d_fixture.name,
            description=image_2d_fixture.description,
            image_url=image_2d_fixture.image_url,
            source_image_url=image_2d_fixture.source_image_url,
            data=image_2d_fixture.data,
            y=[2, 3],
            x=image_2d_fixture.x,
        )
    with pytest.raises(TypeError):
        # X must be a PixelSeries
        image_2d = mm_schema.Image2D(
            name=image_2d_fixture.name,
            description=image_2d_fixture.description,
            image_url=image_2d_fixture.image_url,
            source_image_url=image_2d_fixture.source_image_url,
            data=image_2d_fixture.data,
            y=image_2d_fixture.y,
            x="wrong type",
        )


def test_image_2d_validity(image_2d_fixture):
    dumper = YAMLDumper()
    loader = YAMLLoader()
    yaml_string = dumper.dumps(image_2d_fixture)
    loaded_image_2d = loader.loads(yaml_string, mm_schema.Image2D)

    assert image_2d_fixture == loaded_image_2d


def test_image_5d_creation(image_5d_fixture):
    image_5d = mm_schema.Image5D(
        name=image_5d_fixture.name,
        description=image_5d_fixture.description,
        image_url=image_5d_fixture.image_url,
        source_image_url=image_5d_fixture.source_image_url,
        data=image_5d_fixture.data,
        t=image_5d_fixture.t,
        z=image_5d_fixture.z,
        y=image_5d_fixture.y,
        x=image_5d_fixture.x,
        c=image_5d_fixture.c,
    )

    assert image_5d == image_5d_fixture


def test_image_5d_attributes_required(image_5d_fixture):
    # no data
    with pytest.raises(ValueError):
        image_5d = mm_schema.Image5D(
            name=image_5d_fixture.name,
            description=image_5d_fixture.description,
            image_url=image_5d_fixture.image_url,
            source_image_url=image_5d_fixture.source_image_url,
            t=image_5d_fixture.t,
            z=image_5d_fixture.z,
            y=image_5d_fixture.y,
            x=image_5d_fixture.x,
            c=image_5d_fixture.c,
        )
    # no t
    with pytest.raises(ValueError):
        image_5d = mm_schema.Image5D(
            name=image_5d_fixture.name,
            description=image_5d_fixture.description,
            image_url=image_5d_fixture.image_url,
            source_image_url=image_5d_fixture.source_image_url,
            data=image_5d_fixture.data,
            z=image_5d_fixture.z,
            y=image_5d_fixture.y,
            x=image_5d_fixture.x,
            c=image_5d_fixture.c,
        )
    # no z
    with pytest.raises(ValueError):
        image_5d = mm_schema.Image5D(
            name=image_5d_fixture.name,
            description=image_5d_fixture.description,
            image_url=image_5d_fixture.image_url,
            source_image_url=image_5d_fixture.source_image_url,
            data=image_5d_fixture.data,
            t=image_5d_fixture.t,
            y=image_5d_fixture.y,
            x=image_5d_fixture.x,
            c=image_5d_fixture.c,
        )
    # no y
    with pytest.raises(ValueError):
        image_5d = mm_schema.Image5D(
            name=image_5d_fixture.name,
            description=image_5d_fixture.description,
            image_url=image_5d_fixture.image_url,
            source_image_url=image_5d_fixture.source_image_url,
            data=image_5d_fixture.data,
            t=image_5d_fixture.t,
            z=image_5d_fixture.z,
            x=image_5d_fixture.x,
            c=image_5d_fixture.c,
        )
    # no x
    with pytest.raises(ValueError):
        image_5d = mm_schema.Image5D(
            name=image_5d_fixture.name,
            description=image_5d_fixture.description,
            image_url=image_5d_fixture.image_url,
            source_image_url=image_5d_fixture.source_image_url,
            data=image_5d_fixture.data,
            t=image_5d_fixture.t,
            z=image_5d_fixture.z,
            y=image_5d_fixture.y,
            c=image_5d_fixture.c,
        )
    # no c
    with pytest.raises(ValueError):
        image_5d = mm_schema.Image5D(
            name=image_5d_fixture.name,
            description=image_5d_fixture.description,
            image_url=image_5d_fixture.image_url,
            source_image_url=image_5d_fixture.source_image_url,
            data=image_5d_fixture.data,
            t=image_5d_fixture.t,
            z=image_5d_fixture.z,
            y=image_5d_fixture.y,
            x=image_5d_fixture.x,
        )


def test_image_5d_attribute_types(image_5d_fixture):
    assert isinstance(image_5d_fixture.name, str)
    assert isinstance(image_5d_fixture.description, str)
    assert isinstance(image_5d_fixture.image_url, str)
    assert isinstance(image_5d_fixture.source_image_url, list)
    assert isinstance(image_5d_fixture.data, list)
    assert isinstance(image_5d_fixture.t, mm_schema.TimeSeries)
    assert isinstance(image_5d_fixture.z, mm_schema.PixelSeries)
    assert isinstance(image_5d_fixture.y, mm_schema.PixelSeries)
    assert isinstance(image_5d_fixture.x, mm_schema.PixelSeries)
    assert isinstance(image_5d_fixture.c, mm_schema.ChannelSeries)


def test_image_5d_attribute_values(image_5d_fixture):
    with pytest.raises(ValueError):
        image_5d = mm_schema.Image5D(
            name=image_5d_fixture.name,
            description=image_5d_fixture.description,
            image_url=image_5d_fixture.image_url,
            source_image_url=image_5d_fixture.source_image_url,
            data="Unknown",
            t=image_5d_fixture.t,
            z=image_5d_fixture.z,
            y=image_5d_fixture.y,
            x=image_5d_fixture.x,
            c=image_5d_fixture.c,
        )
    with pytest.raises(TypeError):
        # T must be a TimeSeries
        image_5d = mm_schema.Image5D(
            name=image_5d_fixture.name,
            description=image_5d_fixture.description,
            image_url=image_5d_fixture.image_url,
            source_image_url=image_5d_fixture.source_image_url,
            data=image_5d_fixture.data,
            t=[2, 3],
            z=image_5d_fixture.z,
            y=image_5d_fixture.y,
            x=image_5d_fixture.x,
            c=image_5d_fixture.c,
        )
    with pytest.raises(TypeError):
        # Z must be a PixelSeries
        image_5d = mm_schema.Image5D(
            name=image_5d_fixture.name,
            description=image_5d_fixture.description,
            image_url=image_5d_fixture.image_url,
            source_image_url=image_5d_fixture.source_image_url,
            data=image_5d_fixture.data,
            t=image_5d_fixture.t,
            z=[2, 3],
            y=image_5d_fixture.y,
            x=image_5d_fixture.x,
            c=image_5d_fixture.c,
        )
    with pytest.raises(TypeError):
        # Y must be a PixelSeries
        image_5d = mm_schema.Image5D(
            name=image_5d_fixture.name,
            description=image_5d_fixture.description,
            image_url=image_5d_fixture.image_url,
            source_image_url=image_5d_fixture.source_image_url,
            data=image_5d_fixture.data,
            t=image_5d_fixture.t,
            z=image_5d_fixture.z,
            y=[2, 3],
            x=image_5d_fixture.x,
            c=image_5d_fixture.c,
        )
    with pytest.raises(TypeError):
        # X must be a PixelSeries
        image_5d = mm_schema.Image5D(
            name=image_5d_fixture.name,
            description=image_5d_fixture.description,
            image_url=image_5d_fixture.image_url,
            source_image_url=image_5d_fixture.source_image_url,
            data=image_5d_fixture.data,
            t=image_5d_fixture.t,
            z=image_5d_fixture.z,
            y=image_5d_fixture.y,
            x="wrong type",
            c=image_5d_fixture.c,
        )
    with pytest.raises(TypeError):
        # C must be a ChannelSeries
        image_5d = mm_schema.Image5D(
            name=image_5d_fixture.name,
            description=image_5d_fixture.description,
            image_url=image_5d_fixture.image_url,
            source_image_url=image_5d_fixture.source_image_url,
            data=image_5d_fixture.data,
            t=image_5d_fixture.t,
            z=image_5d_fixture.z,
            y=image_5d_fixture.y,
            x=image_5d_fixture.x,
            c=[2, 3],
        )


def test_image_5d_validity(image_5d_fixture):
    dumper = YAMLDumper()
    loader = YAMLLoader()
    yaml_string = dumper.dumps(image_5d_fixture)
    loaded_image_5d = loader.loads(yaml_string, mm_schema.Image5D)

    assert image_5d_fixture == loaded_image_5d


def test_point_creation():
    point = mm_schema.Point(x=1, y=2, z=3)
    assert point.x == 1
    assert point.y == 2
    assert point.z == 3


def test_point_attributes_required():
    with pytest.raises(ValueError):
        point = mm_schema.Point(x=1, z=3)
    with pytest.raises(ValueError):
        point = mm_schema.Point(y=2, z=3)


def test_point_attributes_types():
    point = mm_schema.Point(x=1, y=2, z=3)
    assert isinstance(point.x, float)
    assert isinstance(point.y, float)
    assert isinstance(point.z, float)


def test_point_attributes_values():
    with pytest.raises(ValueError):
        point = mm_schema.Point(x="x", y=2)
    with pytest.raises(ValueError):
        point = mm_schema.Point(x=1, y="y")
    with pytest.raises(ValueError):
        point = mm_schema.Point(x=1, y=2, z="z")
    with pytest.raises(ValueError):
        point = mm_schema.Point(x=1, y=2, c="c")
    with pytest.raises(TypeError):
        point = mm_schema.Point(x=1, y=2, fill_color="fill_color")
    with pytest.raises(TypeError):
        point = mm_schema.Point(x=1, y=2, stroke_color="stroke_color")
    with pytest.raises(ValueError):
        point = mm_schema.Point(x=1, y=2, stroke_width="stroke_width")
