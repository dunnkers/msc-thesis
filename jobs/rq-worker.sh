#!/bin/bash
#SBATCH --time=02:00:00
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --partition=regular
#SBATCH --mem=10000
#SBATCH --output=/data/s2995697/slurm/logs/slurm-%A_%a.out

echo "Spawning a job to upload logs, as a dependency on this job:"
sbatch \
    --dependency=afterany:$SLURM_JOB_ID \
    --export=SACCT_JOB_ID=$SLURM_JOB_ID \
    src/sacct_to_wandb.sh

echo "Running worker in directory:"
pwd

module load Python
python -m venv venv
source venv/bin/activate
pip uninstall fseval --yes
pip install git+https://github.com/dunnkers/fseval.git@2.0
rq worker -u $REDIS_URL