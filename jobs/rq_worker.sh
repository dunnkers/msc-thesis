#!/bin/bash
#SBATCH --time=20:00:00
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --partition=regular
#SBATCH --mem=10000
#SBATCH --chdir=/scratch/s2995697/fseval/
#SBATCH --output=/data/s2995697/slurm/logs/slurm-%A_%a.out

if [ -n "${SLURM_ARRAY_JOB_ID+set}" ]; then
    job_id=$SLURM_ARRAY_JOB_ID
else
    job_id=$SLURM_JOB_ID
fi
echo "This job has id: $job_id"

echo "Spawning a job to upload logs, as a dependency on this job."
sbatch \
    --dependency=afterany:$job_id \
    --export=SACCT_JOB_ID=$job_id \
    ~/msc-thesis/jobs/upload_logs.sh

echo "Requesting to prepare the worker environment..."
sh ~/msc-thesis/jobs/_prepare_env.sh

echo "Running rq worker..."
rq worker -u $REDIS_URL