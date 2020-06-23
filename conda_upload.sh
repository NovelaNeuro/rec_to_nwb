#!/bin/bash

export PKG_NAME=rec_to_nwb
export ANACONDA_API_TOKEN=$CONDA_UPLOAD_TEST_TOKEN
export VERSION=$(python setup.py)
export CONDA_BUILD_PATH=/home/travis/miniconda/envs/test-environment/conda-bld
export BASE_PATH=$(pwd)

conda config --set anaconda_upload no

echo "Building conda package..."
conda build . -c acwikla-novela -c novelakrk -c conda-forge --no-include-recipe --python 3.6 || exit 1

echo "Move conda package..."
mv ${CONDA_BUILD_PATH}/linux-64/${PKG_NAME}-${VERSION}-*.tar.bz2 ${CONDA_BUILD_PATH} || exit 1

echo "Making new_tar dir..."
mkdir ${CONDA_BUILD_PATH}/new_tar || exit 1

echo "Extracting conda package..."
tar -xf ${CONDA_BUILD_PATH}/${PKG_NAME}-${VERSION}-*.tar.bz2 -C ${CONDA_BUILD_PATH}/new_tar || exit 1

cd ${CONDA_BUILD_PATH}/new_tar || exit 1

echo "Creating new conda package without some files..."
tar -cjvf ${PKG_NAME}-${VERSION}-*.tar.bz2 --exclude=info/recipe/rec_to_nwb/test --exclude=info/recipe/rec_to_nwb/scripts --exclude='*.sh' --exclude='*.gitignore' --exclude='*.pytest_cache' --exclude='*.gitignore' info lib || exit 1

cd ..

echo "Move conda package to linux dir..."
mv new_tar/${PKG_NAME}-${VERSION}-*.tar.bz2 linux-64 || exit 1

echo "Converting conda package..."
conda convert --platform osx-64 $CONDA_BUILD_PATH/linux-64/${PKG_NAME}-${VERSION}-*.tar.bz2 --output-dir $CONDA_BUILD_PATH -q || exit 1
conda convert --platform linux-32 $CONDA_BUILD_PATH/linux-64/${PKG_NAME}-${VERSION}-*.tar.bz2 --output-dir $CONDA_BUILD_PATH -q || exit 1
conda convert --platform linux-64 $CONDA_BUILD_PATH/linux-64/${PKG_NAME}-${VERSION}-*.tar.bz2 --output-dir $CONDA_BUILD_PATH -q || exit 1
conda convert --platform win-32 $CONDA_BUILD_PATH/linux-64/${PKG_NAME}-${VERSION}-*.tar.bz2 --output-dir $CONDA_BUILD_PATH -q || exit 1
conda convert --platform win-64 $CONDA_BUILD_PATH/linux-64/${PKG_NAME}-${VERSION}-*.tar.bz2 --output-dir $CONDA_BUILD_PATH -q || exit 1

echo "Deploying to Anaconda.org..."
anaconda upload $CONDA_BUILD_PATH/**/${PKG_NAME}-${VERSION}-*.tar.bz2 --force || exit 1
