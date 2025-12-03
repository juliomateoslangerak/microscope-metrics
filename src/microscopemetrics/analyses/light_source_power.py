import logging
from dataclasses import asdict
from datetime import datetime
from typing import Dict, List, Tuple

import microscopemetrics_schema.datamodel as mm_schema
import numpy as np
import pandas as pd
import scipy

import microscopemetrics as mm
from microscopemetrics.analyses import tools as mm_tools

# TODO: Determine what are we going to consider the threshold for measuring stability


def _find_linearity_subset(
    df: pd.DataFrame,
    min_points: int = 10,
) -> pd.DataFrame | None:
    """
    Find the single longest contiguous block of rows where light source power linearity can be assessed.

    Returns a copy of the subset DataFrame or None if none found.
    Assumes df is ordered by acquisition_datetime (contiguity is with respect to df order).
    """
    if df.empty:
        return None

    linearity_subset_df = df.copy()

    linearity_mask = (
        linearity_subset_df["power_set_point"] == linearity_subset_df["power_set_point"].shift()
    )
    groups = linearity_mask.cumsum()

    # Find the rows where power_set_point changes
    groups = linearity_subset_df.groupby(groups).agg(
        {"acquisition_datetime": ["count", "min", "max"]}
    )

    # Select the group with the maximum count of acquisition_datetime
    linearity_group = groups[
        groups["acquisition_datetime"]["count"] == groups["acquisition_datetime"]["count"].max()
    ]
    if (
        linearity_group.empty
        or linearity_group["acquisition_datetime"]["count"].iloc[0] < min_points
    ):
        return None

    start_time = linearity_group["acquisition_datetime"]["min"].iloc[0]
    end_time = linearity_group["acquisition_datetime"]["max"].iloc[0]
    subset = linearity_subset_df[
        (linearity_subset_df["acquisition_datetime"] >= start_time)
        & (linearity_subset_df["acquisition_datetime"] <= end_time)
    ]

    return subset.copy()


def _find_stability_subset(
    df: pd.DataFrame,
    min_nb_points: int,
    interval_seconds: float,
    tolerance_seconds: float = 0.1,
) -> List[pd.DataFrame] | None:
    """
    Find the contiguous blocks of rows where light source power stability can be assessed.

    Returns a list of the subset DataFrames or None if none found.
    Assumes df is ordered by acquisition_datetime (contiguity is with respect to df order).
    """
    if df.empty:
        return None

    stability_subset_df = df.copy()

    # Find the rows where power_set_point does not change, integration_time_seconds does not change,
    # and diff between acquisition_datetime is constant and close to interval_seconds
    set_point_mask = (
        stability_subset_df["power_set_point"] != stability_subset_df["power_set_point"].shift()
    )
    integration_time_mask = (
        stability_subset_df["integration_time_seconds"]
        != stability_subset_df["integration_time_seconds"].shift()
    )
    interval_time_mask = ~np.isclose(
        stability_subset_df["acquisition_datetime"].diff().dt.total_seconds().fillna(0),
        interval_seconds,
        atol=tolerance_seconds,
    )

    stability_mask = set_point_mask | integration_time_mask | interval_time_mask

    groups = stability_mask.cumsum()
    groups = stability_subset_df.groupby(groups).agg(
        {"acquisition_datetime": ["count", "min", "max"]}
    )

    # Select the group with the maximum count of acquisition_datetime
    stability_group = groups[
        groups["acquisition_datetime"]["count"] == groups["acquisition_datetime"]["count"].max()
    ]
    if stability_group["acquisition_datetime"]["count"].iloc[0] < min_nb_points:
        logging.warning(
            "Not enough measurements for stability analysis."
            f" Found {len(stability_group)}, required {min_nb_points}."
        )
        return None
    if stability_group.empty:
        logging.warning("No measurements for stability analysis.")
        return None

    start_time = stability_group["acquisition_datetime"]["min"].iloc[0]
    end_time = stability_group["acquisition_datetime"]["max"].iloc[0]

    return stability_subset_df[
        (stability_subset_df["acquisition_datetime"] >= start_time)
        & (stability_subset_df["acquisition_datetime"] <= end_time)
    ].copy()


def _compute_basic_measurement(measurements: pd.DataFrame) -> Dict:
    return {
        "nr_of_measurements": len(measurements),
        "power_mean_mw": measurements["power_mw"].mean().item(),
        "power_median_mw": measurements["power_mw"].median().item(),
        "power_std_mw": measurements["power_mw"].std().item(),
        "power_min_mw": measurements["power_mw"].min().item(),
        "power_max_mw": measurements["power_mw"].max().item(),
    }


def _compute_linearity(measurements: pd.DataFrame) -> Dict:
    slope, intercept, r_value, p_value, std_err = scipy.stats.linregress(
        measurements["power_set_point"].values,
        measurements["power_mw"].values,
    )
    return {
        "power_linearity_start_datetime": measurements["acquisition_datetime"]
        .iloc[0]
        .to_pydatetime(),
        "power_linearity_end_datetime": measurements["acquisition_datetime"]
        .iloc[-1]
        .to_pydatetime(),
        "power_linearity_slope": slope.item(),
        "power_linearity_intercept": intercept.item(),
        "power_linearity_coefficient_of_determination": (r_value**2).item(),
        "power_linearity_p_value": p_value.item(),
        "power_linearity_std_err": std_err.item(),
    }


def _compute_stability(measurements: pd.DataFrame) -> Dict:
    values = measurements["power_mw"].values
    p_max = np.max(values)
    p_min = np.min(values)
    stability = 1 - ((p_max - p_min) / (p_max + p_min))

    return {
        "stability_start_datetime": measurements["acquisition_datetime"].iloc[0].to_pydatetime(),
        "stability_end_datetime": measurements["acquisition_datetime"].iloc[-1].to_pydatetime(),
        "power_stability": stability.item(),
    }


def _compute_light_source_power_key_measurements(
    power_measurements: List[mm_schema.PowerMeasurement],
    input_parameters: mm_schema.LightSourcePowerInputParameters,
) -> List[mm_schema.LightSourcePowerKeyMeasurement]:
    power_measurement_df = pd.DataFrame.from_records([asdict(pm) for pm in power_measurements])

    # We change the datetime to microssecond precision to avoid issues when converting to XSD later
    power_measurement_df["acquisition_datetime"] = power_measurement_df[
        "acquisition_datetime"
    ].astype("datetime64[us]")

    power_measurement_df["measuring_location"] = power_measurement_df["measuring_location"].apply(
        lambda x: x
    )

    key_measurements = []

    # Go through each light source, power meter and measuring location combinations
    for light_source in power_measurement_df["light_source"].drop_duplicates(ignore_index=True):
        for power_meter in power_measurement_df["power_meter"].drop_duplicates(ignore_index=True):
            for measuring_location in power_measurement_df["measuring_location"].drop_duplicates(
                ignore_index=True
            ):
                logging.info(
                    f"Processing light source {light_source}, "
                    f"power meter {power_meter}, "
                    f"measuring location {measuring_location}."
                )

                subset_key_measurements = {
                    "light_source": light_source,
                    "power_meter": power_meter,
                    "measuring_location": measuring_location,
                    "nr_of_measurements": 0,
                    "power_mean_mw": np.nan,
                    "power_median_mw": np.nan,
                    "power_std_mw": np.nan,
                    "power_min_mw": np.nan,
                    "power_max_mw": np.nan,
                    "power_linearity_start_datetime": datetime.min,
                    "power_linearity_end_datetime": datetime.min,
                    "power_linearity_slope": np.nan,
                    "power_linearity_intercept": np.nan,
                    "power_linearity_coefficient_of_determination": np.nan,
                    "power_linearity_p_value": np.nan,
                    "power_linearity_std_err": np.nan,
                    "short_term_power_stability_start_datetime": datetime.min,
                    "short_term_power_stability_end_datetime": datetime.min,
                    "short_term_power_stability": np.nan,
                    "long_term_power_stability_start_datetime": datetime.min,
                    "long_term_power_stability_end_datetime": datetime.min,
                    "long_term_power_stability": np.nan,
                }

                subset_df = power_measurement_df[
                    (power_measurement_df["light_source"] == light_source)
                    & (power_measurement_df["power_meter"] == power_meter)
                    & (power_measurement_df["measuring_location"] == measuring_location)
                ]
                subset_df = subset_df.set_index("acquisition_datetime")
                subset_df.sort_index(inplace=True)
                subset_df.reset_index(inplace=True)

                # Catch the case where we have only one measurement
                if len(subset_df) == 1:
                    logging.info("Only one measurement found. Extracting basic statistics.")
                    subset_key_measurements |= _compute_basic_measurement(subset_df)
                    key_measurements.append(subset_key_measurements)

                    continue

                # Get basic statistics following these rules:
                # 1. If there is a single power set point with less than REQ_NR measurements, use it for basic statistics
                # 2. If there are a single power set point with more than REQ_NR measurements, use it for basic statistics
                # 3. throw an error otherwise

                basic_stats_df = _find_stability_subset(
                    subset_df,
                    min_nb_points=1,
                    interval_seconds=input_parameters.short_term_stability_measurement_interval_seconds,
                    tolerance_seconds=0.1,
                )
                linearity_df = _find_linearity_subset(
                    subset_df,
                    min_points=input_parameters.linearity_required_measurements,
                )
                short_term_stability_df = _find_stability_subset(
                    subset_df,
                    min_nb_points=input_parameters.short_term_stability_required_measurements,
                    interval_seconds=input_parameters.short_term_stability_measurement_interval_seconds,
                    tolerance_seconds=0.1,
                )
                long_term_stability_df = _find_stability_subset(
                    subset_df,
                    min_nb_points=input_parameters.long_term_stability_required_measurements,
                    interval_seconds=input_parameters.long_term_stability_measurement_interval_seconds,
                    tolerance_seconds=1.0,
                )

                if basic_stats_df is None:
                    logging.error("No basic statistics can be computed.")
                elif len(basic_stats_df) == 1:
                    logging.warning(
                        "Only one measurement was found to compute statistics. Limited statistics will be computed."
                    )
                    subset_key_measurements |= _compute_basic_measurement(basic_stats_df)
                elif len(basic_stats_df) > 1:
                    logging.info("Computing basic statistics.")
                    subset_key_measurements |= _compute_basic_measurement(basic_stats_df)
                else:
                    logging.error(
                        "Could not determine which measurements to use for basic statistics."
                    )

                if linearity_df is None:
                    logging.warning("No linearity measurements can be computed.")
                else:
                    logging.info("Computing linearity statistics.")
                    subset_key_measurements |= _compute_linearity(linearity_df)

                if short_term_stability_df is None:
                    logging.warning("No short term stability measurements can be computed.")
                else:
                    logging.info("Computing short term stability statistics.")
                    res = _compute_stability(short_term_stability_df)
                    subset_key_measurements["short_term_power_stability_start_datetime"] = res[
                        "stability_start_datetime"
                    ]
                    subset_key_measurements["short_term_power_stability_end_datetime"] = res[
                        "stability_end_datetime"
                    ]
                    subset_key_measurements["short_term_power_stability"] = res["power_stability"]

                if long_term_stability_df is None:
                    logging.warning("No long term stability measurements can be computed.")
                else:
                    logging.info("Computing long term stability statistics.")
                    res = _compute_stability(long_term_stability_df)
                    subset_key_measurements["long_term_power_stability_start_datetime"] = res[
                        "stability_start_datetime"
                    ]
                    subset_key_measurements["long_term_power_stability_end_datetime"] = res[
                        "stability_end_datetime"
                    ]
                    subset_key_measurements["long_term_power_stability"] = res["power_stability"]

                key_measurements.append(subset_key_measurements)

    key_measurements = [mm_schema.LightSourcePowerKeyMeasurement(**km) for km in key_measurements]

    return key_measurements


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
