from setuptools import setup, find_packages

setup(
    name='LorenFranksDataMigration',
    version='0.1.003',
    author='Novela Neurotech',
    url="https://github.com/NovelaNeuro/lfdatamigration",
    packages=find_packages(),
    package_data={'': ['logging.conf']},
    description='Data transformation from rec binary files into NWB 2.0 format',
    platforms='Posix; MacOS X; Windows',
    python_requires='==3.7.4',
)
