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


if __name__ == "__main__":
    """EXPERIMENT RESULT:"""
    df = get_random_data(return_type="frame")
    print(df)

    wandb.init(config={"some_property": 4}, dir="/Users/dunnkers/git/msc-thesis/")
    table = wandb.Table(dataframe=df)
    wandb.log({"validation_scores": table})
    wandb.finish()
