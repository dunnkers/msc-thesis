#%%
import os

import numpy as np
import pandas as pd
import seaborn as sns
import yaml
from matplotlib import pyplot as plt
from sklearn.datasets import make_classification
from sklearn.model_selection import cross_val_score
from sklearn.tree import DecisionTreeClassifier
from sklearn.utils import resample


def synclf_dataset_generator(config, name, filename):
    """Synclf dataset generator. Given a `make_classification` config, this generates
    apprioprate yaml files, compatible with fseval."""

    X, y = make_classification(**config)

    reg = DecisionTreeClassifier()
    n_folds = 5
    df = pd.DataFrame()
    n, p = np.array(X).shape

    for n_samples_frac in range(1, 10 + 1):
        n_samples = round(n_samples_frac / 10 * config["n_samples"])
        print(f"using {n_samples} samples..")
        for n_runs in range(1):
            X_new, y_new = resample(X, y, replace=False, n_samples=n_samples)
            score = cross_val_score(reg, X_new, y_new, cv=n_folds)
            res = pd.DataFrame(
                {"score": score, "fold": range(n_folds), "n_samples": n_samples}
            )
            df = df.append(res)

    sns.scatterplot(data=df, x="n_samples", y="score")
    plt.title("validation performance")
    plt.tight_layout()
    plt.show()

    best_index = df["score"].argmax()
    print(f"n={n} best score:")
    print(df.iloc[best_index])

    n_informative = config["n_informative"]
    feature_importances_ground_truth = {f"X[:, 0:{n_informative}]": 1.0}

    output = dict(
        name=name,
        task="classification",
        group="Synclf",
        domain="synthetic",
        adapter={
            "_target_": "sklearn.datasets.make_classification",
            **config,
        },
        feature_importances=feature_importances_ground_truth,
    )

    filedir = "/Users/dunnkers/git/fseval/fseval/conf/dataset"
    filepath = os.path.join(filedir, filename)
    with open(filepath, "w") as file:
        yaml.dump(output, file)


#%%
n_samples = 1000
config = dict(
    n_samples=10000,
    n_features=20,
    n_informative=2,
    n_redundant=0,
    n_repeated=0,
    n_classes=2,
    n_clusters_per_class=2,
    class_sep=1.0,
    random_state=0,
)
synclf_dataset_generator(
    config,
    name=f"Synclf easy",
    filename=f"synclf_easy.yaml",
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
