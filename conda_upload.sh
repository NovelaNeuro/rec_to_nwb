#!/bin/bash

export PKG_NAME=fldatamigration

conda config --set anaconda_upload no
export ANACONDA_API_TOKEN=$CONDA_UPLOAD_TOKEN

echo "Building conda package..."
conda build . --no-include-recipe || exit 1
export CONDA_BUILD_PATH=/home/travis/miniconda/envs/test-environment/conda-bld

echo "Converting conda package..."
conda convert --platform osx-64 $CONDA_BUILD_PATH/linux-64/***.tar.bz2 --output-dir $CONDA_BUILD_PATH -q || exit 1
conda convert --platform linux-32 $CONDA_BUILD_PATH/linux-64/***.tar.bz2 --output-dir $CONDA_BUILD_PATH -q || exit 1
conda convert --platform linux-64 $CONDA_BUILD_PATH/linux-64/***.tar.bz2 --output-dir $CONDA_BUILD_PATH -q || exit 1
conda convert --platform win-32 $CONDA_BUILD_PATH/linux-64/***.tar.bz2 --output-dir $CONDA_BUILD_PATH -q || exit 1
conda convert --platform win-64 $CONDA_BUILD_PATH/linux-64/***.tar.bz2 --output-dir $CONDA_BUILD_PATH -q || exit 1

echo "Deploying to Anaconda.org..."
anaconda upload $CONDA_BUILD_PATH/**/fldatamigration-*.tar.bz2 --force || exit 1


