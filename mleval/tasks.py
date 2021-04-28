import wandb
import hydra
import numpy as np
import pandas as pd
from omegaconf import DictConfig, OmegaConf
from mleval.datasrc import DataSource
from mleval.dataset import DataSet
from mleval.rankers import AbstractRanker
from dataclasses import dataclass
from slugify import slugify
from sklearn.model_selection import BaseCrossValidator
from sklearn.pipeline import Pipeline
from sklearn.utils import resample

@dataclass
class Task:
    name: str
    cfg: DictConfig
    datasrc: DataSource
    cv: BaseCrossValidator

    def run(self) -> None: raise NotImplementedError

@dataclass
class FeatureRanker(Task):
    bootseed: int = 0
    fold: int = 0

    def __post_init__(self):
        # instantiate estimator
        est = self.cfg.ranker.estimator
        self.estimator: AbstractRanker = hydra.utils.instantiate(est)

        # move estimator to top-level
        OmegaConf.set_struct(self.cfg, False)
        self.cfg.estimator = est
        del self.cfg.ranker['estimator']
        OmegaConf.set_struct(self.cfg, True)
        
    def run(self) -> None:
        # load dataset
        X, y = self.datasrc.load()
        # get training split indices
        train_index, _ = list(self.cv.split(X))[self.fold]
        # boostrap: random sampling with replacement - test stability
        train_index = resample(train_index, random_state=self.bootseed)
        # train subset
        X_train, y_train = X[train_index], y[train_index]

        # configure wandb
        config = OmegaConf.to_container(self.cfg, resolve=True)
        run = wandb.init(   project=self.cfg.project,
                            config=config, 
                            job_type=self.cfg.task.name)
        # perform feature ranking
        self.estimator.fit_transform(X_train, y_train)
        ranking = self.estimator.feature_importances_

        # save ranking to wandb
        series = pd.Series(ranking)
        save_path = f'{wandb.run.dir}/ranking.csv'
        series.to_csv(save_path, index=False)

        wandb.finish()