from dataclasses import dataclass
from typing import List
from sklearn.base import BaseEstimator
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2

@dataclass
class AbstractRanker(BaseEstimator):
    n_features_to_select: int = 1
    feature_importances_: List[float] = None

@dataclass
class Chi2(SelectKBest):
    def __init__(self, n_features_to_select=1):
        super().__init__(score_func=chi2, k=n_features_to_select)
        self.n_features_to_select = n_features_to_select

    @property
    def feature_importances_(self):
        return self.scores_
