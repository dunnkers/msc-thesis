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
fseval --multirun \
    "pipeline.n_bootstraps=25" \
    "dataset=glob(*)" \
    "estimator@pipeline.ranker=glob(*)" \
    "++callbacks.wandb.project=fseval" \
    "++callbacks.wandb.group=cohort-1" \
    "hydra/launcher=rq" \
    "hydra.launcher.enqueue.result_ttl=1d" \
    "hydra.launcher.enqueue.failure_ttl=1d" \
    "hydra.launcher.stop_after_enqueue=true"
```

... which runs a benchmark on all rankers and all datasets.


Learning curve run:

```shell
fseval --multirun \
    "pipeline.n_bootstraps=25" \
    "dataset=synreg_hard" \
    "pipeline.resample.sample_size=range(0.01, 0.1, 0.01)" \
    "estimator@pipeline.ranker=glob(*)" \
    "++callbacks.wandb.project=fseval" \
    "++callbacks.wandb.group=cohort-1" \
    "hydra/launcher=rq" \
    "hydra.launcher.enqueue.result_ttl=1d" \
    "hydra.launcher.enqueue.failure_ttl=1d" \
    "hydra.launcher.stop_after_enqueue=true"
```

## Running workers on Peregrine
> Make sure to set the `PEREGRINE_USERNAME` environment variable both locally and on the cluster.

From your laptop, run:

```shell
ssh $PEREGRINE_USERNAME@peregrine.hpc.rug.nl "cd msc-thesis; sbatch --array=0-1 --job-name=rq-workers jobs/rq-worker.sh"
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

## Running the RQ dashboard
```shell
rq-dashboard -u $REDIS_URL
```