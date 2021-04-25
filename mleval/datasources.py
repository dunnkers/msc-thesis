from dataclasses import dataclass
from openml.datasets import get_dataset
import pandas as pd
import numpy as np
from typing import Tuple

@dataclass
class DataSource:
    type: str # classification / regression

    def load(self) -> Tuple[list, list]: raise NotImplementedError

@dataclass
class OpenML(DataSource):
    id: int
    target_column: str

    def load(self) -> Tuple[list, list]:
        dataset = get_dataset(self.id)
        X, y, cat, _ = dataset.get_data(target=self.target_column)

        # drop qualitative columns
        to_drop = X.columns[np.array(cat)]
        X = X.drop(columns=to_drop).values

        # quantitatively encode target
        y, _ = pd.factorize(y)
        
        return X, y