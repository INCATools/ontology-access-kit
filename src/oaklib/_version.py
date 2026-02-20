from importlib import metadata

try:
    __version__ = metadata.version(__package__)
except metadata.PackageNotFoundError:
    # package is not installed
    __version__ = "0.0.0"  