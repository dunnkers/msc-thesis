# mleval
A Machine Learning benchmarking library. Neatly integrates with wandb and sklearn. Uses Hydra as a config parser.



## Enqueueing jobs
Install [fseval](https://github.com/dunnkers/fseval). Then run:
    <!-- # hydra.run.dir="/Users/dunnkers/Downloads/outputs/${now:%Y-%m-%d}/${now:%H-%M-%S}" \
    # hydra.sweep.dir="/Users/dunnkers/Downloads/multirun/${now:%Y-%m-%d}/${now:%H-%M-%S}" \ -->

```shell
fseval --multirun \
    hydra.run.dir="/data/$PEREGRINE_USERNAME/fseval/outputs/${now:%Y-%m-%d}/${now:%H-%M-%S}" \
    hydra.sweep.dir="/data/$PEREGRINE_USERNAME/fseval/multirun/${now:%Y-%m-%d}/${now:%H-%M-%S}" \
    hydra.sweep.subdir="${hydra.job.num}" \
    dataset="glob(*)" \
    estimator@pipeline.ranker="glob(*)" \
    pipeline.n_bootstraps=30 \
    hydra/launcher=rq \
    hydra.launcher.enqueue.result_ttl=1d \
    hydra.launcher.enqueue.failure_ttl=1d \
    hydra.launcher.stop_after_enqueue=true \
    # +callbacks.wandb.project="fseval" \
```

... which runs a benchmark on all rankers and all datasets.


## Running workers on Peregrine
> Make sure to set the `PEREGRINE_USERNAME` environment variable both locally and on the cluster.

From your laptop, run:

```shell
ssh $PEREGRINE_USERNAME@peregrine.hpc.rug.nl "cd msc-thesis; sbatch --array=0-1 --job-name=rq-workers src/rq-worker.sh"
```

Check your queue status:
```shell
ssh $PEREGRINE_USERNAME@peregrine.hpc.rug.nl "squeue -u $PEREGRINE_USERNAME"
```

Save `sacct` SLURM job information to `/data/<user>/logs/`.
```shell
ssh $PEREGRINE_USERNAME@peregrine.hpc.rug.nl "sh ~/msc-thesis/sacct_to_csv.sh > /data/$PEREGRINE_USERNAME/logs/sacct.csv"
```

To download raw log files:
```shell
rsync -aP $PEREGRINE_USERNAME@peregrine.hpc.rug.nl:/data/$PEREGRINE_USERNAME/logs/ ./logs/
```

Then upload to wandb using:

```shell
python wandb_sacct_uploader.py
```

## Running the RQ dashboard
```shell
rq-dashboard -u $REDIS_URL
```