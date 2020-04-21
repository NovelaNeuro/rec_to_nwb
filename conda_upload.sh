#!/bin/bash

export PKG_NAME=fldatamigration

conda config --set anaconda_upload no
export ANACONDA_API_TOKEN=$CONDA_UPLOAD_TEST_TOKEN
export VERSION=$(python setup.py)
export CONDA_BUILD_PATH=/home/travis/miniconda/envs/test-environment/conda-bld
export BASE_PATH=$(pwd)

echo "Build missing pypi packages..."
conda skeleton pypi ndx-fllab-novela --version 0.0.7
conda skeleton pypi pdoc --version 0.3.2
conda skeleton pypi pyvalid --version 0.9.2
conda skeleton pypi rec-to-binaries --version 0.3.0.dev0
conda skeleton pypi xmldiff --version 2.4

echo "Build missing pypi packages into conda packages..."
conda build ndx-fllab-novela
conda build pdoc
conda build pyvalid
conda build rec-to-binaries
conda build xmldiff

echo "Convert missing pypi packages ..."
conda convert --platform osx-64 $CONDA_BUILD_PATH/linux-64/***.tar.bz2 --output-dir $CONDA_BUILD_PATH -q
conda convert --platform linux-32 $CONDA_BUILD_PATH/linux-64/***.tar.bz2 --output-dir $CONDA_BUILD_PATH -q
conda convert --platform linux-64 $CONDA_BUILD_PATH/linux-64/***.tar.bz2 --output-dir $CONDA_BUILD_PATH -q
conda convert --platform win-32 $CONDA_BUILD_PATH/linux-64/***.tar.bz2 --output-dir $CONDA_BUILD_PATH -q
conda convert --platform win-64 $CONDA_BUILD_PATH/linux-64/***.tar.bz2 --output-dir $CONDA_BUILD_PATH -q

echo "Upload missing pypi packages to anaconda..."
anaconda upload $CONDA_BUILD_PATH/**/ndx-fllab-novela-*.tar.bz2 --force
anaconda upload $CONDA_BUILD_PATH/**/pdoc-*.tar.bz2 --force
anaconda upload $CONDA_BUILD_PATH/**/pyvalid-*.tar.bz2 --force
anaconda upload $CONDA_BUILD_PATH/**/rec-to-binaries-*.tar.bz2 --force
anaconda upload $CONDA_BUILD_PATH/**/xmldiff-*.tar.bz2 --force

echo "Building conda package..."
conda build . --no-include-recipe -c novelakrk || exit 1

echo "Move conda package..."
mv ${CONDA_BUILD_PATH}/linux-64/${PKG_NAME}-${VERSION}-py37_0.tar.bz2  ${CONDA_BUILD_PATH} || exit 1

echo "Making new_tar dir..."
mkdir ${CONDA_BUILD_PATH}/new_tar || exit 1

echo "Extracting conda package..."
tar -xf ${CONDA_BUILD_PATH}/${PKG_NAME}-${VERSION}-py37_0.tar.bz2 -C ${CONDA_BUILD_PATH}/new_tar || exit 1

cd ${CONDA_BUILD_PATH}/new_tar || exit 1

echo "Creating new conda package without some files..."
tar -cjvf ${PKG_NAME}-${VERSION}-py37_0.tar.bz2 --exclude=info/recipe/fl/test --exclude=info/recipe/fl/scripts --exclude='*.sh' --exclude='*.gitignore' --exclude='*.pytest_cache' --exclude='*.gitignore' info lib || exit 1

cd ..

echo "Move conda package to linux dir..."
mv new_tar/${PKG_NAME}-${VERSION}-py37_0.tar.bz2 linux-64 || exit 1

echo "Converting conda package..."
conda convert --platform osx-64 $CONDA_BUILD_PATH/linux-64/***.tar.bz2 --output-dir $CONDA_BUILD_PATH -q || exit 1
conda convert --platform linux-32 $CONDA_BUILD_PATH/linux-64/***.tar.bz2 --output-dir $CONDA_BUILD_PATH -q || exit 1
conda convert --platform linux-64 $CONDA_BUILD_PATH/linux-64/***.tar.bz2 --output-dir $CONDA_BUILD_PATH -q || exit 1
conda convert --platform win-32 $CONDA_BUILD_PATH/linux-64/***.tar.bz2 --output-dir $CONDA_BUILD_PATH -q || exit 1
conda convert --platform win-64 $CONDA_BUILD_PATH/linux-64/***.tar.bz2 --output-dir $CONDA_BUILD_PATH -q || exit 1

echo "Deploying to Anaconda.org..."
anaconda upload $CONDA_BUILD_PATH/**/$PKG_NAME-*.tar.bz2 --force || exit 1



