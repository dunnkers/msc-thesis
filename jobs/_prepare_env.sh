#!/bin/bash
echo "preparing fseval environment in directory:"
pwd
module load Python/3.8.6-GCCcore-10.2.0

venv_dir=$TMPDIR/venv_$SLURM_JOB_ID
echo "creating clean \u001b[33mvirtual environment\u001b[0m (in $venv_dir)..."
rm -rf $venv_dir
python -m venv $venv_dir
source $venv_dir/bin/activate
echo "virtual environment created \u001b[32m ✓ \u001b[0m"

echo "upgrading \u001b[33mpip\u001b[0m..."
python -m pip install --upgrade pip --quiet
echo "pip upgraded \u001b[32m✓\u001b[0m"

echo "installing \u001b[33mhydra rq launcher\u001b[0m..."
pip install -e git+https://github.com/dunnkers/hydra.git@plugins/rq-launcher/fail-hard#"egg=hydra_rq_launcher&subdirectory=plugins/hydra_rq_launcher"  --quiet
echo "hydra rq launcher installed \u001b[32m✓\u001b[0m"

echo "installing \u001b[33mfseval\u001b[0m..."
pip install git+https://github.com/dunnkers/fseval.git@master --quiet
echo "fseval installed \u001b[32m✓\u001b[0m"
