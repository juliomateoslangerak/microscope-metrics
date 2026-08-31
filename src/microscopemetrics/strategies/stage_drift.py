import numpy as np

try:
    from hypothesis import assume
    from hypothesis import strategies as st
except ImportError as e:
    raise ImportError(
        "In order to run the strategies you need to install the test extras. Run `pip install microscopemetrics[test]`."
    ) from e
import microscopemetrics_schema.strategies.analyses as st_mm_analyses_schema

from microscopemetrics.analyses.schema_tools import numpy_to_mm_image
from microscopemetrics.strategies import st_beads_test_data


# Strategies for Stage Drift
@st.composite
def st_stage_drift_dataset(
    draw,
    unprocessed_dataset=st_mm_analyses_schema.st_mm_stage_drift_unprocessed_dataset(),
    test_data=st_beads_test_data(
        nr_images=st.just(2),
        z_image_shape=st.just(1),
        y_image_shape=st.just(256),
        x_image_shape=st.just(256),
        c_image_shape=st.just(1),
        t_image_shape=st.just(5),
        nr_valid_beads=st.just(1),
        nr_edge_beads=st.just(0),
        nr_out_of_focus_beads=st.just(0),
        nr_clustering_beads=st.just(0),
        min_lateral_distance_px=st.just(5),
        min_axial_distance_px=st.just(0),
        drift_z=st.just(2.0),
        drift_y=st.just(2.0),
        drift_x=st.just(2.0),
    ),
):
    test_data = draw(test_data)
    stage_drift_unprocessed_dataset = draw(unprocessed_dataset)
    excitation_wavelengths_nm = [405.0, 488.0, 561.0, 642.0, 705.0]
    emission_wavelengths_nm = [435.0, 525.0, 605.0, 692.0, 750.0]
    voxel_size_micron_z = 0.3
    voxel_size_micron_y = voxel_size_micron_x = 0.1
    time_intervals_sec = 60

    stage_drift_unprocessed_dataset.input_data.beads_images = [
        numpy_to_mm_image(
            array=image,
            name=f"beads_image_{i}",
            channel_names=[f"Channel_{c}" for c in range(image.shape[-1])],
            excitation_wavelengths_nm=[
                excitation_wavelengths_nm[c] for c in range(image.shape[-1])
            ],
            emission_wavelengths_nm=[emission_wavelengths_nm[c] for c in range(image.shape[-1])],
            voxel_size_micron_z=voxel_size_micron_z,
            voxel_size_micron_y=voxel_size_micron_y,
            voxel_size_micron_x=voxel_size_micron_x,
            time_intervals_sec=time_intervals_sec,
        )
        for i, image in enumerate(test_data.pop("images"))
    ]

    # Setting the bit depth to the data type of the image
    image_dtype = {
        a.array_data.dtype for a in stage_drift_unprocessed_dataset.input_data.beads_images
    }
    if len(image_dtype) != 1:
        raise ValueError("All images should have the same data type")
    image_dtype = image_dtype.pop()
    if np.issubdtype(image_dtype, np.integer):
        stage_drift_unprocessed_dataset.input_parameters.bit_depth = np.iinfo(image_dtype).bits
    elif np.issubdtype(image_dtype, np.floating):
        stage_drift_unprocessed_dataset.input_parameters.bit_depth = np.finfo(image_dtype).bits
    else:
        stage_drift_unprocessed_dataset.input_parameters.bit_depth = None

    return {
        "unprocessed_dataset": stage_drift_unprocessed_dataset,
        "expected_output": test_data,
    }
