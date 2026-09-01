"""
This module maps the sample classes to the analysis functions and the dataset classes.
"""

from collections import namedtuple

from microscopemetrics_schema import datamodel as mm_schema

from microscopemetrics.analyses import (
    co_registration,
    field_illumination,
    light_source_power,
    psf_beads,
)

Mapping = namedtuple("Mapping", ["analysis_function", "sample_classes"])

MAPPINGS = {
    mm_schema.FieldIlluminationDataset.class_class_curie: Mapping(
        analysis_function=field_illumination.analyse_field_illumination,
        sample_classes=[
            mm_schema.FluorescentHomogeneousThinField,
            mm_schema.FluorescentHomogeneousThickField,
        ],
    ),
    mm_schema.PSFBeadsDataset.class_class_curie: Mapping(
        analysis_function=psf_beads.analyse_psf_beads,
        sample_classes=[mm_schema.PSFBeads],
    ),
    mm_schema.LightSourcePowerDataset.class_class_curie: Mapping(
        analysis_function=light_source_power.analyse_light_source_power, sample_classes=[]
    ),
    mm_schema.CoRegistrationDataset.class_class_curie: Mapping(
        analysis_function=co_registration.analyse_co_registration,
        sample_classes=[mm_schema.MultiWavelengthBeads],
    ),
    mm_schema.MicroscopeMetricsDataset.class_class_curie: Mapping(
        analysis_function=microscope_metrics.analyse_stage_drift,
        sample_classes=[mm_schema.NonPSFBeads],
    ),
}

# TEST = {
#     mm_schema.FieldIlluminationDataset: {
#         "sample_class": [
#             mm_schema.FluorescentHomogeneousThinField,
#             mm_schema.FluorescentHomogeneousThickField,
#         ],
#         "analysis_function": [
#             field_illumination.analyse_field_illumination,
#             field_illumination.analyse_field_illumination,
#         ],
#     },
#     mm_schema.PSFBeadsDataset: {
#         "sample_class": [
#             mm_schema.PSFBeads,
#         ],
#         "analysis_function": [
#             psf_beads.analyse_psf_beads,
#         ],
#     },
# }
#
