#!/bin/bash
#SBATCH --time=00:15:00
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --partition=short
#SBATCH --job-name=logs-uploader
#SBATCH --mem=2500
#SBATCH --chdir=/scratch/s2995697/fseval/
#SBATCH --output=/data/s2995697/slurm/logs/slurm-%A_%a.out

echo "Uploading logs for job: $SACCT_JOB_ID (this job has id $SLURM_JOB_ID)"
module load Python/3.8.6-GCCcore-10.2.0
venv_dir=$TMPDIR/venv_$SLURM_JOB_ID
python -m venv $venv_dir
source $venv_dir/bin/activate
pip install git+https://github.com/dunnkers/slurm-to-wandb.git@master
slurm_to_wandb $SACCT_JOB_ID
