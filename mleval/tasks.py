import wandb
import hydra
from omegaconf import DictConfig
from mleval.datasources import DataSource
from mleval.rankers import Ranker
from dataclasses import dataclass

@dataclass
class Task:
    def run(self) -> None: raise NotImplementedError

@dataclass
class FeatureRanker(Task):
    ranker: Ranker
    dataset: DataSource

    def __post_init__(self):
        self.ranker = hydra.utils.instantiate(self.ranker)
        self.dataset = hydra.utils.instantiate(self.dataset)
        
    def run(self) -> None:
        X, y = self.dataset.load()
        ranking, _ = self.ranker.rank(X, y)
        print('ranking', ranking)