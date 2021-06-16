import pandas as pd
import wandb
from fseval.types import TerminalColor
from fseval.utils.dict_utils import dict_merge

print("importing hydra utils...")
from fseval.utils.hydra_utils import get_group_configs, get_group_options

print("hydra utils imported " + TerminalColor.green("✓"))

# construct estimator mapping
print("Constructing estimator mapping...")
estimator_cfgs = get_group_configs("estimator")
estimator_names = [estimator_cfg.get("name") for estimator_cfg in estimator_cfgs]
estimator_options = get_group_options("estimator")
estimator_mapping = dict(zip(estimator_names, estimator_options))
print("estimator mapping constructed " + TerminalColor.green("✓"))


estimators = {}

for estimator_cfg in estimator_cfgs:
    name = estimator_cfg["name"]
    estimators[name] = estimators.get(name) or {}
    dict_merge(estimators[name], estimator_cfg)

    if "classifier" in estimator_cfg:
        dict_merge(estimators[name], estimator_cfg["classifier"])

    if "regressor" in estimator_cfg:
        dict_merge(estimators[name], estimator_cfg["regressor"])

for name, estimator in estimators.items():
    classification = estimator.get("classifier", "")
    regression = estimator.get("regressor", "")
    multioutput = estimator.get("multioutput", "")
    estimates_feature_importances = estimator.get("estimates_feature_importances", "")
    estimates_feature_support = estimator.get("estimates_feature_support", "")
    estimates_feature_ranking = estimator.get("estimates_feature_ranking", "")

    latex = ""
    latex += name
    latex += r" & "

    latex += r"\checkmark" if classification else ""
    latex += r" & "

    latex += r"\checkmark" if regression else ""
    latex += r" & "

    latex += r"\checkmark" if multioutput else ""
    latex += r" & "

    latex += r"\checkmark" if estimates_feature_importances else ""
    latex += r" & "

    latex += r"\checkmark" if estimates_feature_support else ""
    latex += r" & "

    latex += r"\checkmark" if estimates_feature_ranking else ""
    latex += r" \\ "

    print(latex)
    print(r"\hline")
...
