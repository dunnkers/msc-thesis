# msc-thesis
Benchmarking feature rankers using [fseval](https://github.com/dunnkers/fseval).



## Enqueueing jobs
Run:

```shell
pg -t 'sh /home/$PEREGRINE_USERNAME/msc-thesis/jobs/prepare_fseval_env.sh; bash -l'
```

(see Peregrine [wiki page](https://github.com/dunnkers/msc-thesis/wiki/Peregrine#cli-aliases-and-shortcuts) for command-line aliases)

## Enqueueing jobs
Install [fseval](https://github.com/dunnkers/fseval). Then run:

```shell
ssh $PEREGRINE_USERNAME@peregrine.hpc.rug.nl -t "srun --ntasks=1 --time=00:30:00 --partition=short --pty bash -i"
```

```shell
fseval \
    --multirun \
    --config-dir conf \
    +experiment=rq \
    pipeline.n_bootstraps=25 \
    dataset="glob(*)" \
    "estimator@pipeline.ranker=featboost" \
    "++callbacks.wandb.group=cohort-1" \
    "++callbacks.wandb.group=fseval"
```

```shell
fseval \
    "--multirun" \
    "pipeline.n_bootstraps=25" \
    "dataset=glob(*)" \
    "estimator@pipeline.ranker=featboost" \
    "++callbacks.wandb.project=fseval" \
    "++callbacks.wandb.group=cohort-1" \
    "hydra/launcher=rq" \
    "hydra.launcher.enqueue.result_ttl=1d" \
    "hydra.launcher.enqueue.failure_ttl=60d" \
    "hydra.launcher.stop_after_enqueue=true"
```


... which runs a benchmark on all rankers and all datasets.


Learning curve run:

```shell
fseval \
    --multirun \
    --config-dir conf \
    +experiment=rq \
    "pipeline.n_bootstraps=25" \
    "dataset=glob(*)" \
    "pipeline.resample.sample_size=range(0.01, 0.1, 0.01)" \
    "estimator@pipeline.ranker=boruta" \
    "++callbacks.wandb.project=fseval" \
    "++callbacks.wandb.group=cohort-1" \
```

⚠️ Mind carefully: when using the RQ launcher jobs **must** be launched in exactly the same environment as in which the jobs will eventually run: this has to do with how `cloudpickle` works: the serializer and deserializer of the jobs to- and from Redis.

## Running workers on Peregrine
> Make sure to set the `PEREGRINE_USERNAME` environment variable both locally and on the cluster.

From your laptop, run:

```shell
ssh $PEREGRINE_USERNAME@peregrine.hpc.rug.nl "cd msc-thesis; git pull"
ssh $PEREGRINE_USERNAME@peregrine.hpc.rug.nl "cd msc-thesis; git log -n 1"
ssh $PEREGRINE_USERNAME@peregrine.hpc.rug.nl "cd msc-thesis; sbatch --array=0-3 --job-name=rq-worker jobs/rq_worker.sh"
```

(peregrine folders can be mounted like so:)

```shell
sudo sshfs -o allow_other,default_permissions,IdentityFile=~/.ssh/id_rsa $PEREGRINE_USERNAME@peregrine.hpc.rug.nl:/home/$PEREGRINE_USERNAME /Users/dunnkers/mnt/peregrine/home
sudo sshfs -o allow_other,default_permissions,IdentityFile=~/.ssh/id_rsa $PEREGRINE_USERNAME@peregrine.hpc.rug.nl:/data/$PEREGRINE_USERNAME /Users/dunnkers/mnt/peregrine/data
sudo sshfs -o allow_other,default_permissions,IdentityFile=~/.ssh/id_rsa $PEREGRINE_USERNAME@peregrine.hpc.rug.nl:/scratch/$PEREGRINE_USERNAME /Users/dunnkers/mnt/peregrine/scratch
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