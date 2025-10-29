from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("microscopemetrics")
except PackageNotFoundError:
    # package not installed
    __version__ = "0.0.0"
