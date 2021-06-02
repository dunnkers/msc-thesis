#%%
import re

import pandas as pd
import wandb

GROUP = "cohort-1"

api = wandb.Api()
runs = api.runs("dunnkers/fseval", filters={"$or": [{"group": GROUP}]})
print(f"Found {len(runs)} runs.")

#%%
df = pd.DataFrame()
for run in runs:
    if run.state != "finished":
        continue

    config = run.config

    # extract config variables

    dataset_mapping = {
        "Boston house prices": "boston",
        "Climate Model Simulation": "climate_model_simulation",
        "Multifeat Pixel": "mfeat_pixel",
        "Synclf medium": "synclf_medium",
        "Synreg medium": "synreg_medium",
        "Additive (Chen et al.)": "chen_additive",
        "Cylinder bands": "cylinder_bands",
        "Mice Protein": "mice_protein",
        "Synclf very hard": "synclf_very_hard",
        "Synreg very hard": "synreg_very_hard",
        "Orange (Chen et al.)": "chen_orange",
        "Dresses sales": "dresses_sales",
        "Synclf easy": "synclf_easy",
        "Synreg easy": "synreg_easy",
        "Texture": "texture",
        "XOR (Chen et al.)": "chen_xor",
        "Iris Flowers": "iris",
        "Synclf hard": "synclf_hard",
        "Synreg hard": "synreg_hard",
        "Wall Robot Navigation": "wall_robot_navigation",
    }
    dataset_name = config["dataset"]["name"]
    dataset = dataset_mapping[dataset_name]

    ranker_mapping = {
        "ANOVA F-value": "anova_f_value",
        "Chi-Squared": "chi2",
        "FeatBoost": "featboost",
        "Mutual Info": "mutual_info",
        "Stability Selection": "stability_selection",
        "TabNet": "tabnet",
        "Boruta": "boruta",
        "Decision Tree": "decision_tree",
        "MultiSURF": "multisurf",
        "ReliefF": "relieff",
        "XGBoost": "xgb",
    }
    ranker_name = config["ranker"]["name"]
    ranker = ranker_mapping[ranker_name]

    normalize = lambda string: string.lower().replace("-", "_").replace(" ", "_")
    print(
        f"""fseval --multirun \
"++callbacks.wandb.id={run.id}" \
dataset={normalize(dataset)} \
"estimator@pipeline.ranker={normalize(ranker)}" \
pipeline.n_bootstraps=25 \
"++callbacks.wandb.log_metrics=false" \
"++callbacks.wandb.project=fseval" \
"++callbacks.wandb.group=cohort-1" \
"hydra/launcher=rq" \
"hydra.launcher.enqueue.result_ttl=1d" \
"hydra.launcher.enqueue.failure_ttl=60d" \
"hydra.launcher.stop_after_enqueue=true" \
"hydra.launcher.fail_hard=true" """
    )
    pass
