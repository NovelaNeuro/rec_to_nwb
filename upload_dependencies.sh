#!/bin/bash

export PKG_NAME=rec_to_nwb
export ANACONDA_API_TOKEN=wb-5fbc6785-4006-4a9d-8eb7-c9d640e330e4
export CONDA_BUILD_PATH=/home/travis/miniconda/envs/test-environment/conda-bld

conda config --set anaconda_upload no

echo "Build missing pypi packages..."
conda skeleton pypi rec_to_binaries --version 0.5.1.dev0
conda skeleton pypi xmldiff
conda skeleton pypi vdom
conda skeleton pypi jp_proxy_widget
conda skeleton pypi jupyter-ui-poll
conda skeleton pypi mountainlab_pytools

echo "Build missing pypi packages into conda packages..."
conda build rec_to_binaries
conda build xmldiff
conda build vdom
conda build jp_proxy_widget
conda build jupyter-ui-poll
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
anaconda upload $CONDA_BUILD_PATH/**/vdom-*.tar.bz2 --force
anaconda upload $CONDA_BUILD_PATH/**/jp_proxy_widget-*.tar.bz2 --force
anaconda upload $CONDA_BUILD_PATH/**/jupyter-ui-poll-*.tar.bz2 --force
anaconda upload $CONDA_BUILD_PATH/**/mountainlab_pytools-*.tar.bz2 --force

