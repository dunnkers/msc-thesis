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
ssh $PEREGRINE_USERNAME@peregrine.hpc.rug.nl "sacct --format='Account,AdminComment,AllocCPUS,AllocGRES,AllocNodes,AllocTRES,AssocID,AveCPU,AveCPUFreq,AveDiskRead,AveDiskWrite,AvePages,AveRSS,AveVMSize,BlockID,Cluster,Comment,Constraints,ConsumedEnergy,ConsumedEnergyRaw,CPUTime,CPUTimeRAW,DBIndex,DerivedExitCode,Elapsed,ElapsedRaw,Eligible,End,ExitCode,Flags,GID,Group,JobID,JobIDRaw,JobName,Layout,MaxDiskRead,MaxDiskReadNode,MaxDiskReadTask,MaxDiskWrite,MaxDiskWriteNode,MaxDiskWriteTask,MaxPages,MaxPagesNode,MaxPagesTask,MaxRSS,MaxRSSNode,MaxRSSTask,MaxVMSize,MaxVMSizeNode,MaxVMSizeTask,McsLabel,MinCPU,MinCPUNode,MinCPUTask,NCPUS,NNodes,NodeList,NTasks,Priority,Partition,QOS,QOSRAW,Reason,ReqCPUFreq,ReqCPUFreqMin,ReqCPUFreqMax,ReqCPUFreqGov,ReqCPUS,ReqGRES,ReqMem,ReqNodes,ReqTRES,Reservation,ReservationId,Reserved,ResvCPU,ResvCPURAW,Start,State,Submit,Suspended,SystemCPU,SystemComment,Timelimit,TimelimitRaw,TotalCPU,TRESUsageInAve,TRESUsageInMax,TRESUsageInMaxNode,TRESUsageInMaxTask,TRESUsageInMin,TRESUsageInMinNode,TRESUsageInMinTask,TRESUsageInTot,TRESUsageOutAve,TRESUsageOutMax,TRESUsageOutMaxNode,TRESUsageOutMaxTask,TRESUsageOutMin,TRESUsageOutMinNode,TRESUsageOutMinTask,TRESUsageOutTot,UID,User,UserCPU,WCKey,WCKeyID,WorkDir' --starttime 2021-05-20 -u $PEREGRINE_USERNAME --parsable2 -v --delimiter=';' > /data/$PEREGRINE_USERNAME/logs/sacct.csv"
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