# PyLasaDataset [![PyPI](https://img.shields.io/pypi/v/pylasadataset?color=blue)](https://pypi.org/project/pylasadataset/) [![CI](https://github.com/justagist/pyLasaDataset/actions/workflows/ci.yml/badge.svg)](https://github.com/justagist/pyLasaDataset/actions/workflows/ci.yml)

[LASA Handwriting dataset](https://github.com/epfl-lasa/LASAHandwritingDataset) loader and other tools for Python (3.9+).

The raw dataset is downloaded automatically from the official
[epfl-lasa/LASAHandwritingDataset](https://github.com/epfl-lasa/LASAHandwritingDataset)
repository the first time it is used, and cached locally (default:
`~/.cache/pyLasaDataset`; override with the `PYLASADATASET_DATA_DIR`
environment variable).

## Installation

```bash
pip install pylasadataset
```

Or directly from source:

```bash
pip install git+https://github.com/justagist/pylasadataset
```

## Usage

```python
import pyLasaDataset as lasa

# DataSet object has all the LASA handwriting data files
# as attributes, eg:
angle_data = lasa.DataSet.Angle
sine_data = lasa.DataSet.Sine

# List all available patterns:
print(lasa.DataSet.names)

# Each Data object has attributes dt and demos (For documentation,
# refer original dataset repo:
# https://github.com/epfl-lasa/LASAHandwritingDataset/blob/master/Readme.txt)
dt = angle_data.dt
demos = angle_data.demos # list of 7 Demo objects, each corresponding to a
                         # repetition of the pattern

# Each Demo object in demos list will have attributes pos, t, vel, acc
# corresponding to the original .mat format described in
# https://github.com/epfl-lasa/LASAHandwritingDataset/blob/master/Readme.txt
demo_0 = demos[0]
pos = demo_0.pos # np.ndarray, shape: (2,1000)
vel = demo_0.vel # np.ndarray, shape: (2,1000)
acc = demo_0.acc # np.ndarray, shape: (2,1000)
t = demo_0.t # np.ndarray, shape: (1,1000)

# To visualise the data (2D position and velocity) use the plot_model utility
lasa.utilities.plot_model(lasa.DataSet.BendedLine) # give any of the available
                                                   # pattern data as argument
```

## Development

```bash
pip install -e .[test]
pytest
```

## Acknowledgements

The LASA Handwriting Dataset is created and maintained by the
[LASA lab at EPFL](https://www.epfl.ch/labs/lasa/). See the
[dataset repository](https://github.com/epfl-lasa/LASAHandwritingDataset) for
its terms of use and citation information.
