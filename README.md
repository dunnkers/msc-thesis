# msc-thesis
Benchmarking feature rankers using [fseval](https://github.com/dunnkers/fseval).

## Enqueueing jobs
Install [fseval](https://github.com/dunnkers/fseval). Then run:

```shell
pg -t "srun --ntasks=1 --time=00:30:00 --mem=5000 --chdir=/scratch/s2995697/fseval/ --partition=short --pty bash -i"

sh ~/msc-thesis/jobs/_prepare_env.sh

module load Python/3.8.6-GCCcore-10.2.0
source $venv_dir/bin/activate
fseval \
    "--multirun" \
    "pipeline.n_bootstraps=25" \
    "dataset=glob(*)" \
    "estimator@pipeline.ranker=stability_selection" \
    "++callbacks.wandb.project=fseval" \
    "++callbacks.wandb.group=cohort-1" \
    "hydra/launcher=rq" \
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
pg "sbatch --array=0-3 --time=20:00:00 --job-name=rq-worker ~/msc-thesis/jobs/rq_worker.sh"
```


## Running the RQ dashboard
```shell
rq-dashboard -u $REDIS_URL
```