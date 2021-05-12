### Concurrent
In 3 terminal windows, run:

```shell
python wandb-run-id-multiprocessing.py 0
```

```shell
python wandb-run-id-multiprocessing.py 1
```

```shell
python wandb-run-id-multiprocessing.py 2
```

**simultaneously**.

=> does not work.
### Serial

```shell
python wandb-run-id-multiprocessing.py 0
python wandb-run-id-multiprocessing.py 1
python wandb-run-id-multiprocessing.py 2
```

with `wandb.init(resume="allow")` **does** work.