# mleval
A Machine Learning benchmarking library. Neatly integrates with wandb and sklearn. Uses Hydra as a config parser.



## Enqueueing jobs
Install [fseval](https://github.com/dunnkers/fseval). Then run:
    <!-- # hydra.run.dir="/Users/dunnkers/Downloads/outputs/${now:%Y-%m-%d}/${now:%H-%M-%S}" \
    # hydra.sweep.dir="/Users/dunnkers/Downloads/multirun/${now:%Y-%m-%d}/${now:%H-%M-%S}" \ -->
    <!-- hydra.run.dir='/data/${oc.env:PEREGRINE_USERNAME}/fseval/outputs/${now:%Y-%m-%d}/${now:%H-%M-%S}' \
    hydra.sweep.dir='/data/${oc.env:PEREGRINE_USERNAME}/fseval/multirun/${now:%Y-%m-%d}/${now:%H-%M-%S}' \ 
    hydra.sweep.subdir='${hydra.job.num}' \-->

```shell
fseval \
    "--multirun" \
    "pipeline.n_bootstraps=25" \
    "dataset=synclf_easy,synclf_medium,synclf_hard,synclf_very_hard" \
    "estimator@pipeline.ranker=glob(*)" \
    "++callbacks.wandb.project=fseval" \
    "++callbacks.wandb.group=cohort-1" \
    "hydra/launcher=rq" \
    "hydra.launcher.enqueue.result_ttl=1d" \
    "hydra.launcher.stop_after_enqueue=true"
```

... which runs a benchmark on all rankers and all datasets.


Learning curve run:

```shell
fseval \
    "--multirun" \
    "pipeline.n_bootstraps=25" \
    "dataset=synclf_hard" \
    "pipeline.resample.sample_size=range(0.01, 0.1, 0.01)" \
    "estimator@pipeline.ranker=glob(*)" \
    "++callbacks.wandb.project=fseval" \
    "++callbacks.wandb.group=cohort-1" \
    "hydra/launcher=rq" \
    "hydra.launcher.enqueue.result_ttl=1d" \
    "hydra.launcher.stop_after_enqueue=true"
```

⚠️ Mind carefully: when using the RQ launcher jobs **must** be launched in exactly the same environment as in which the jobs will eventually run: this has to do with how `cloudpickle` works: the serializer and deserializer of the jobs to- and from Redis.

## Running workers on Peregrine
> Make sure to set the `PEREGRINE_USERNAME` environment variable both locally and on the cluster.

From your laptop, run:

```shell
ssh $PEREGRINE_USERNAME@peregrine.hpc.rug.nl "cd msc-thesis; git pull"
ssh $PEREGRINE_USERNAME@peregrine.hpc.rug.nl "cd msc-thesis; git log -n 1"
ssh $PEREGRINE_USERNAME@peregrine.hpc.rug.nl "cd msc-thesis; sbatch --array=0-1 --job-name=rq-workers jobs/rq-worker.sh"
```

A small test worker run can be started like so:
```shell
ssh $PEREGRINE_USERNAME@peregrine.hpc.rug.nl "cd msc-thesis; sbatch --array=0-1 --job-name=rq-workers --time=00:30:00 --partition=short jobs/rq-worker.sh"
```

Check your queue status:
```shell
ssh $PEREGRINE_USERNAME@peregrine.hpc.rug.nl "squeue -u $PEREGRINE_USERNAME"
```

To download raw log files:
```shell
rsync -aP $PEREGRINE_USERNAME@peregrine.hpc.rug.nl:/data/$PEREGRINE_USERNAME/slurm/ ./slurm/
```

Upload SLURM information to wandb using:

```shell
sh src/sacct_to_csv.sh $SACCT_JOB_ID | python src/sacct_csv_to_wandb.py
```

per job, on the cluster. Or for all jobs, on Peregrine:

```shell
ssh $PEREGRINE_USERNAME@peregrine.hpc.rug.nl "cd msc-thesis; sh src/sacct_to_csv.sh" | python src/sacct_csv_to_wandb.py
```

## Architecture
Uses [RQ](https://python-rq.org/) (Redis Queue) as a launcher for Hydra. For this reason we require a Redis server. Follow Hydra RQ [instructions](https://hydra.cc/docs/next/plugins/rq_launcher/): set all necessary environment variables. Also:

- Take note of whether your Redis server uses SSL or not `redis` versus `rediss`. In the case of SSL, we require extra config. A version of the RQ launcher supporting SSL is available on the [dunnkers/hydra](https://github.com/dunnkers/hydra) fork. to install:

```shell
pip install -e \
        git+https://github.com/dunnkers/hydra.git@master#egg=hydra-rq-launcher\&subdirectory=plugins/hydra_rq_launcher
```

Which install the RQ launcher compatible with Hydra 1.1. For 1.0 compatibility, use the `1.0_branch` branch. 

### Running Hydra & RQ:

When getting the following error:
> We cannot safely call it or ignore it in the fork() child process. Crashing instead.
Use ([src](https://stackoverflow.com/questions/50168647/multiprocessing-causes-python-to-crash-and-gives-an-error-may-have-been-in-progr)):

```shell
OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES
```

→ Be more verbose by setting `hydra.verbose=true` or `hydra.verbose=__main__`


## Running the RQ dashboard
```shell
rq-dashboard -u $REDIS_URL
```