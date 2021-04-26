import wandb
import hydra
import numpy as np
from omegaconf import DictConfig
from mleval.datasrc import DataSource
from mleval.rankers import Ranker
from dataclasses import dataclass
from slugify import slugify

@dataclass
class Task:
    cfg: DictConfig
    datasrc: DataSource

    def run(self) -> None: raise NotImplementedError

@dataclass
class FeatureRanker(Task):
    ranker: Ranker

    def __post_init__(self):
        self.ranker = hydra.utils.instantiate(self.ranker)
        
    def run(self) -> None:
        cfg     = self.cfg
        ds      = self.datasrc
        ranker  = self.ranker

        run = wandb.init(project=cfg.project, config=dict(
            dataset=ds.__dict__,
            ranker=ranker.__dict__
            # TODO: just pass in entire conf object?
            # TODO: rename `_target_` to `type`?
        ), job_type='FeatureRanker')

        # perform feature ranking
        X, y = ds.load()
        ranking, _ = ranker.rank(X, y)

        # save ranking to wandb
        series = pd.Series(ranking)
        save_path = f'{wandb.run.dir}/ranking.csv'
        series.to_csv(save_path, index=False)

        wandb.finish()