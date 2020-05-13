#!/bin/bash
source ~/miniconda3/etc/profile.d/conda.sh

conda deactivate

echo "Creating new env"
conda create --name test_rec_to_nwb -y --force

conda list

conda activate test_rec_to_nwb
#conda install rec_to_nwb -c novelakrk
conda install fldatamigration -c novelakrk -y

conda list