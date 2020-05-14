#!/bin/bash
source ~/miniconda3/etc/profile.d/conda.sh

conda deactivate
conda create -p ./env -y --force
conda activate ./env
conda install rec_to_nwb -c novelakrk
