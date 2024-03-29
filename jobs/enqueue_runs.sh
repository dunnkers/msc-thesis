#!/bin/bash
#SBATCH --time=02:00:00
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --partition=regular
#SBATCH --job-name=enqueue-fseval-jobs
#SBATCH --mem=10000
#SBATCH --chdir=/scratch/s2995697/fseval/
#SBATCH --output=/data/s2995697/slurm/logs/slurm-%A.out

echo "Running metrics enqueueing job ✨"

echo "(1) 📚 Spawning a job to upload logs ..."
sh ~/msc-thesis/jobs/_spawn_upload_logs_job.sh

echo "(2) 🔧 Requesting to prepare fseval environment ..."
sh ~/msc-thesis/jobs/_prepare_env.sh
module load Python/3.8.6-GCCcore-10.2.0
source $TMPDIR/venv_${SLURM_JOB_ID}_${SLURM_ARRAY_TASK_ID}/bin/activate

echo "(3) 📊 Fetching runs and storing enqueueing script ..."
echo "→ storing jobs in '$TMPDIR/fseval_jobs.sh'."
rm -rf $TMPDIR/fseval_jobs.sh
python ~/msc-thesis/src/enqueue_runs.py $TMPDIR/fseval_jobs.sh

echo "(4) 🚀 Enqueueing jobs ..."
sh $TMPDIR/fseval_jobs.sh

exit 0