#!/bin/bash
#SBATCH --time=20:00:00
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --partition=regular
#SBATCH --mem=10000
#SBATCH --chdir=/scratch/s2995697/fseval/
#SBATCH --output=/data/s2995697/slurm/logs/slurm-%A_%a.out

echo "Spawning a job to upload logs, as a dependency on this job:"
sbatch \
    --dependency=afterany:$SLURM_JOB_ID \
    --export=SACCT_JOB_ID=$SLURM_JOB_ID \
    /home/s2995697/msc-thesis/jobs/sacct_to_wandb.sh

echo "Running worker in directory:"
pwd

module load Python/3.8.6-GCCcore-10.2.0
venv_dir=$TMPDIR/venv_$SLURM_JOB_ID
python -m venv $venv_dir
source $venv_dir/bin/activate
pip install rq
pip install git+https://github.com/dunnkers/fseval.git@master
pip install -e git+https://github.com/dunnkers/hydra.git@master#egg=hydra_rq_launcher&subdirectory=plugins/hydra_rq_launcher
rq worker -u $REDIS_URL