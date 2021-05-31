#!/bin/bash
echo "preparing fseval environment in directory:"
pwd
module load Python/3.8.6-GCCcore-10.2.0

venv_dir=$TMPDIR/venv_$job_id
echo "creating clean virtual environment (in $venv_dir)..."
rm -rf $venv_dir
python -m venv $venv_dir
source $venv_dir/bin/activate
echo "virtual environment created  ✓"

echo "upgrading pip.."
python -m pip install --upgrade pip --quiet
echo "pip upgraded ✓"

echo "installing hydra rq launcher.."
pip install -e git+https://github.com/dunnkers/hydra.git@plugins/rq-launcher/fail-hard#"egg=hydra_rq_launcher&subdirectory=plugins/hydra_rq_launcher"  --quiet
echo "hydra rq launcher installed ✓"

echo "installing fseval.."
pip install git+https://github.com/dunnkers/fseval.git@master --quiet
echo "fseval installed ✓"
