import numpy as np
import pytest
from hypothesis import assume, given
from hypothesis import strategies as st
from skimage.filters import gaussian

from microscopemetrics.samples import field_illumination, numpy_to_image_byref
from tests.test_utilities import get_file


@st.composite
def field_illumination_image(
    draw,
    x_image_shape: int = st.integers(min_value=256, max_value=2048),
    y_image_shape: int = st.integers(min_value=256, max_value=2048),
    dtype: np.dtype = st.sampled_from([np.uint8, np.uint16, np.float32, np.float64]),
    noise: float = st.floats(min_value=0, max_value=1),
    x_center_rel_offset: float = st.floats(min_value=-0.8, max_value=0.8),
    y_center_rel_offset: float = st.floats(min_value=-0.8, max_value=0.8),
    dispersion: float = st.floats(min_value=0.1, max_value=10),
):
    """This strategy generates a field illumination image."""
    x_image_shape = draw(x_image_shape)
    y_image_shape = draw(y_image_shape)
    assume(0.5 < (x_image_shape / y_image_shape) < 2)

    dtype = draw(dtype)

    x_center_rel_offset = draw(x_center_rel_offset)
    y_center_rel_offset = draw(y_center_rel_offset)
    dispersion = draw(dispersion)

    image = np.zeros(shape=(x_image_shape, y_image_shape), dtype=dtype)
    x_center = int(image.shape[0] * (0.5 + x_center_rel_offset / 2))
    y_center = int(image.shape[1] * (0.5 + y_center_rel_offset / 2))

    if np.issubdtype(dtype, np.integer):
        max_value = np.iinfo(dtype).max
    elif np.issubdtype(dtype, np.floating):
        max_value = np.finfo(dtype).max
    else:
        raise ValueError("Unsupported datatype")

    image[x_center, y_center] = max_value / 2

    image = gaussian(
        image, sigma=max(x_image_shape, y_image_shape) * dispersion, preserve_range=True
    )

    return {
        "image": image,
        "noise": noise,
        "x_center_rel_offset": x_center_rel_offset,
        "y_center_rel_offset": y_center_rel_offset,
        "dispersion": dispersion,
    }


@pytest.fixture
def field_illumination_analysis():
    image_url = "https://dev.mri.cnrs.fr/attachments/download/3071/chroma.npy"
    file_path = get_file(image_url)
    data = np.load(file_path)
    analysis = field_illumination.FieldIlluminationAnalysis(
        name="an analysis",
        description="a description",
        microscope="1234",
        input={
            "field_illumination_image": numpy_to_image_byref(
                array=data,
                name="image_name",
                description="image_description",
                image_url=image_url,
                source_image_url=image_url,
            ),
        },
        output={},
    )

    return analysis


def test_run_field_illumination(field_illumination_analysis):
    assert field_illumination_analysis.run()
    assert field_illumination_analysis.processed
