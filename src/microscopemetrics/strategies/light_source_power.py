import datetime as dt

import numpy as np
import pandas as pd

try:
    from hypothesis import assume
    from hypothesis import strategies as st
except ImportError as e:
    raise ImportError(
        "In order to run the strategies you need to install the test extras. Run `pip install microscopemetrics[test]`."
    ) from e
import microscopemetrics_schema.strategies.analyses as st_mm_analyses_schema


def _add_seconds_to_datetime(datetime: dt.datetime, seconds: float) -> dt.datetime:
    return datetime + dt.timedelta(seconds=seconds)


# Strategies for Light Source Power
@st.composite
def st_light_source_test_data(
    draw,
    light_sources=st.lists(st_mm_analyses_schema.st_mm_light_source(), min_size=1, max_size=5),
    measuring_location=st.just("OBJECTIVE_FOCAL"),
    acquisition_start_datetime=st.datetimes(),
    nr_linearity_measurements=st.integers(min_value=5, max_value=10),
    linearity_interval_seconds=st.just(60.0),
    linearity_integration_time_seconds=st.just(1.0),
    # nr_short_term_stability_measurements=st.just(300),
    # short_term_stability_interval_seconds=st.just(1.0),
    # short_term_stability_integration_time_seconds=st.just(0.1),
    # nr_long_term_stability_measurements=st.just(240),
    # long_term_stability_interval_seconds=st.just(30.0),
    # long_term_stability_integration_time_seconds=st.just(0.1),
    target_intensity_mw=st.floats(min_value=10.0, max_value=100.0),
    target_intensity_std_rel=st.floats(min_value=0.01, max_value=0.1),
):
    power_measurements = []
    current_datetime = draw(acquisition_start_datetime)
    light_sources = draw(light_sources)
    linearity_interval_seconds = draw(linearity_interval_seconds)
    linearity_integration_time_seconds = draw(linearity_integration_time_seconds)
    target_intensity_std_rel = draw(target_intensity_std_rel)

    for light_source in light_sources:
        power_meter = draw(st_mm_analyses_schema.st_mm_power_meter())
        location = draw(measuring_location)
        target_intensity_mw = draw(target_intensity_mw)

        # Generating linearity measurements
        set_power_values = np.linspace(0.0, 1.0, draw(nr_linearity_measurements))
        for set_power_value in set_power_values:
            measured_power = max(
                0.0,
                np.random.normal(
                    loc=set_power_value,
                    scale=target_intensity_std_rel,
                )
                * target_intensity_mw,
            )
            power_measurements.append(
                {
                    "acquisition_datetime": current_datetime,
                    "light_source": light_source,
                    "measurement_device": power_meter,
                    "measuring_location": location,
                    "power_set_point": set_power_value,
                    "power_mw": measured_power,
                    "integration_time_seconds": linearity_integration_time_seconds,
                }
            )
            current_datetime = _add_seconds_to_datetime(
                current_datetime, linearity_interval_seconds
            )

    return power_measurements


@st.composite
def st_light_source_power_dataset(
    draw,
    unprocessed_dataset=st_mm_analyses_schema.st_mm_light_source_power_unprocessed_dataset(),
    test_data=st_light_source_power_test_data(),
):
    test_data = draw(test_data)
    field_illumination_unprocessed_dataset = draw(unprocessed_dataset)

    field_illumination_unprocessed_dataset.input_data.field_illumination_images = [
        numpy_to_mm_image(
            array=image,
            name=f"FI_image_{i}",
            channel_names=[f"Channel_{i}{j}" for j in range(image.shape[-1])],
        )
        for i, image in enumerate(test_data.pop("images"))
    ]

    # Setting the bit depth to the data type of the image
    image_dtype = {
        a.array_data.dtype
        for a in field_illumination_unprocessed_dataset.input_data.field_illumination_images
    }
    if len(image_dtype) != 1:
        raise ValueError("All images should have the same data type")
    image_dtype = image_dtype.pop()
    if np.issubdtype(image_dtype, np.integer):
        field_illumination_unprocessed_dataset.input_parameters.bit_depth = np.iinfo(
            image_dtype
        ).bits
    elif np.issubdtype(image_dtype, np.floating):
        field_illumination_unprocessed_dataset.input_parameters.bit_depth = np.finfo(
            image_dtype
        ).bits
    else:
        field_illumination_unprocessed_dataset.input_parameters.bit_depth = None

    return {
        "unprocessed_dataset": field_illumination_unprocessed_dataset,
        "expected_output": test_data,
    }


@st.composite
def st_field_illumination_table(
    draw,
    nr_rows=st.integers(min_value=1, max_value=50),
):
    nr_rows = draw(nr_rows)
    columns = [
        "bottom_center_intensity_mean",
        "bottom_center_intensity_ratio",
        "channel_nr",
    ]
    table = []
    for _ in range(nr_rows):
        dataset = draw(st_field_illumination_dataset())["unprocessed_dataset"]
        dataset.run()
        if dataset.processed:
            key_values = {col: getattr(dataset.output.key_values, col) for col in columns}
        else:
            continue
        table.append(key_values)

    table = [pd.DataFrame(d) for d in table]

    return pd.concat(table, ignore_index=True)
