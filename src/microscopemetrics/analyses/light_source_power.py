import logging
from datetime import datetime
from typing import Dict, List, Tuple

import microscopemetrics_schema.datamodel as mm_schema
import numpy as np
import pandas as pd
import scipy

import microscopemetrics as mm
from microscopemetrics.analyses import tools as mm_tools

# TODO: Determine what are we going to consider the threshold for measuring stability
REQ_NR = 10


def _stability(values: np.ndarray) -> float:
    p_max = np.max(values)
    p_min = np.min(values)
    return 1 - ((p_max - p_min) / (p_max + p_min))


def _compute_single_measurement(measurements: pd.DataFrame) -> Dict:
    return {
        "nr_of_measurements": len(measurements),
        "power_mean_mw": measurements["power_mw"].mean,
        "power_median_mw": measurements["power_mw"].median,
        "power_std_mw": measurements["power_mw"].std,
        "power_min_mw": measurements["power_mw"].min,
        "power_max_mw": measurements["power_mw"].max,
    }


def _compute_linearity(measurements: pd.DataFrame) -> Dict:
    pass


def _compute_stability(
    measurements: pd.DataFrame, short_long_term_threshold_seconds: float
) -> Dict:
    measurements = measurements.sort_values(by="acquisition_datetime")
    time_deltas = measurements["acquisition_datetime"].diff().dt.total_seconds().fillna(0).values
    # The first measurement delta is always zero, so we set it to the second one
    time_deltas[0] = time_deltas[1]
    long_term_segment = time_deltas > short_long_term_threshold_seconds
    short_term_segment = ~long_term_segment

    long_term_stability = None
    long_term_measurement_duration_seconds = None
    short_term_stability = None
    short_term_measurement_duration_seconds = None
    if np.any(long_term_segment):
        # Validate that there are enough measurements for long term stability
        if np.sum(long_term_segment) < REQ_NR:
            logging.warning("Not enough measurements for long term stability analysis.")
        else:
            logging.info("Light source has long term stability measurements.")
            long_term_stability = _stability(measurements[short_term_segment]["power_mw"].values)
            long_term_measurement_duration_seconds = time_deltas[short_term_segment].mean()
    if np.any(short_term_segment):
        # Validate that there are enough measurements for short term stability
        if np.sum(short_term_segment) < REQ_NR:
            logging.warning("Not enough measurements for short term stability analysis.")
        else:
            logging.info("Light source has short term stability measurements.")
            short_term_stability = _stability(measurements[long_term_segment]["power_mw"].values)
            short_term_measurement_duration_seconds = time_deltas[long_term_segment].mean()

    return {
        "power_std_mw": measurements["power_mw"].std,
        "short_term_power_stability": short_term_stability,
        "short_term_measurement_duration_seconds": short_term_measurement_duration_seconds,
        "long_term_power_stability": long_term_stability,
        "long_term_measurement_duration_seconds": long_term_measurement_duration_seconds,
    }


def _compute_light_source_power_key_measurements(
    power_measurements: List[mm_schema.PowerMeasurement],
    input_parameters: mm_schema.LightSourcePowerInputParameters,
) -> mm_schema.LightSourcePowerKeyMeasurements:
    power_measurement_df = pd.DataFrame.from_records(power_measurements)
    key_measurements = []

    # Replace some of the columns with the identifiers instead of the full objects
    power_measurement_df["light_source"] = power_measurement_df["light_source"].apply(
        lambda ls: ls.wavelength_nm if ls else None
    )
    power_measurement_df["measurement_device"] = power_measurement_df["measurement_device"].apply(
        lambda md: md.name if md else None
    )

    # Go through each light source, power meter and measuring location combinations
    for light_source in power_measurement_df["light_source"].unique():
        for measurement_device in power_measurement_df["measurement_device"].unique():
            for measuring_location in power_measurement_df["measuring_location"].unique():
                logging.info(
                    f"Processing light source {light_source}, "
                    f"measurement device {measurement_device}, "
                    f"measuring location {measuring_location}."
                )

                subset_key_measurements = {
                    "light_source": light_source,
                    "measurement_device": measurement_device,
                    "measuring_location": measuring_location,
                }

                subset_df = power_measurement_df[
                    (power_measurement_df["light_source"] == light_source)
                    & (power_measurement_df["measurement_device"] == measurement_device)
                    & (power_measurement_df["measuring_location"] == measuring_location)
                ]

                # Catch the case where we have only one measurement
                if len(subset_df) == 1:
                    subset_key_measurements |= _compute_single_measurement(subset_df)
                    key_measurements.append(subset_key_measurements)

                    continue

                power_set_point_counts = subset_df["power_set_point"].value_counts()
                if len(power_set_point_counts) == 1:
                    # There are no linearity measurements, only stability
                    if power_set_point_counts[0] < REQ_NR:
                        # Not enough measurements for stability analysis
                        logging.warning(
                            "Not enough measurements for stability analysis, Treating as single measurement."
                        )
                        subset_key_measurements |= _compute_single_measurement(subset_df)
                        key_measurements.append(subset_key_measurements)
                    else:
                        subset_key_measurements |= _compute_single_measurement(subset_df)
                        subset_key_measurements |= _compute_stability(
                            short_long_term_threshold_seconds=input_parameters.short_long_term_threshold_seconds,
                            measurements=subset_df,
                        )
                        key_measurements.append(subset_key_measurements)

                    continue

                elif 1 < len(power_set_point_counts) < 10:
                    logging.error("Not enough different power set points for linearity analysis.")
                    continue

                else:
                    # There are linearity measurements, and possibly stability too
                    # We are only considering the scenario where there is a single measurement per power set point and,
                    # possibly, more than REQ_NR measurements for stability analysis
                    stability_mask = power_set_point_counts > REQ_NR
                    linearity_mask = power_set_point_counts == 1
                    if np.sum(linearity_mask) < 10:
                        logging.error(
                            "Not enough different power set points for linearity analysis."
                        )
                        continue

                # Populate the key measurements with single measurement results
                pass


def analyse_light_source_power(dataset: mm_schema.LightSourcePowerDataset) -> bool:
    mm.analyses.validate_requirements()

    key_measurements = _compute_light_source_power_key_measurements(
        power_measurements=dataset.input_data.power_measurements,
        input_parameters=dataset.input_parameters,
    )

    dataset.output = mm_schema.LightSourcePowerOutput(
        processing_application="microscopemetrics",
        processing_version=mm.__version__,
        processing_datetime=datetime.now(),
        key_measurements=key_measurements,
    )

    dataset.processed = True

    return True
