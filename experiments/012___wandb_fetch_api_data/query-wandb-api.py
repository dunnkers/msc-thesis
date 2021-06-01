#%%
import re

import pandas as pd
import wandb

GROUP = "cohort-1"

api = wandb.Api()
runs = api.runs("dunnkers/fseval", filters={"$or": [{"group": GROUP}]})
print(f"Found {len(runs)} runs.")

df = pd.DataFrame()
for run in runs:
    # get config and summary from run
    config = run._attrs["config"]
    summary = run.summary._json_dict

    # extract summary 'best' scores
    summary_best = summary.get("best", {})
    summary_best_ranker = summary_best.get("ranker", {})
    summary_best_ranker_score = summary_best_ranker.get("r2_score", None)
    summary_best_validator = summary_best.get("validator", {})
    summary_best_validator_score = summary_best_validator.get("score", None)

    # determine whether has score
    has_ranking = "ranking" if bool(summary_best_ranker_score) else None
    has_validation = "validation" if bool(summary_best_validator_score) else None
    has_scores = " + ".join(pd.Series([has_ranking, has_validation]).dropna())

    # extract config variables
    dataset = config["dataset"]["name"]
    multioutput = config["dataset"]["multioutput"]
    task = config["dataset"]["task"]
    task = re.match(r"Task\.(.*)", task).group(1)
    ranker = config["ranker"]["name"]

    # create result object
    result = {}
    result["state"] = run.state
    result["dataset"] = dataset
    result["task"] = task
    result["ranker"] = ranker
    result["best_ranker_score"] = summary_best_ranker_score
    result["best_validator_score"] = summary_best_validator_score
    result["has_scores"] = has_scores

    result_df = pd.DataFrame([result])
    df = df.append(result_df)
    print(f"processed run {run.id} ({ranker} on `{dataset}` dataset)")

failures = df[df["state"].isin(["crashed", "failed"])]
successes = df[df["state"].isin(["running", "finished"])]
classification = successes[successes["task"] == "classification"]
regression = successes[successes["task"] == "regression"]
print(f"{len(failures)} failures")
print(f"{len(successes)} successes")
print(f"\tof which{len(classification)} classification")
print(f"\tand{len(regression)} regression")

run_id = f"failures"
wandb.init(project="fseval-stats", id=run_id, name=run_id, group=GROUP)
table = wandb.Table(dataframe=failures)
wandb.log(dict(results=table))
wandb.finish()


run_id = f"successes"
wandb.init(project="fseval-stats", id=run_id, name=run_id, group=GROUP)
table = wandb.Table(dataframe=successes)
wandb.log(dict(results=table))
wandb.finish()


run_id = f"classification"
wandb.init(project="fseval-stats", id=run_id, name=run_id, group=GROUP)
table = wandb.Table(dataframe=classification)
wandb.log(dict(results=table))
wandb.finish()


run_id = f"regression"
wandb.init(project="fseval-stats", id=run_id, name=run_id, group=GROUP)
table = wandb.Table(dataframe=regression)
wandb.log(dict(results=table))
wandb.finish()
