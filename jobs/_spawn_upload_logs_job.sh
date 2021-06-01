#!/bin/bash

if [ -n "${SLURM_ARRAY_TASK_ID+set}" ]; then
    JOB_ID=${SLURM_JOB_ID}_${SLURM_ARRAY_TASK_ID}
    echo -e "→ current job is \e[33mpart of a job array\e[0m."
else
    JOB_ID=${SLURM_JOB_ID}
    echo -e "→ current job is \e[33mstandalone\e[0m."
fi

echo "Scheduling 'logs upload' job as a dependency on job: $JOB_ID"
sbatch \
    --dependency=afterany:$JOB_ID \
    --export=SACCT_JOB_ID=$JOB_ID \
    ~/msc-thesis/jobs/upload_logs.sh
