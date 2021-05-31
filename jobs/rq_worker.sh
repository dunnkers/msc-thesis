#!/bin/bash
#SBATCH --time=20:00:00
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --partition=regular
#SBATCH --mem=10000
#SBATCH --chdir=/scratch/s2995697/fseval/
#SBATCH --output=/data/s2995697/slurm/logs/slurm-%A_%a.out

echo "Spawning a job to upload logs, as a dependency on this job (id $SLURM_JOB_ID):"
sbatch \
    --dependency=afterany:$SLURM_JOB_ID \
    --export=SACCT_JOB_ID=$SLURM_JOB_ID \
    ~/msc-thesis/jobs/upload_logs.sh

echo "Running worker in directory:"
pwd

sh ~/msc-thesis/jobs/_prepare_env.sh
rq worker -u $REDIS_URL