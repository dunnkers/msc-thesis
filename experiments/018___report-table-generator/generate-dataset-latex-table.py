import pandas as pd
import wandb
from fseval.types import TerminalColor
from fseval.utils.dict_utils import dict_merge
from hydra.utils import instantiate

print("importing hydra utils...")
from fseval.utils.hydra_utils import get_group_configs, get_group_options

print("hydra utils imported " + TerminalColor.green("✓"))

# construct dataset mapping
print("Constructing dataset mapping...")
dataset_cfgs = get_group_configs("dataset")
dataset_names = [dataset_cfg.get("name") for dataset_cfg in dataset_cfgs]
dataset_options = get_group_options("dataset")
dataset_mapping = dict(zip(dataset_names, dataset_options))
print("dataset mapping constructed " + TerminalColor.green("✓"))


datasets = {}

for dataset_cfg in dataset_cfgs:
    name = dataset_cfg["name"]
    datasets[name] = datasets.get(name) or {}
    dict_merge(datasets[name], dataset_cfg)


for dataset in dataset_cfgs:
    name = dataset["name"]

    ds_loader = instantiate(dataset)
    ds = ds_loader.load()

    n = ds.n
    p = ds.p
    multioutput = ds.multioutput
    domain = dataset.get("domain", "") or "-"
    group = dataset.get("group", "") or "-"

    latex = ""
    latex += name
    latex += r" & "

    latex += str(n)
    latex += r" & "

    latex += str(p)
    latex += r" & "

    latex += "Yes" if multioutput else "No"
    latex += r" & "

    latex += domain.capitalize()
    latex += r" & "

    latex += group.capitalize()

    latex += r" \\ "

    print(latex)
    print(r"\hline")
...
