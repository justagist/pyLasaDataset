"""Loader for the LASA Handwriting Dataset.

The raw ``.mat`` files are downloaded automatically from
https://github.com/epfl-lasa/LASAHandwritingDataset on first use and cached
locally (default: ``~/.cache/pyLasaDataset``; override with the
``PYLASADATASET_DATA_DIR`` environment variable).
"""

import io
import os
import shutil
import time
import zipfile
from functools import lru_cache
from urllib.request import urlopen

import numpy as np
from scipy.io import loadmat

DATASET_URL = (
    "https://github.com/epfl-lasa/LASAHandwritingDataset/archive/refs/heads/master.zip"
)

# Legacy location used by pyLasaDataset <= 0.1.x, where the dataset was
# bundled inside the installed package. Still honoured if present.
_LEGACY_DATASET_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "resources",
    "LASAHandwritingDataset",
    "DataSet",
)


def _default_cache_dir():
    env_dir = os.environ.get("PYLASADATASET_DATA_DIR")
    if env_dir:
        return env_dir
    xdg_cache = os.environ.get(
        "XDG_CACHE_HOME", os.path.join(os.path.expanduser("~"), ".cache")
    )
    return os.path.join(xdg_cache, "pyLasaDataset")


def _download_dataset(target_dir):
    """Download the dataset zip from GitHub and extract the .mat files."""
    print(
        "pyLasaDataset: downloading LASA Handwriting Dataset from {} ...".format(
            DATASET_URL
        )
    )
    attempts = 3
    for attempt in range(1, attempts + 1):
        try:
            with urlopen(DATASET_URL) as response:
                archive = io.BytesIO(response.read())
            break
        except Exception as exc:
            if attempt == attempts:
                raise IOError(
                    "Failed to download LASA dataset from {} after {} "
                    "attempts: {}".format(DATASET_URL, attempts, exc)
                )
            print(
                "pyLasaDataset: download failed ({}), retrying ({}/{})...".format(
                    exc, attempt, attempts
                )
            )
            time.sleep(2 * attempt)

    tmp_dir = target_dir + ".tmp"
    if os.path.isdir(tmp_dir):
        shutil.rmtree(tmp_dir)
    os.makedirs(tmp_dir)
    with zipfile.ZipFile(archive) as zf:
        for member in zf.namelist():
            # members look like 'LASAHandwritingDataset-master/DataSet/Angle.mat'
            parts = member.split("/")
            if len(parts) == 3 and parts[1] == "DataSet" and parts[2].endswith(".mat"):
                with (
                    zf.open(member) as src,
                    open(os.path.join(tmp_dir, parts[2]), "wb") as dst,
                ):
                    shutil.copyfileobj(src, dst)

    if not any(f.endswith(".mat") for f in os.listdir(tmp_dir)):
        shutil.rmtree(tmp_dir)
        raise IOError(
            "Downloaded archive from {} did not contain any .mat files.".format(
                DATASET_URL
            )
        )
    # Atomic-ish swap so an interrupted download never leaves a half-filled
    # directory behind to be mistaken for a valid cache.
    if os.path.isdir(target_dir):
        shutil.rmtree(target_dir)
    os.replace(tmp_dir, target_dir)
    print("pyLasaDataset: dataset cached at {}".format(target_dir))


@lru_cache(maxsize=1)
def _dataset_path():
    """Return the directory containing the .mat files, downloading if needed."""
    if os.path.isdir(_LEGACY_DATASET_PATH):
        return _LEGACY_DATASET_PATH
    cache_dir = _default_cache_dir()
    if not (
        os.path.isdir(cache_dir)
        and any(f.endswith(".mat") for f in os.listdir(cache_dir))
    ):
        _download_dataset(cache_dir)
    return cache_dir


def _available_names():
    return sorted(f[:-4] for f in os.listdir(_dataset_path()) if f.endswith(".mat"))


class _Demo(object):
    """
    Each demo object has attributes:

    pos : 2D cartesian position data. shape: (2,1000)
    t   : corresponding time for each data point. shape: (1,1000)
    vel : 2D cartesian velocity data for motion. shape: (2,1000)
    acc : 2D cartesian acceleration data for motion. shape: (2,1000)

    """

    def __init__(self, demo):
        typelist = str(np.asarray(demo[0][0].dtype))
        typelist = typelist[1:-2].split(", ")
        idx = 0
        for att in typelist:
            if "'O'" in att:
                continue
            else:
                setattr(self, att[2:-1], demo[0][0][idx])
                idx += 1

        assert idx == 5, "Reading data for demo failed"


class _Data(object):
    """
    Data object for each pattern has the following two attributes:

    dt : the average time steps across all demonstrations for this pattern
    demos : array of _Demo objects (len: 7) corresponding the trials for this pattern

    """

    def __init__(self, matdata, name):
        self.name = name
        self.dt = matdata["dt"][0][0]
        self.demos = [_Demo(d) for d in matdata["demos"][0]]

        assert len(self.demos) == 7, (
            "ERROR: Data for matdata could not be read properly."
        )

    def __repr__(self):
        return str({"dt": self.dt, "demos": self.demos})

    @classmethod
    @lru_cache(maxsize=None)
    def get_data(cls, name):
        return cls(loadmat(os.path.join(_dataset_path(), name + ".mat")), name)


class _PyLasaDataSet(object):
    def __getattr__(self, name):
        if name.startswith("_"):
            raise AttributeError(name)
        if name in _available_names():
            return _Data.get_data(name)
        raise AttributeError(
            "DataSet has no data named '{}'. Available: {}".format(
                name, ", ".join(_available_names())
            )
        )

    def __dir__(self):
        return list(super().__dir__()) + _available_names()

    @property
    def names(self):
        """List of all available pattern names."""
        return _available_names()


DataSet = _PyLasaDataSet()
