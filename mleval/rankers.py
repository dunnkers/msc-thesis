from dataclasses import dataclass
from typing import List
from sklearn.base import BaseEstimator
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2

@dataclass
class AbstractRanker(BaseEstimator):
    n_features_to_select: int = None
    feature_importances_: List[float] = None

@dataclass
class Chi2(SelectKBest):
    n_features_to_select: int = None

    def __init__(self, n_features_to_select=None):
        super().__init__(score_func=chi2, k=n_features_to_select)
        self.n_features_to_select = n_features_to_select

    @property
    def feature_importances_(self):
        return self.scores_
