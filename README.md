# mleval
A Machine Learning benchmarking library. Neatly integrates with wandb and sklearn. Uses Hydra as a config parser.



## Enqueueing jobs
Install [fseval](https://github.com/dunnkers/fseval). Then run:

```shell
fseval --multirun \
    dataset="glob(*)" \
    estimator@pipeline.ranker="glob(*)" \
    hydra/launcher=rq \
    hydra.launcher.enqueue.result_ttl=1d \
    hydra.launcher.enqueue.failure_ttl=1d \
    hydra.launcher.stop_after_enqueue=true \
    pipeline.n_bootstraps=30 \
    # +callbacks.wandb.project="fseval" \
```

... which runs a benchmark on all rankers and all datasets.


## Running workers on Peregrine
From your laptop, run:

```shell
ssh $PEREGRINE_USERNAME@peregrine.hpc.rug.nl "sbatch --array=0-1 --job-name=rq-workers msc-thesis/rq-worker.sh"
```

Check your queue status:
```shell
ssh $PEREGRINE_USERNAME@peregrine.hpc.rug.nl "squeue -u $PEREGRINE_USERNAME"
```

Download logs:
```shell
ssh $PEREGRINE_USERNAME@peregrine.hpc.rug.nl "sh ~/msc-thesis/save_sacct_to_logs.sh"
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