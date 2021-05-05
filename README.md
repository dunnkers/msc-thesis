# mleval
A Machine Learning benchmarking library. Neatly integrates with wandb and sklearn. Uses Hydra as a config parser.



## Enqueueing jobs
Install [fseval](https://github.com/dunnkers/fseval). Then run:

```
fseval --multirun \
    ranker=chi2,relieff,tabnet \
    dataset=boston,iris,switch,xor \
    resample.sample_size=0.75 \
    resample.random_state=10,11,12,13,14,15,16,17,18,19,20 \
    hydra/launcher=rq \
    hydra.launcher.enqueue.result_ttl=1d \
    hydra.launcher.enqueue.failure_ttl=1d \
    hydra.launcher.stop_after_enqueue=true
```

... which runs a benchmark on 3 rankers, 4 datasets and some 10 bootstrap datasets.