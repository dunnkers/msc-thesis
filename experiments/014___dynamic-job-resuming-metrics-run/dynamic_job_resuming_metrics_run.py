import os
import re
import subprocess
import sys
from subprocess import PIPE, Popen

import pandas as pd
import wandb
from fseval.types import TerminalColor

print("importing hydra utils...")
from fseval.utils.hydra_utils import get_group_configs, get_group_options

print("hydra utils imported " + TerminalColor.green("✓"))

GROUP = "cohort-1"

# construct dataset mapping
print("Constructing dataset mapping...")
dataset_cfgs = get_group_configs("dataset")
dataset_names = [dataset_cfg.get("name") for dataset_cfg in dataset_cfgs]
dataset_options = get_group_options("dataset")
dataset_mapping = dict(zip(dataset_names, dataset_options))
print("dataset mapping constructed " + TerminalColor.green("✓"))

# construct estimator mapping
print("Constructing estimator mapping...")
estimator_cfgs = get_group_configs("estimator")
estimator_names = [estimator_cfg.get("name") for estimator_cfg in estimator_cfgs]
estimator_options = get_group_options("estimator")
estimator_mapping = dict(zip(estimator_names, estimator_options))
print("estimator mapping constructed " + TerminalColor.green("✓"))

# retrieve runs from API
api = wandb.Api()
runs = api.runs("dunnkers/fseval", filters={"$or": [{"group": GROUP}]})
print(f"Found {TerminalColor.yellow(str(len(runs)))} runs.")

# stdout
original_stdout = sys.stdout
writing_to_file = sys.argv[1:]
if writing_to_file:
    outputfile = sys.argv[1]
    f = open(outputfile, "w")

#%%
print("processing runs...")
df = pd.DataFrame()
for run in runs:
    should_process = run.state == "finished"
    process_text = (
        TerminalColor.blue("processing")
        if should_process
        else TerminalColor.purple("skipping")
    )
    if writing_to_file:
        print(process_text + " run " + TerminalColor.yellow(run.id) + f" ({run.state})")

    if not should_process:
        continue

    config = run.config

    ### grabbing the run dir
    script_dir = "~/msc-thesis/experiments/014___dynamic-job-resuming-metrics-run"
    username = os.environ.get("PEREGRINE_USERNAME")
    # fetch run dir
    script_path = f"{script_dir}/get_run_path.sh"
    stdout, stderr = Popen(
        ["ssh", f"{username}@peregrine.hpc.rug.nl", f"sh {script_path} {run.id}"],
        stdout=PIPE,
    ).communicate()
    run_dir = stdout.decode("utf-8").replace("\n", "")
    # verify run dir
    script_path = f"{script_dir}/verify_path.sh"
    stdout, stderr = Popen(
        ["ssh", f"{username}@peregrine.hpc.rug.nl", f"sh {script_path} {run_dir}"],
        stdout=PIPE,
    ).communicate()
    verified = stdout.decode("utf-8").replace("\n", "")
    # has cache
    stdout, stderr = Popen(
        ["ssh", f"{username}@peregrine.hpc.rug.nl", f"ls {run_dir}/*.pickle | wc -l"],
        stdout=PIPE,
    ).communicate()
    n_cached = stdout.decode("utf-8").replace("\n", "")
    n_cached = int(n_cached)

    if verified != "true":
        print(TerminalColor.red(f"incorrect run dir: {run_dir}"))
        continue

    if not (n_cached > 0):
        print(
            TerminalColor.purple(
                "⚠️ " + str(n_cached) + f" pickle files in dir: {run_dir}"
            )
        )
        continue

    if writing_to_file:
        print(
            TerminalColor.green("✓")
            + " found "
            + TerminalColor.cyan(str(n_cached))
            + " pickle files in dir: "
            + TerminalColor.yellow(run_dir)
        )

    dataset_name = config["dataset"]["name"]
    dataset = dataset_mapping[dataset_name]
    ranker_name = config["ranker"]["name"]
    ranker = estimator_mapping[ranker_name]

    if writing_to_file:
        sys.stdout = f
    print(
        f"""fseval --multirun \
"++callbacks.wandb.id={run.id}" \
"++storage_provider.local_dir={run_dir}" \
dataset={dataset} \
"estimator@ranker={ranker}" \
pipeline.n_bootstraps=25 \
pipeline.n_jobs=1 \
"++callbacks.wandb.log_metrics=false" \
"++callbacks.wandb.project=fseval" \
"++callbacks.wandb.group=cohort-1" \
"hydra/launcher=rq" \
"hydra.launcher.enqueue.result_ttl=1d" \
"hydra.launcher.enqueue.failure_ttl=60d" \
"hydra.launcher.stop_after_enqueue=true" \
"hydra.launcher.fail_hard=true" """
    )
    sys.stdout = original_stdout

print("✨ all done " + TerminalColor.green("✓"))
