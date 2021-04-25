from dataclasses import dataclass
from typing import List

@dataclass
class Ranker:
    ranking_type: str

    def rank(self, X, y) -> List[float]: raise NotImplementedError

from sklearn.feature_selection import chi2
class Chi2(Ranker):
    def rank(self, X, y) -> List[float]:
        scores = chi2(X, y)
        return scores / sum(scores)