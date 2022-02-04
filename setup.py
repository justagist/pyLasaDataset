# from setup_reqs import use_setuptools
# use_setuptools()
import os, subprocess
from setuptools import setup, find_packages
from distutils.core import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

def clone_repo():

    process = subprocess.Popen(['git', 'clone', 'https://bitbucket.org/khansari/lasahandwritingdataset.git', 'pyLasaDataset/resources/LASAHandwritingDataset'], 
                           stdout=subprocess.PIPE,
                           universal_newlines=True)

    while True:
        output = process.stdout.readline()
        print(output.strip())
        return_code = process.poll()
        if return_code is not None:
            print('RETURN CODE', return_code)
            # Process has finished, read rest of the output 
            for output in process.stdout.readlines():
                print(output.strip())
            break

clone_repo()

setup(
    name = "pyLasaDataset",
    version = "0.1.1",
    author = "Saif Sidhik",
    author_email = "mail@saifsidhik.page",
    description = ("LASA Handwriting dataset loader and other tools for Python."),
    long_description_content_type="text/markdown",
    long_description=read("README.md"),
    license = "Public Domain",
    keywords = "handwriting dataset, python",
    url = "https://github.com/justagist/pyLasaDataset",
    project_urls = {
        "Bug Tracker": "https://github.com/justagist/pylasadataset/issues",
        "Documentation": "https://github.com/justagist/pyLasaDataset/blob/master/README.md",
        "Source Code": "https://github.com/justagist/pylasadataset",
    },
    classifiers=[
        "License :: Public Domain",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    packages=find_packages(),
    install_requires=[
       'scipy', 'numpy', 'matplotlib'
      ],
    include_package_data=True,
)
