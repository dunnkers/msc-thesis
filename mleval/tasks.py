import wandb
import hydra
import numpy as np
import pandas as pd
import pprint
from omegaconf import DictConfig, OmegaConf
from mleval.datasrc import DataSource
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
    fold: int = 0

    def run(self) -> None:
        # load dataset
        X, y = self.datasrc.get_data()
        # get training split indices
        splits = list(self.cv.split(X))
        train_index, _ = splits[self.fold]
        # boostrap: random sampling with replacement - test stability
        train_index = resample(train_index, **self.cfg.bootstrap)
        # train subset
        X_train, y_train = X[train_index], y[train_index]

        # configure wandb
        config = OmegaConf.to_container(self.cfg, resolve=True)
        run = wandb.init(   project=self.cfg.project,
                            config=config, 
                            job_type=self.cfg.task.name)

        # run estimator
        print(f'Running {self.cfg.task.name}' +
              f' on fold {self.fold + 1}/{len(splits)}')
        print(f'Using {self.datasrc.name} dataset' +
              f'(n={self.datasrc.n}, p={self.datasrc.p}).')
        self.run_estimator(X_train, y_train)

@dataclass
class FeatureRanker(Task):
    def __post_init__(self):
        # instantiate estimator
        est = self.cfg.ranker.estimator
        self.estimator: AbstractRanker = hydra.utils.instantiate(est)

        # move estimator to top-level
        OmegaConf.set_struct(self.cfg, False)
        self.cfg.estimator = est
        # TODO add get_params()
        del self.cfg.ranker['estimator']
        OmegaConf.set_struct(self.cfg, True)
        
    def run_estimator(self, X, y) -> None:
        # perform feature ranking
        n, p = X.shape
        print(f'Feature ranking with (n={n}, p={p}). Params:')
        pprint.pprint(self.estimator.get_params())
        self.estimator.fit_transform(X, y)
        ranking = self.estimator.feature_importances_

        # save ranking to wandb
        series = pd.Series(ranking)
        save_path = f'{wandb.run.dir}/ranking.csv'
        series.to_csv(save_path, index=False)

        wandb.finish()

@dataclass
class FitEstimator(Task):
    run_path: str = None

    def run_estimator(self, X, y) -> None:
        inp = wandb.restore('ranking.csv', run_path=self.run_path)