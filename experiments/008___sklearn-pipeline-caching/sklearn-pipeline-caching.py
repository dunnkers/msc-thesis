#%%
import numpy as np
import sklearn
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier

steps = [
    ("scaler", StandardScaler()),
    ("kbest", SelectKBest(score_func=f_classif, k=1)),
    ("dt", DecisionTreeClassifier(random_state=0)),
]
np.random.seed(0)
pipeline = Pipeline(steps=steps, memory="../../sklearn_cache/", verbose=True)
pipeline.fit(np.random.normal(size=(500000, 100)), np.random.randint(2, size=500000))

# print(pipeline.feature_importances_)
print(pipeline.score(np.random.normal(size=(5, 100)), np.random.randint(2, size=5)))
pipeline.named_steps["dt"].feature_importances_
