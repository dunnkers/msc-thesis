import wandb
import hydra
from omegaconf import DictConfig
from mleval.datasrc import DataSource
from mleval.rankers import Ranker
from dataclasses import dataclass

@dataclass
class Task:
    datasrc: DataSource

    def run(self) -> None: raise NotImplementedError

@dataclass
class FeatureRanker(Task):
    ranker: Ranker

    def __post_init__(self):
        self.ranker = hydra.utils.instantiate(self.ranker)
        
    def run(self) -> None:
        X, y = self.datasrc.load()
        ranking, _ = self.ranker.rank(X, y)
        return ranking
