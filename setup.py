# from setup_reqs import use_setuptools
# use_setuptools()
import os, subprocess
from setuptools import setup, find_packages
from distutils.core import setup

# print "THIS\n\n"
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

def clone_repo():

    process = subprocess.Popen(['git', 'clone', 'https://bitbucket.org/khansari/lasahandwritingdataset.git', 'pyLasaDataset/resources/LASAHandwritingDataset'], 
                           stdout=subprocess.PIPE,
                           universal_newlines=True)

    while True:
        output = process.stdout.readline()
        print(output.strip())
        # Do something else
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
    version = "0.1",
    author = "JustaGist",
    author_email = "saifksidhik@gmail.com",
    description = ("Simulation environments and experiments for comparing different variable impedance control strategies used for robot manipulation."),
    license = "Apache 2.0",
    keywords = "handwriting dataset, python",
    url = "https://github.com/justagist/pyLasaDataset",
    packages=find_packages(),
    # scripts=['scripts/sign_package'],
    install_requires=[
       'scipy', 'numpy', 'matplotlib'
      ],
    long_description=read('README.md'),
    classifiers=[],
    # package_data={'': ['config/sample_signature.txt']},
    include_package_data=True,
    #     "Development Status :: 3 - Alpha",
    #     "Topic :: Utilities",
    #     "License :: OSI Approved :: BSD License",
    # ],
)


# os.system("export VAR_IMP_EXP_PATH=this")
# os.environ['VAR_IMP_EXP_PATH'] = "this"