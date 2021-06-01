#!/bin/bash
echo "preparing \e[33mfseval environment\e[0m in directory:"
pwd

module load Python/3.8.6-GCCcore-10.2.0
venv_dir=$TMPDIR/venv_${SLURM_JOB_ID}_${SLURM_ARRAY_TASK_ID}

echo -e "creating clean \e[33mvirtual environment\e[0m (in $venv_dir)..."
rm -rf $venv_dir
python -m venv $venv_dir
source $venv_dir/bin/activate
echo -e "virtual environment created  \e[32m✓\e[0m"

echo -e "upgrading \e[33mpip\e[0m..."
python -m pip install --upgrade pip --quiet
echo -e "pip upgraded \e[32m✓\e[0m"

echo -e "installing \e[33mhydra rq launcher\e[0m..."
pip install -e git+https://github.com/dunnkers/hydra.git@plugins/rq-launcher/fail-hard#"egg=hydra_rq_launcher&subdirectory=plugins/hydra_rq_launcher"  --quiet
echo -e "hydra rq launcher installed \e[32m✓\e[0m"

echo -e "installing \e[33mfseval\e[0m..."
pip install git+https://github.com/dunnkers/fseval.git@master --quiet
echo -e "fseval installed \e[32m✓\e[0m"
