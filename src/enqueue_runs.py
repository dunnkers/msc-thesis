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

GROUP = "knn-cohort"

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


def get_peregrine_output(cmd):
    cmds = []
    username = os.environ.get("PEREGRINE_USERNAME")
    if os.environ.get("LMOD_sys", "") != "Linux":
        cmds = ["ssh", f"{username}@peregrine.hpc.rug.nl", cmd]
    else:
        cmds = cmd.split(" ")

    stdout, stderr = Popen(cmds, stdout=PIPE).communicate()

    output = stdout.decode("utf-8").split("\n")
    return output


#%%
print("processing runs...")
df = pd.DataFrame()
for i, run in enumerate(runs):
    should_process = run.state == "finished"
    process_text = (
        TerminalColor.blue("processing")
        if should_process
        else TerminalColor.purple("skipping")
    )
    if writing_to_file:
        print(
            f"{i}/{len(runs)} "
            + process_text
            + " run "
            + TerminalColor.yellow(run.id)
            + f" ({run.state})"
        )

    if not should_process:
        continue

    config = run.config

    run_dir = config.get("storage_provider/save_dir")
    if not run_dir:

        ### grabbing the run dir
        script_dir = f"/home/{os.environ.get('PEREGRINE_USERNAME')}/msc-thesis/jobs"
        # fetch run dir
        output = get_peregrine_output(f"sh {script_dir}/_get_run_path.sh {run.id}")
        result = output[-2]

        if result == "fail" or result == "":
            print(TerminalColor.red(f"incorrect result: {result}"))
            continue

        # get config, and assure they all exist
        try:
            p = config.get("dataset/p") or config["dataset"]["p"]
            p = int(p)
            n_bootstraps = int(config["n_bootstraps"])
            dataset_name = config.get("dataset/name") or config["dataset"]["name"]
            ranker_name = config.get("ranker/name") or config["ranker"]["name"]
        except Exception:
            print(TerminalColor.red(f"corrupt config: " + f"{run.id}"))
            continue

        run_dir = result
        n_pickles = int(output[-3])
        n_validations = min(50, p)
        n_pickles_should_be = n_bootstraps * n_validations + n_bootstraps
        if not (
            n_pickles == n_pickles_should_be
            or n_pickles == n_pickles_should_be + n_bootstraps
        ):
            print(
                TerminalColor.red(
                    f"incorrect n_pickles: "
                    + f"expected {n_pickles_should_be}, was {n_pickles}"
                )
            )
            continue
    else:
        ...

    if writing_to_file:
        print(TerminalColor.green("✓") + " found " + TerminalColor.yellow(run_dir))

    dataset = dataset_mapping[dataset_name]
    ranker = estimator_mapping[ranker_name]

    if writing_to_file:
        sys.stdout = f
    # "++storage_provider.run_id={run.id}" \
    print(
        f"""fseval --multirun \
"+backend=wandb" \
"++callbacks.wandb.id={run.id}" \
"++storage_provider.load_dir={run_dir}" \
"dataset={dataset}" \
"estimator@validator=knn" \
"estimator@ranker={ranker}" \
"validator.load_cache=never" \
"pipeline.n_bootstraps=25" \
"pipeline.n_jobs=1" \
"++callbacks.wandb.log_metrics=true" \
"++callbacks.wandb.project=fseval" \
"++callbacks.wandb.group=knn-cohort" \
"hydra/launcher=rq" \
"hydra.launcher.enqueue.result_ttl=1d" \
"hydra.launcher.enqueue.failure_ttl=60d" \
"hydra.launcher.stop_after_enqueue=true" \
"hydra.launcher.fail_hard=true" """
    )
    sys.stdout = original_stdout

print("✨ all done " + TerminalColor.green("✓"))
