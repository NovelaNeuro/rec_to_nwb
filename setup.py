version = '0.1.006'
print(version)
from setuptools import setup, find_packages


setup(
    name='fldatamigration',
    version=version,
    author='Novela Neurotech',
    url="https://github.com/NovelaNeuro/fldatamigration",
    packages=find_packages(),
    package_data={'': ['logging.conf', 'data/fl_lab_header.xsd', 'data/reconfig_header.xsd']},
    description='Data transformation from rec binary files into NWB 2.0 format',
    platforms='Posix; MacOS X; Windows',
    python_requires='==3.7.4',
)
