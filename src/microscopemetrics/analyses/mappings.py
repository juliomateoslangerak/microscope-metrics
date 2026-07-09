"""
This module maps the sample classes to the analysis functions and the dataset classes.
"""

from collections import namedtuple

from microscopemetrics_schema import datamodel as mm_schema

from microscopemetrics.analyses import (
    field_illumination,
    light_source_power,
    psf_beads,
)

Mapping = namedtuple("Mapping", ["analysis_function", "sample_classes"])

MAPPINGS = {
    mm_schema.FieldIlluminationDataset.__name__: Mapping(
        analysis_function=field_illumination.analyse_field_illumination,
        sample_classes=[
            mm_schema.FluorescentHomogeneousThinField,
            mm_schema.FluorescentHomogeneousThickField,
        ],
    ),
    mm_schema.PSFBeadsDataset.__name__: Mapping(
        analysis_function=psf_beads.analyse_psf_beads,
        sample_classes=[mm_schema.PSFBeads],
    ),
    mm_schema.LightSourcePowerDataset.__name__: Mapping(
        analysis_function=light_source_power.analyse_light_source_power, sample_classes=[]
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
