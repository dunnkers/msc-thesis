#!/bin/bash
module load Python/3.8.6-GCCcore-10.2.0
venv_dir=$TMPDIR/venv_$SLURM_JOB_ID
python -m venv $venv_dir
source $venv_dir/bin/activate
pip install -e git+https://github.com/dunnkers/hydra.git@master#egg=hydra_rq_launcher&subdirectory=plugins/hydra_rq_launcher
pip install git+https://github.com/dunnkers/fseval.git@master