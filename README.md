# msc-thesis
Benchmarking feature rankers using [fseval](https://github.com/dunnkers/fseval).

## Enqueueing jobs
Install [fseval](https://github.com/dunnkers/fseval). Then run:

```shell
pg -t "srun --ntasks=1 --time=02:00:00 --mem=10000 --chdir=/scratch/s2995697/fseval/ --partition=regular --pty bash -i"

sh ~/msc-thesis/jobs/_prepare_env.sh
module load Python/3.8.6-GCCcore-10.2.0
source $TMPDIR/venv_${SLURM_JOB_ID}_${SLURM_ARRAY_TASK_ID}/bin/activate

fseval \
    "--multirun" \
    "+dataset=synclf_easy" \
    "+estimator@ranker=multisurf" \
    "+estimator@validator=decision_tree" \
    "resample=bootstrap" \
    "resample.sample_size=1.0" \
    "n_bootstraps=25" \
    "n_jobs=13" \
    "storage=local" \
    "callbacks=[wandb]" \
    "++callbacks.wandb.project=fseval" \
    "++callbacks.wandb.log_metrics=true" \
    "++callbacks.wandb.resume=allow" \
    "++callbacks.wandb.group=fixing-runs" \
    "hydra/launcher=rq" \
    "hydra.launcher.queue=fixing-runs" \
    "hydra.launcher.enqueue.result_ttl=1d" \
    "hydra.launcher.enqueue.failure_ttl=60d" \
    "hydra.launcher.stop_after_enqueue=true" \
    "hydra.launcher.fail_hard=true"
```

(see Peregrine [wiki page](https://github.com/dunnkers/msc-thesis/wiki/Peregrine#cli-aliases-and-shortcuts) for command-line aliases like `pg`)

⚠️ Mind carefully: when using the RQ launcher jobs **must** be launched in exactly the same environment as in which the jobs will eventually run: this has to do with how `cloudpickle` works: the serializer and deserializer of the jobs to- and from Redis.

## Running workers on Peregrine
> Make sure to set the `PEREGRINE_USERNAME` environment variable both locally and on the cluster.

From your laptop, run:

```shell
pg "cd msc-thesis; git pull && git log -n 1"
pg "sbatch --array=0-2 --ntasks=13 --dependency=afterany:20579282 --partition=himem --mem=260000 --time=72:00:00 --export=queue=tabnet-run,burst=--burst ~/msc-thesis/jobs/rq_worker.sh"
```

## Enqueue runs
```shell
pg "cd msc-thesis; git pull && git log -n 1"
pg "sbatch ~/msc-thesis/jobs/enqueue_runs.sh"
pg "sbatch --array=0-1 --mem=455000 --ntasks=13 --partition=himem --time=96:00:00 --export=queue=himem-missing-runs,burst=--burst --job-name=himem-missing-runs ~/msc-thesis/jobs/rq_worker.sh"
```


## Running the RQ dashboard
```shell
rq-dashboard -u $REDIS_URL
```