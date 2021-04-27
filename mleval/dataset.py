from mleval.datasrc import DataSource
from dataclasses import dataclass
from typing import Tuple

@dataclass
class DataSet:
    datasrc: DataSource
    testseed: int = 0
    bootseed: int = 0

    def load(self, subset=None) -> Tuple[list, list]:
        X, y = datasrc.load()
        pass