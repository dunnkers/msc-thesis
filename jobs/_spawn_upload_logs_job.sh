#!/bin/bash

if [ -n "${SLURM_ARRAY_TASK_ID+set}" ]; then
    export JOB_ID=$SLURM_JOB_ID_$SLURM_ARRAY_TASK_ID
else
    export JOB_ID=$SLURM_JOB_ID
fi

echo "Spawning `upload logs` task for job $JOB_ID..."
sbatch \
    --dependency=afterany:$JOB_ID \
    --export=SACCT_JOB_ID=$JOB_ID \
    ~/msc-thesis/jobs/upload_logs.sh
