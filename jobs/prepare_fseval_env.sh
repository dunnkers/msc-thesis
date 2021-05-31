#!/bin/bash
cd /scratch/s2995697/fseval/

module load Python/3.8.6-GCCcore-10.2.0
venv_dir=$TMPDIR/venv_$SLURM_JOB_ID
rm -rf $venv_dir
python -m venv $venv_dir
source $venv_dir/bin/activate
python -m pip install --upgrade pip
pip install -e git+https://github.com/dunnkers/hydra.git@plugins/rq-launcher/fail-hard#"egg=hydra_rq_launcher&subdirectory=plugins/hydra_rq_launcher"
pip install -e git+https://github.com/facebookresearch/hydra.git@master#"egg=hydra_submitit_launcher&subdirectory=plugins/hydra_submitit_launcher"
pip install git+https://github.com/dunnkers/fseval.git@master
