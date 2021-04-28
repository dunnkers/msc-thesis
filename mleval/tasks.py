import wandb
import hydra
import numpy as np
import pandas as pd
from omegaconf import DictConfig
from mleval.datasrc import DataSource
from mleval.dataset import DataSet
from mleval.rankers import Ranker
from dataclasses import dataclass
from slugify import slugify
from sklearn.model_selection import BaseCrossValidator
from sklearn.pipeline import Pipeline
from sklearn.utils import resample

@dataclass
class Task:
    cfg: DictConfig
    datasrc: DataSource
    cv: BaseCrossValidator

    def run(self) -> None: raise NotImplementedError

@dataclass
class FeatureRanker(Task):
    ranker: Ranker
    bootseed: int = 0
    fold: int = 0

    def __post_init__(self):
        self.ranker = hydra.utils.instantiate(self.ranker)
        
    def run(self) -> None:
        cfg: DictConfig = self.cfg
        ds: DataSource  = self.datasrc
        ranker: Ranker  = self.ranker


        # load dataset
        X, y = ds.load()
        # use training split
        train_index, _ = list(self.cv.split(X))[self.fold]
        # boostrap: random sampling with replacement - test stability
        train_index = resample(train_index, random_state=self.bootseed)

        # perform feature ranking
        run = wandb.init(project=cfg.project, config=dict(
            dataset=ds.__dict__,
            ranker=ranker.__dict__
            # TODO: just pass in entire conf object?
            # TODO: rename `_target_` to `type`?
        ), job_type='FeatureRanker')
        ranking = ranker.rank(X[train_index], y[train_index])

        # save ranking to wandb
        series = pd.Series(ranking)
        save_path = f'{wandb.run.dir}/ranking.csv'
        series.to_csv(save_path, index=False)

        wandb.finish()