import os

import wandb
from rq import Worker
from slurm_to_wandb import sacct_as_df


class WandbWorker(Worker):
    def register_birth(self):
        df = sacct_as_df(os.environ.get("SLURM_JOB_ID"))
        result = df.loc[0]
        wandb.init(
            project="peregrine",
            config=result.to_dict(),
            id=result["JobID"] if "JobID" in df else None,
            job_type=result["JobName"] if "JobName" in df else None,
            name=result["JobID"] if "JobID" in df else None,
            tags=[result["State"]] if "State" in df else None,
        )
        wandb.init(project="peregrine", config=df)
        super(WandbWorker, self).register_birth()

    def register_death(self):
        df = sacct_as_df(os.environ.get("SLURM_JOB_ID"))
        result = df.loc[0]
        wandb.finish(exit_code=result["ExitCode"] if "ExitCode" in result else None)
        super(WandbWorker, self).register_death()
