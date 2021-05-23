#%%
import numpy as np
import pandas as pd
import seaborn as sns
import wandb


def get_random_data(return_type: str):
    df = pd.DataFrame()
    bootstrap_scores = []

    bootstrap_states = list(range(1, 30 + 1))
    for bootstrap_state in bootstrap_states:

        all_features_to_select = list(range(1, 10 + 1))
        subset_scores = []
        for n_features_to_select in all_features_to_select:
            base_score = n_features_to_select / 20
            if n_features_to_select == 2:
                base_score = 0.4
            if n_features_to_select == 3:
                base_score = 0.5
            if n_features_to_select == 4:
                base_score = 0.3
            score = np.random.rand() * 0.5 + base_score

            # log
            metrics = {
                "n_features_to_select": n_features_to_select,
                "score": score,
                "bootstrap_state": bootstrap_state,
            }
            metrics_df = pd.DataFrame([metrics])
            df = df.append(metrics_df)
            subset_scores.append(score)
        bootstrap_scores.append(subset_scores)

    if return_type == "frame":
        return df
    elif return_type == "2d-array":
        return bootstrap_states, all_features_to_select, bootstrap_scores
    else:
        raise ValueError(f"incorrect `return_type`: {return_type}")


#%%
if __name__ == "__main__":
    """EXPERIMENT RESULT:
    This setup will cause `n_features_to_select` to be non-monotonically increasing,
    and when setting the x-axis to `n_features_to_select`, the scores shown will be
    0.5 and 0.6, respectively.
    """
    wandb.init(config={"some_property": 4})

    wandb.log({"n_features_to_select": 1, "score": 0.5, "bootstrap_state": 1})
    wandb.log({"n_features_to_select": 2, "score": 0.6, "bootstrap_state": 1})

    wandb.log({"n_features_to_select": 1, "score": 0.7, "bootstrap_state": 2})
    wandb.log({"n_features_to_select": 2, "score": 0.8, "bootstrap_state": 2})

    wandb.finish()

#%%
if __name__ == "__main__":
    """EXPERIMENT RESULT:
    `n_features_to_select` will be monotonically increasing, but the scores shown
    will still be 0.5 and 0.6, respectively.

    https://wandb.ai/dunnkers/msc-thesis-experiments_009___wandb-aggregation-behavior/runs/ssvs64y8
    """
    wandb.init(config={"some_property": 4})

    wandb.log({"n_features_to_select": 1, "score": 0.5, "bootstrap_state": 1})
    wandb.log({"n_features_to_select": 1, "score": 0.7, "bootstrap_state": 2})

    wandb.log({"n_features_to_select": 2, "score": 0.6, "bootstrap_state": 1})
    wandb.log({"n_features_to_select": 2, "score": 0.8, "bootstrap_state": 2})

    wandb.finish()

#%%
if __name__ == "__main__":
    """EXPERIMENT RESULT:
    `n_features_to_select` will be monotonically increasing, but the scores shown
    will be 0.7 and 0.8, respectively.

    https://wandb.ai/dunnkers/msc-thesis-experiments_009___wandb-aggregation-behavior/runs/2ztl3sej

    ➡ grouping by both `score` and `bootstrap_state` will cause very wrong metrics:
    it will aggregate the y-axis over both of these scores.
    """
    wandb.init(config={"some_property": 4})

    wandb.log({"n_features_to_select": 1, "score": 0.5, "bootstrap_state": 1}, step=1)
    wandb.log({"n_features_to_select": 1, "score": 0.7, "bootstrap_state": 2}, step=1)

    wandb.log({"n_features_to_select": 2, "score": 0.6, "bootstrap_state": 1}, step=2)
    wandb.log({"n_features_to_select": 2, "score": 0.8, "bootstrap_state": 2}, step=2)

    wandb.finish()


#%%
if __name__ == "__main__":
    """EXPERIMENT RESULT:
    works: creates a custom chart! ✅
    """
    bootstrap_states, all_features_to_select, bootstrap_scores = get_random_data(
        return_type="2d-array"
    )

    wandb.init(config={"some_property": 4})
    wandb.log(
        {
            "validation_performance_all_bootstraps": wandb.plot.line_series(
                xs=all_features_to_select,
                ys=bootstrap_scores,
                keys=[
                    f"random_state={bootstrap_state:02}"
                    for bootstrap_state in bootstrap_states
                ],
                title="Validation performance for all bootstraps",
            )
        }
    )
    wandb.finish()


#%%
if __name__ == "__main__":
    """EXPERIMENT RESULT:
    works: but very ugly chart - not native with wandb.
    """
    df = get_random_data(return_type="frame")
    print(df)
    g = sns.lineplot(data=df, x="n_features_to_select", y="score")

    wandb.init(config={"some_property": 4})
    wandb.log({"custom_plot": g.figure})
    wandb.finish()


#%%
if __name__ == "__main__":
    """EXPERIMENT RESULT:
    works: very nice custom chart using `dunnkers/fseval/validation-score-bootstraps`
    custom vega chart 👍🏻
    """
    df = get_random_data(return_type="frame")
    print(df)

    wandb.init(config={"some_property": 4})
    table = wandb.Table(dataframe=df)
    fields = {
        "n_features_to_select": "step",
        "score": "lineVal",
        "bootstrap_state": "lineKey",
    }

    bootstrap_plot = wandb.plot_table(
        vega_spec_name="dunnkers/fseval/validation-score-bootstraps",
        data_table=table,
        fields=fields,
    )
    wandb.log({"bootstrap_plot": bootstrap_plot})
    wandb.finish()

#%%
if __name__ == "__main__":
    """EXPERIMENT RESULT:"""
    df = get_random_data(return_type="frame")
    print(df)

    wandb.init(config={"some_property": 4}, dir="/Users/dunnkers/git/msc-thesis/")
    table = wandb.Table(dataframe=df)
    wandb.log({"validation_scores": table})
    wandb.finish()
