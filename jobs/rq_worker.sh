#!/bin/bash
#SBATCH --time=20:00:00
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --partition=regular
#SBATCH --mem=10000
#SBATCH --chdir=/scratch/s2995697/fseval/
#SBATCH --output=/data/s2995697/slurm/logs/slurm-%A_%a.out

echo "Running RQ worker job ✨"

echo "(1) Spawning a job to upload logs, as a dependency on this job."
sh ~/msc-thesis/jobs/_spawn_upload_logs_job.sh

echo "(2) Requesting to prepare the worker environment..."
sh ~/msc-thesis/jobs/_prepare_env.sh
module load Python/3.8.6-GCCcore-10.2.0
source $TMPDIR/venv_${SLURM_JOB_ID}_${SLURM_ARRAY_TASK_ID}/bin/activate

echo "(3) Running rq worker..."
rq worker -u $REDIS_URL