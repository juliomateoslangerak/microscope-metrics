from datetime import datetime
from typing import Dict, List, Tuple

import microscopemetrics_schema.datamodel as mm_schema
import numpy as np
import pandas as pd
import scipy

import microscopemetrics as mm
from microscopemetrics.analyses import tools as mm_tools


def _compute_light_source_power_key_measurements(
    power_measurements: List[mm_schema.PowerMeasurement],
    input_parameters: mm_schema.LightSourcePowerInputParameters,
) -> mm_schema.LightSourcePowerKeyMeasurements:
    power_measurement_df = pd.DataFrame([pm.dict() for pm in power_measurements])


def analyse_light_source_power(dataset: mm_schema.LightSourcePowerDataset) -> bool:
    mm.analyses.validate_requirements()

    key_measurements = None
    dataset.output = mm_schema.LightSourcePowerOutput(
        processing_application="microscopemetrics",
        processing_version=mm.__version__,
        processing_datetime=datetime.now(),
        key_measurements=key_measurements,
    )

    dataset.processed = True

    return True
