#!/bin/bash

export PKG_NAME=rec_to_nwb
export ANACONDA_API_TOKEN=$CONDA_UPLOAD_TOKEN
export CONDA_BUILD_PATH=/home/travis/miniconda/envs/test-environment/conda-bld

conda config --set anaconda_upload no

echo "Build missing pypi packages..."
conda skeleton pypi rec_to_binaries --version 0.5.1.dev0 --recursive
conda skeleton pypi xmldiff --recursive
conda skeleton pypi mountainlab_pytools --recursive

echo "Build missing pypi packages into conda packages..."
conda build rec_to_binaries
conda build xmldiff
conda build mountainlab_pytools

echo "Convert  missing pypi packages ..."
conda convert --platform osx-64 $CONDA_BUILD_PATH/linux-64/***.tar.bz2 --output-dir $CONDA_BUILD_PATH -q
conda convert --platform linux-32 $CONDA_BUILD_PATH/linux-64/***.tar.bz2 --output-dir $CONDA_BUILD_PATH -q
conda convert --platform linux-64 $CONDA_BUILD_PATH/linux-64/***.tar.bz2 --output-dir $CONDA_BUILD_PATH -q
conda convert --platform win-32 $CONDA_BUILD_PATH/linux-64/***.tar.bz2 --output-dir $CONDA_BUILD_PATH -q
conda convert --platform win-64 $CONDA_BUILD_PATH/linux-64/***.tar.bz2 --output-dir $CONDA_BUILD_PATH -q

echo "Upload  missing pypi packages to anaconda..."
anaconda upload $CONDA_BUILD_PATH/**/rec_to_binaries-*.tar.bz2 --force
anaconda upload $CONDA_BUILD_PATH/**/xmldiff-*.tar.bz2 --force
anaconda upload $CONDA_BUILD_PATH/**/mountainlab_pytools-*.tar.bz2 --force
