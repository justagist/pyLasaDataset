# PyLasaDataset [![PyPI](https://img.shields.io/pypi/v/pylasadataset?color=blue)](https://pypi.org/project/pylasadataset/)

[LASA Handwriting dataset](https://bitbucket.org/khansari/lasahandwritingdataset) loader and other tools for Python 2 and Python 3.

## Installation

### Via pip

`python3 -m pip install pylasadataset`

Or 

`python3 -m pip install git+https://github.com/justagist/pylasadataset`


### Manual Install

- Dependencies: `apt install python-tk`; `pip install numpy scipy matplotlib`.
- Run `python setup.py install`.

## Usage

```python

import pyLasaDataset as lasa

# DataSet object has all the LASA handwriting data files 
# as attributes, eg:
angle_data = lasa.DataSet.Angle
sine_data = lasa.DataSet.Sine


# Each Data object has attributes dt and demos (For documentation, 
# refer original dataset repo: 
# https://bitbucket.org/khansari/lasahandwritingdataset/src/master/Readme.txt)
dt = angle_data.dt
demos = angle_data.demos # list of 7 Demo objects, each corresponding to a 
                         # repetition of the pattern


# Each Demo object in demos list will have attributes pos, t, vel, acc 
# corresponding to the original .mat format described in 
# https://bitbucket.org/khansari/lasahandwritingdataset/src/master/Readme.txt
demo_0 = demos[0]
pos = demo_0.pos # np.ndarray, shape: (2,2000)
vel = demo_0.vel # np.ndarray, shape: (2,2000) 
acc = demo_0.acc # np.ndarray, shape: (2,2000)
t = demo_0.t # np.ndarray, shape: (1,2000)


# To visualise the data (2D position and velocity) use the plot_model utility
lasa.utilities.plot_model(lasa.DataSet.BendedLine) # give any of the available 
                                                   # pattern data as argument

```
