__version__ = "0.3.0"

import logging

logger = logging.getLogger(__name__)


class InconsistentDataError(Exception):
    pass


class AnalysisError(Exception):
    pass


class SaturationError(AnalysisError):
    pass


class FittingError(AnalysisError):
    pass
