#!/bin/bash

if [ -n "${SLURM_ARRAY_JOB_ID+set}" ]; then
    export JOB_ID=$SLURM_ARRAY_JOB_ID
else
    export JOB_ID=$SLURM_JOB_ID
fi
