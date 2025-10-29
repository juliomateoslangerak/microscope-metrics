__version__ = "0.0.0"

import logging

logger = logging.getLogger(__name__)


class SaturationError(Exception):
    pass


class FittingError(Exception):
    pass


class AnalysisError(Exception):
    pass
