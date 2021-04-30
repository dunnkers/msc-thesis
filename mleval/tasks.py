import wandb
import hydra
import numpy as np
import pandas as pd
from omegaconf import DictConfig, OmegaConf
from mleval.datasrc import DataSource
from mleval.rankers import AbstractRanker
from dataclasses import dataclass, asdict
from slugify import slugify
from sklearn.model_selection import BaseCrossValidator
from sklearn.pipeline import Pipeline
from sklearn.utils import resample
from typing import Tuple, List

@dataclass
class Task:
    name: str
    cfg: DictConfig
    datasrc: DataSource
    cv: BaseCrossValidator
    fold: int = 0

    def get_splits(self, X) -> Tuple[List, List]:
        splits = list(self.cv.split(X))
        train_index, test_index = splits[self.fold]
        return train_index, test_index

    def run(self) -> None:
        # load dataset
        X, y = self.datasrc.get_data()

        # configure wandb
        config = OmegaConf.to_container(self.cfg, resolve=True)
        run = wandb.init(   project=self.cfg.project,
                            config=config, 
                            job_type=self.cfg.task.name,
                            # id=wandb.util.generate_id()
                            )

        # run estimator
        print(f'{self.cfg.task.name}' +
              f' (fold {self.fold + 1}/{self.cv.get_n_splits(X)})')
        print(f'Using {self.datasrc.name} dataset' +
              f' (n={self.datasrc.n}, p={self.datasrc.p}).')
        return self.run_estimator(X, y)

@dataclass
class FeatureRanker(Task):
    def __post_init__(self):
        # instantiate estimator
        est = self.cfg.ranker.estimator
        self.estimator: AbstractRanker = hydra.utils.instantiate(est)

        # # move estimator to top-level
        # OmegaConf.set_struct(self.cfg, False)
        # self.cfg.estimator = est
        # # TODO add get_params()
        # del self.cfg.ranker['estimator']
        # OmegaConf.set_struct(self.cfg, True)
        
    def run_estimator(self, X, y) -> None:
        train_index, _ = self.get_splits(X)
        # boostrap: random sampling with replacement - test stability
        train_index = resample(train_index, **self.cfg.bootstrap)
        X_train, y_train = X[train_index], y[train_index]

        # perform feature ranking
        n, p = X_train.shape
        print(f'Feature ranking with (n={n}, p={p}). Params:')
        self.estimator.fit_transform(X_train, y_train)
        ranking = self.estimator.feature_importances_

        # save ranking to wandb
        series = pd.Series(ranking)
        save_path = f'{wandb.run.dir}/ranking.csv'
        series.to_csv(save_path, index=False)

        run_path = wandb.run.path
        wandb.finish()
        return run_path

@dataclass
class ValidateRanking(Task):
    run_path: str = None
    k: int = 1

    def __post_init__(self):
        est = self.cfg.validator.estimator
        self.estimator: AbstractRanker = hydra.utils.instantiate(est)

    def run_estimator(self, X, y) -> None:
        file = wandb.restore('ranking.csv', run_path=self.run_path)
        ranking = pd.read_csv(file.name, squeeze=True)
        ranking = ranking.to_numpy()
        kbest = np.argsort(ranking)[-self.k:]

        train_index, test_index = self.get_splits(X)
        X_train, y_train = X[train_index], y[train_index]
        X_test, y_test = X[test_index], y[test_index]
        
        # select features
        X_train = X_train[:, kbest]
        X_test = X_test[:, kbest]

        # fit and score estimator
        self.estimator.fit(X_train, y_train)
        score = self.estimator.score(X_test, y_test)

        wandb.log({
            'score': score
        })
        
        run_path = wandb.run.path
        wandb.finish()
        return run_path

# TODO use a sklearn.pipeline.Pipeline?
@dataclass
class RankAndValidate(Task):
    def run(self) -> None:
        ranker = FeatureRanker(
            name='Rank features',
            fold=self.cfg.task.fold,
            cfg=self.cfg,
            datasrc=self.datasrc,
            cv=self.cv
        )
        run_path = ranker.run()

        validator = ValidateRanking(
            name='Validate feature ranking',
            fold=self.cfg.task.fold,
            cfg=self.cfg,
            datasrc=self.datasrc,
            cv=self.cv,
            run_path=run_path
        )
        validator.run()