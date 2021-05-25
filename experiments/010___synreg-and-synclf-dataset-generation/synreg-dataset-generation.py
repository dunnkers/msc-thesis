#%%
import os

import numpy as np
import pandas as pd
import seaborn as sns
import yaml
from matplotlib import pyplot as plt
from sklearn.datasets import make_regression
from sklearn.feature_selection import SelectKBest
from sklearn.model_selection import cross_val_score
from sklearn.tree import DecisionTreeRegressor


def synreg_dataset_generator(config, name, filename):
    """Synreg dataset generator. Given a `make_regression` config, this generates
    apprioprate yaml files, compatible with fseval."""

    X, y, coef = make_regression(**config)

    feature_importances = np.array(coef) / sum(coef)

    reg = DecisionTreeRegressor()
    n_folds = 5
    df = pd.DataFrame()
    n, p = np.array(X).shape

    for k in range(1, p + 1):
        for n_runs in range(10):
            X_new = SelectKBest(lambda X, y: coef, k=k).fit_transform(X, y)
            score = cross_val_score(reg, X_new, y, cv=n_folds)
            res = pd.DataFrame({"score": score, "fold": range(n_folds), "k": k})
            df = df.append(res)

    sns.scatterplot(data=df, x="k", y="score")
    plt.title(
        "feature importances:\n"
        + ", ".join(
            [
                f"{feature_importance:.2f}"
                for feature_importance in sorted(feature_importances, reverse=True)
            ]
        )
    )
    plt.tight_layout()
    plt.show()

    best_index = df["score"].argmax()
    print(f"n={n} best score:")
    print(df.iloc[best_index])

    feature_importances_string = ", ".join(feature_importances.astype(str))
    config["coef"] = False
    output = dict(
        name=name,
        task="regression",
        group="Synreg",
        domain="synthetic",
        adapter={
            "_target_": "sklearn.datasets.make_regression",
            **config,
        },
        feature_importances=f"[{feature_importances_string}]",
    )

    filedir = "/Users/dunnkers/git/fseval_2.0/fseval/conf/dataset"
    filepath = os.path.join(filedir, filename)
    with open(filepath, "w") as file:
        yaml.dump(output, file)


#%%
n_samples = 1000
config = dict(
    n_samples=n_samples,
    n_features=20,
    n_informative=10,
    n_targets=1,
    bias=200,
    effective_rank=None,
    noise=0.3,
    coef=True,
    random_state=0,
)
synreg_dataset_generator(
    config,
    name=f"Synreg very hard",
    filename=f"synreg_very_hard.yaml",
)

#%%
n_samples = 1000
config = dict(
    n_samples=n_samples,
    n_features=20,
    n_informative=10,
    n_targets=1,
    bias=200,
    effective_rank=4,
    noise=0.3,
    coef=True,
    random_state=0,
)
synreg_dataset_generator(
    config,
    name=f"Synreg hard",
    filename=f"synreg_hard.yaml",
)
