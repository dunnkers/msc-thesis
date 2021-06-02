#!/bin/bash
echo "preparing fseval environment in directory:"
pwd

module load Python/3.8.6-GCCcore-10.2.0
venv_dir=$TMPDIR/venv_${SLURM_JOB_ID}_${SLURM_ARRAY_TASK_ID}

echo "creating clean virtual environment (in $venv_dir)..."
rm -rf $venv_dir
python -m venv $venv_dir
source $venv_dir/bin/activate
echo "virtual environment created  ✓"

echo "upgrading pip..."
python -m pip install --quiet --upgrade pip
echo "pip upgraded ✓"

echo "installing hydra rq launcher..."
pip install --quiet git+https://github.com/dunnkers/hydra.git@plugins/rq-launcher/fail-hard#"egg=hydra_rq_launcher&subdirectory=plugins/hydra_rq_launcher"
echo "hydra rq launcher installed ✓"

echo "installing fseval..."
pip install --quiet git+https://github.com/dunnkers/fseval.git@master
echo "fseval installed ✓"

echo "installing fseval estimators..."
pip install --quiet \
    pytorch-tabnet==3.1.1 \
    skrebate==0.62 \
    xgboost==1.4.2 \
    Boruta==0.3 \
    featboost @ git+https://github.com/dunnkers/FeatBoost.git@support-cloning \
    stability-selection @ git+https://github.com/dunnkers/stability-selection.git@master \
    matplotlib==3.4.2 \
echo "fseval estimators installed ✓"