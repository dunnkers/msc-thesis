#!/bin/bash
#SBATCH --time=20:00:00
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --partition=regular
#SBATCH --mem=10000
#SBATCH --chdir=/scratch/s2995697/fseval/
#SBATCH --output=/data/s2995697/slurm/logs/slurm-%A_%a.out


echo "SLURM_ARRAY_JOB_ID=$SLURM_ARRAY_JOB_ID"
echo "SLURM_JOB_ID=$SLURM_JOB_ID"
echo "SLURM_ARRAY_TASK_ID=$SLURM_ARRAY_TASK_ID"
echo "SLURM_ARRAY_TASK_COUNT=$SLURM_ARRAY_TASK_COUNT"

sh ~/msc-thesis/jobs/_set_jobid.sh
echo "This job has id: $JOB_ID"

echo "Spawning a job to upload logs, as a dependency on this job."
sbatch \
    --dependency=afterany:$JOB_ID \
    --export=SACCT_JOB_ID=$JOB_ID \
    ~/msc-thesis/jobs/upload_logs.sh

echo "Requesting to prepare the worker environment..."
sh ~/msc-thesis/jobs/_prepare_env.sh
source $TMPDIR/venv_$JOB_ID/bin/activate

echo "Running rq worker..."
rq worker -u $REDIS_URL