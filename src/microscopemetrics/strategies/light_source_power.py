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
import microscopemetrics_schema.datamodel as mm_schema
import microscopemetrics_schema.strategies.analyses as st_mm_analyses_schema


def _add_seconds_to_datetime(datetime: dt.datetime, seconds: float) -> dt.datetime:
    return datetime + dt.timedelta(seconds=seconds)


def _generate_power_measurement(
    set_power_value: float,
    target_intensity_std_rel,
    target_intensity_mw,
    datetime,
    light_source,
    power_meter,
    measuring_location,
    linearity_integration_time_seconds,
):
    measured_power = max(
        0.0,
        np.random.normal(
            loc=set_power_value,
            scale=target_intensity_std_rel,
        )
        * target_intensity_mw,
    )

    return mm_schema.PowerMeasurement(
        acquisition_datetime=datetime,
        light_source=light_source,
        power_meter=power_meter,
        measuring_location=measuring_location,
        power_set_point=set_power_value,
        power_mw=measured_power,
        integration_time_seconds=linearity_integration_time_seconds,
    )


def generate_power_measurements(
    current_datetime,
    light_source,
    power_meter,
    measuring_location,
    target_intensity_mw,
    target_intensity_std_rel,
    linearity_integration_time_seconds,
    nr_linearity_measurements,
    linearity_interval_seconds,
    nr_short_term_stability_measurements,
    short_term_stability_set_power_value,
    short_term_stability_interval_seconds,
    nr_long_term_stability_measurements,
    long_term_stability_set_power_value,
    long_term_stability_interval_seconds,
):
    power_measurements = []

    # Generating linearity measurements
    set_power_values = np.linspace(0.0, 1.0, nr_linearity_measurements)
    for set_power_value in set_power_values:
        power_measurements.append(
            _generate_power_measurement(
                set_power_value=set_power_value,
                target_intensity_std_rel=target_intensity_std_rel,
                target_intensity_mw=target_intensity_mw,
                datetime=current_datetime,
                light_source=light_source,
                power_meter=power_meter,
                measuring_location=measuring_location,
                linearity_integration_time_seconds=linearity_integration_time_seconds,
            )
        )
        current_datetime = _add_seconds_to_datetime(current_datetime, linearity_interval_seconds)

    # Generating short-term stability measurements
    for _ in range(nr_short_term_stability_measurements):
        power_measurements.append(
            _generate_power_measurement(
                set_power_value=short_term_stability_set_power_value,
                target_intensity_std_rel=target_intensity_std_rel,
                target_intensity_mw=target_intensity_mw,
                datetime=current_datetime,
                light_source=light_source,
                power_meter=power_meter,
                measuring_location=measuring_location,
                linearity_integration_time_seconds=linearity_integration_time_seconds,
            )
        )
        current_datetime = _add_seconds_to_datetime(
            current_datetime, short_term_stability_interval_seconds
        )

    # Generating long-term stability measurements
    for _ in range(nr_long_term_stability_measurements):
        power_measurements.append(
            _generate_power_measurement(
                set_power_value=long_term_stability_set_power_value,
                target_intensity_std_rel=target_intensity_std_rel,
                target_intensity_mw=target_intensity_mw,
                datetime=current_datetime,
                light_source=light_source,
                power_meter=power_meter,
                measuring_location=measuring_location,
                linearity_integration_time_seconds=linearity_integration_time_seconds,
            )
        )
        current_datetime = _add_seconds_to_datetime(
            current_datetime, long_term_stability_interval_seconds
        )

    return power_measurements, current_datetime


# Strategies for Light Source Power
@st.composite
def st_light_source_power_test_data(
    draw,
    light_sources=st.lists(st_mm_analyses_schema.st_mm_light_source(), min_size=1, max_size=5),
    power_meter=st_mm_analyses_schema.st_mm_power_meter(),
    measuring_location=st.just("OBJECTIVE_FOCAL"),
    acquisition_start_datetime=st.datetimes(),
    nr_linearity_measurements=st.integers(min_value=5, max_value=10),
    linearity_interval_seconds=st.just(60.0),
    linearity_integration_time_seconds=st.just(1.0),
    nr_short_term_stability_measurements=st.just(300),
    short_term_stability_set_power_value=st.just(1.0),
    short_term_stability_interval_seconds=st.just(1.0),
    short_term_stability_integration_time_seconds=st.just(0.1),
    nr_long_term_stability_measurements=st.just(240),
    long_term_stability_set_power_value=st.just(1.0),
    long_term_stability_interval_seconds=st.just(30.0),
    long_term_stability_integration_time_seconds=st.just(0.1),
    target_intensity_mw=st.floats(min_value=10.0, max_value=100.0),
    target_intensity_std_rel=st.floats(min_value=0.01, max_value=0.1),
):
    _current_datetime = draw(acquisition_start_datetime)
    _light_sources = draw(light_sources)

    # We don't want to "draw" the same value for all measurements
    _nr_linearity_measurements = draw(nr_linearity_measurements)
    _linearity_interval_seconds = draw(linearity_interval_seconds)
    _linearity_integration_time_seconds = draw(linearity_integration_time_seconds)
    _nr_short_term_stability_measurements = draw(nr_short_term_stability_measurements)
    _short_term_stability_interval_seconds = draw(short_term_stability_interval_seconds)
    _short_term_stability_set_power_value = draw(short_term_stability_set_power_value)
    _long_term_stability_set_power_value = draw(long_term_stability_set_power_value)
    _short_term_stability_integration_time_seconds = draw(
        short_term_stability_integration_time_seconds
    )
    _nr_long_term_stability_measurements = draw(nr_long_term_stability_measurements)
    _long_term_stability_interval_seconds = draw(long_term_stability_interval_seconds)
    _long_term_stability_integration_time_seconds = draw(
        long_term_stability_integration_time_seconds
    )

    input_parameters = draw(
        st_mm_analyses_schema.st_mm_light_source_power_input_parameters(
            linearity_required_measurements=st.integers(
                min_value=_nr_linearity_measurements,
                max_value=_nr_linearity_measurements + 10,
            ),
            short_term_stability_measurement_interval_seconds=st.just(
                _short_term_stability_interval_seconds
            ),
            short_term_stability_required_measurements=st.integers(
                min_value=_nr_short_term_stability_measurements,
                max_value=_nr_short_term_stability_measurements + 50,
            ),
            short_term_stability_required_integration_time_seconds=st.floats(
                min_value=_short_term_stability_integration_time_seconds,
                max_value=_short_term_stability_integration_time_seconds + 0.1,
            ),
            long_term_stability_measurement_interval_seconds=st.just(
                _long_term_stability_interval_seconds
            ),
            long_term_stability_required_measurements=st.integers(
                min_value=_nr_long_term_stability_measurements,
                max_value=_nr_long_term_stability_measurements + 100,
            ),
            long_term_stability_required_integration_time_seconds=st.floats(
                min_value=_long_term_stability_integration_time_seconds,
                max_value=_long_term_stability_integration_time_seconds + 1.0,
            ),
        )
    )

    power_measurements = []
    for light_source in _light_sources:
        new_measurements, _current_datetime = generate_power_measurements(
            current_datetime=_current_datetime,
            light_source=light_source,
            power_meter=draw(power_meter),
            measuring_location=draw(measuring_location),
            target_intensity_mw=draw(target_intensity_mw),
            target_intensity_std_rel=draw(target_intensity_std_rel),
            linearity_integration_time_seconds=_linearity_integration_time_seconds,
            nr_linearity_measurements=_nr_linearity_measurements,
            linearity_interval_seconds=_linearity_interval_seconds,
            nr_short_term_stability_measurements=_nr_short_term_stability_measurements,
            short_term_stability_set_power_value=_short_term_stability_set_power_value,
            short_term_stability_interval_seconds=_short_term_stability_interval_seconds,
            nr_long_term_stability_measurements=_nr_long_term_stability_measurements,
            long_term_stability_set_power_value=_long_term_stability_set_power_value,
            long_term_stability_interval_seconds=_long_term_stability_interval_seconds,
        )
        _current_datetime = _add_seconds_to_datetime(_current_datetime, 60)
        power_measurements.extend(new_measurements)

    return {
        "input_data_power_measurements": power_measurements,
        "input_parameters:": input_parameters,
    }


@st.composite
def st_light_source_power_dataset(
    draw,
    unprocessed_dataset=st_mm_analyses_schema.st_mm_light_source_power_unprocessed_dataset(),
    test_data=st_light_source_power_test_data(),
):
    test_data = draw(test_data)
    light_source_power_dataset = draw(unprocessed_dataset)
    light_source_power_dataset.input_data.power_measurements = test_data[
        "input_data_power_measurements"
    ]
    light_source_power_dataset.input_parameters = test_data["input_parameters:"]

    return {
        "unprocessed_dataset": light_source_power_dataset,
        "expected_output": test_data,
    }
