# mleval
A Machine Learning benchmarking library. Neatly integrates with wandb and sklearn. Uses Hydra as a config parser.



## Enqueueing jobs
Install [fseval](https://github.com/dunnkers/fseval). Then run:

```shell
fseval --multirun \
    ranker="glob(*)" \
    dataset="glob(*)" \
    resample.sample_size=0.75 \
    resample.random_state="range(20, 30)" \
    hydra/launcher=rq \
    hydra.launcher.enqueue.result_ttl=1d \
    hydra.launcher.enqueue.failure_ttl=1d \
    hydra.launcher.stop_after_enqueue=true
```

... which runs a benchmark on 3 rankers, 4 datasets and some 10 bootstrap datasets.


## Running workers on Peregrine
From your laptop, run:

```shell
ssh $PEREGRINE_USERNAME@peregrine.hpc.rug.nl "sbatch msc-thesis/rq-worker.sh --array=0-5 --job-name=rq-workers"
```

Check your queue status:
```shell
ssh $PEREGRINE_USERNAME@peregrine.hpc.rug.nl "squeue -u $PEREGRINE_USERNAME"
```

## Running the RQ dashboard
```shell
rq-dashboard -u $REDIS_URL
```