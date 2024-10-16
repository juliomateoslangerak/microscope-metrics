"""
This module maps the sample classes to the analysis functions and the dataset classes.
"""

from collections import namedtuple

from microscopemetrics_schema import datamodel as mm_schema

from microscopemetrics.analyses import field_illumination, psf_beads

Mapping = namedtuple("Mapping", ["sample_class", "analysis_function", "dataset_class"])

MAPPINGS = [
    Mapping(
        mm_schema.FluorescentHomogeneousThinField,
        field_illumination.analyse_field_illumination,
        mm_schema.FieldIlluminationDataset,
    ),
    Mapping(
        mm_schema.FluorescentHomogeneousThickField,
        field_illumination.analyse_field_illumination,
        mm_schema.FieldIlluminationDataset,
    ),
    Mapping(mm_schema.PSFBeads, psf_beads.analyse_psf_beads, mm_schema.PSFBeadsDataset),
]

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
