import microscopemetrics_schema.datamodel as mm_schema
import pytest
from hypothesis import example, given
from hypothesis import strategies as st
from hypothesis.extra.numpy import arrays as st_arrays
from linkml_runtime import linkml_model

from microscopemetrics.samples import (
    numpy_to_image_byref,
    numpy_to_image_inlined,
    numpy_to_mask_inlined,
)


class NotAString:
    def __str__(self):
        pass


@given(st.builds(mm_schema.NamedObject))
def test_named_object(named_object):
    assert named_object


@given(
    st.builds(
        mm_schema.Experimenter,
        name=st.text(),
        orcid=st.from_regex(r"\d{4}-\d{4}-\d{4}-\d{4}"),
    )
)
# @example(mm_schema.Experimenter(name=st.text(), orcid=st.lists(elements=st.integers()))).xfail()
def test_experimenter_creation(experimenter):
    assert experimenter


@given(
    st.builds(
        mm_schema.Protocol,
        name=st.text(),
        description=st.text(),
        version=st.text(),
        authors=st.lists(st.from_regex(r"\d{4}-\d{4}-\d{4}-\d{4}")),
        url=st.uuids(),
    )
)
def test_protocol_creation(protocol):
    assert protocol


@given(
    st.builds(
        mm_schema.Sample,
        name=st.text(),
        description=st.text(),
        type=st.text(),
        protocol=st.uuids(),
    )
)
def test_sample_creation(sample):
    assert sample


@given(
    st.builds(
        mm_schema.Microscope,
        name=st.text(),
        description=st.text(),
        id=st.integers(),
        manufacturer=st.text(),
        serial_number=st.text(),
        model=st.text(),
        type=st.sampled_from(
            [
                v.text
                for k, v in mm_schema.MicroscopeType.__dict__.items()
                if isinstance(v, linkml_model.meta.PermissibleValue)
            ]
        ),
        url=st.uuids(),
        comment=st.builds(mm_schema.Comment, date=st.dates(), text=st.text()),
    )
)
def test_microscope_creation(microscope):
    assert microscope


@given(
    st.builds(
        mm_schema.MetricsDataset,
        name=st.text(),
        description=st.text(),
        microscope=st.uuids(),
        sample=st.builds(
            mm_schema.Sample,
            name=st.text(),
            description=st.text(),
            type=st.text(),
            protocol=st.uuids(),
        ),
        experimenter=st.from_regex(r"\d{4}-\d{4}-\d{4}-\d{4}"),
        acquisition_date=st.dates(),
        processed=st.booleans(),
        processing_date=st.dates(),
        processing_log=st.text(),
    )
)
def test_metrics_dataset_creation(metrics_dataset):
    assert metrics_dataset


@given(
    name=st.text(),
    description=st.text(),
    array=st_arrays(dtype="float64", shape=(3, 3)),
    image_url=st.uuids(),
    source_image_url=st.uuids(),
)
def test_image_byref_from_numpy_2d_creation(name, description, array, image_url, source_image_url):
    assert numpy_to_image_byref(
        name=name,
        description=description,
        array=array,
        image_url=image_url,
        source_image_url=source_image_url,
    )


@given(
    name=st.text(),
    description=st.text(),
    array=st_arrays(dtype="float64", shape=(3, 3, 3, 3, 3)),
    image_url=st.uuids(),
    source_image_url=st.uuids(),
)
def test_image_byref_from_numpy_5d_creation(name, description, array, image_url, source_image_url):
    assert numpy_to_image_byref(
        name=name,
        description=description,
        array=array,
        image_url=image_url,
        source_image_url=source_image_url,
    )


@given(
    name=st.text(),
    description=st.text(),
    image_url=st.uuids(),
    source_image_url=st.uuids(),
    array=st_arrays(dtype="bool", shape=(3, 3)),
)
def test_image_mask_creation(name, description, image_url, source_image_url, array):
    assert numpy_to_mask_inlined(
        name=name,
        description=description,
        image_url=image_url,
        source_image_url=source_image_url,
        array=array,
    )


@given(
    st.builds(
        mm_schema.Point,
        label=st.text(),
        x=st.floats(),
        y=st.floats(),
        z=st.floats(),
    )
)
def test_point_creation(point):
    assert point


@given(
    st.builds(
        mm_schema.Line,
        label=st.text(),
        x1=st.floats(),
        y1=st.floats(),
        x2=st.floats(),
        y2=st.floats(),
        z=st.floats(),
    )
)
def test_line_creation(line):
    assert line


@given(
    st.builds(
        mm_schema.Rectangle,
        label=st.text(),
        x=st.floats(),
        y=st.floats(),
        w=st.floats(),
        h=st.floats(),
    )
)
def test_rectangle_creation(rectangle):
    assert rectangle


@given(
    st.builds(
        mm_schema.Ellipse,
        label=st.text(),
        x=st.floats(),
        y=st.floats(),
        x_rad=st.floats(),
        y_rad=st.floats(),
    )
)
def test_ellipse_creation(ellipse):
    assert ellipse


@given(
    st.builds(
        mm_schema.Polygon,
        label=st.text(),
        vertexes=st.lists(
            st.builds(
                mm_schema.Vertex,
                x=st.floats(),
                y=st.floats(),
            ),
            min_size=3,  # TODO: Fix this in the schema. A polygon should have at least 3 vertexes
        ),
        is_open=st.booleans(),
    ),
)
def test_polygon_creation(polygon):
    assert polygon
