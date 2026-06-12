"""LASA Handwriting dataset loader and other tools for Python."""

from importlib.metadata import PackageNotFoundError, version

from . import utilities
from .dataset import DataSet

try:
    __version__ = version("pyLasaDataset")
except PackageNotFoundError:  # running from a source checkout without install
    __version__ = "unknown"

__all__ = ["DataSet", "utilities", "__version__"]
