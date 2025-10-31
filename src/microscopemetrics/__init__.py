__version__ = "0.0.0"

import logging

logger = logging.getLogger(__name__)


class AnalysisError(Exception):
    def __init__(self, message, suggestion=None):
        super().__init__(message)
        self.suggestion = suggestion


class DataFormatError(AnalysisError):
    def __init__(self, message, suggestion=None):
        super().__init__(message, suggestion)


class SaturationError(AnalysisError):
    def __init__(self, message, suggestion=None):
        super().__init__(message, suggestion)


class FittingError(AnalysisError):
    def __init__(self, message, suggestion=None):
        super().__init__(message, suggestion)


class SNRError(AnalysisError):
    def __init__(self, message, suggestion=None):
        super().__init__(message, suggestion)
