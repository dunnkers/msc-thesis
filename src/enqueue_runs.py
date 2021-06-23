import os
import re
import subprocess
import sys
from io import StringIO
from subprocess import PIPE, Popen

import pandas as pd
import wandb
from fseval.types import TerminalColor
from fseval.utils.hydra_utils import get_group_configs, get_group_options

# stdout
original_stdout = sys.stdout
writing_to_file = sys.argv[1:]
if writing_to_file:
    outputfile = sys.argv[1]
    f = open(outputfile, "w")
else:
    print(
        TerminalColor.red("⚠️ no output file configured. Set as first arg to program.")
    )
# start wandb
config = {}
if writing_to_file:
    config["outputfile"] = outputfile
slurm_job = os.environ.get("SLURM_JOB_ID", None)
group_and_queue_name = "fix-fitting-time"
wandb.init(
    project="fseval-enqueueing", config=config, id=slurm_job, name=group_and_queue_name
)


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
GROUP = "cohort-1"
runs = api.runs("dunnkers/fseval", filters={"$or": []})


def specific_runs(run_ids):
    return lambda run: run.id in run_ids


# runs = list(filter(specific_runs(["1azi6ic6"]), runs))
print(f"Found {TerminalColor.yellow(str(len(runs)))} runs.")


def get_peregrine_output(cmd):
    cmds = []
    username = os.environ.get("PEREGRINE_USERNAME")
    if os.environ.get("LMOD_sys", "") != "Linux":
        cmds = ["ssh", f"{username}@peregrine.hpc.rug.nl", cmd]
    else:
        cmds = cmd.split(" ")

    stdout, stderr = Popen(cmds, stdout=PIPE).communicate()

    decoded = stdout.decode("utf-8")

    file = StringIO(decoded)
    df = pd.read_csv(file)

    return df


#%%
print("processing runs...")
df = pd.DataFrame()
for i, run in enumerate(runs):
    config = run.config

    # get config, and assure they all exist
    try:
        p = config.get("dataset/p") or config["dataset"]["p"]
        p = int(p)
        n_bootstraps = int(config["n_bootstraps"])
        dataset_name = config.get("dataset/name") or config["dataset"]["name"]
        ranker_name = config.get("ranker/name") or config["ranker"]["name"]
        validator_name = config.get("validator/name") or config["validator"]["name"]
        group = (
            config.get("callbacks/wandb/group")
            or config["callbacks"]["wandb"]["group"]
            or ""
        )
        dataset_group = config.get("dataset/group", None)
        if (
            dataset_group is None
            and config.get("dataset")
            and config.get("dataset").get("group")
        ):
            dataset_group = config["dataset"]["group"]
    except Exception as e:
        print(TerminalColor.red(f"corrupt config: " + f"{run.id}"))
        print(e)
        continue

    ### SHOULd PROCESS??
    # should_process = run.state == "finished"
    if dataset_group == "Synclf" or dataset_group == "Synreg":
        print("not processing: synclf or synreg dataset.")
        continue

    print(
        f"{i + 1}/{len(runs)} "
        + TerminalColor.blue("processing")
        + " run "
        + TerminalColor.yellow(run.id)
        + f" ({run.state})"
    )

    save_dir = config.get("storage_provider/save_dir")
    print(f"(found `save_dir={save_dir}`, but not using it.")
    # if not run_dir:

    ### grabbing the run dir
    script_dir = f"/home/{os.environ.get('PEREGRINE_USERNAME')}/msc-thesis/jobs"
    # fetch run dir
    df = get_peregrine_output(f"sh {script_dir}/_get_run_path.sh {run.id}")

    if df.empty:
        print(TerminalColor.red(f"no run dir found, empty dataframe."))
        continue

    print(f"{len(df)} storage places found.")

    for i, row in df.iterrows():
        run_dir = row["storage_dir"]
        n_pickles = row["n_pickles"]

        n_validations = min(50, p)
        n_pickles_should_be = n_bootstraps * n_validations + n_bootstraps

        if (
            n_pickles == n_pickles_should_be
            or n_pickles == n_pickles_should_be + n_bootstraps
        ):
            # print(f"using: {run_dir} " + TerminalColor.green("✓"))
            print(TerminalColor.green("✓") + " chose: " + TerminalColor.yellow(run_dir))
            print(f"found {TerminalColor.yellow(n_pickles)} pickle files.")
            break

    if not run_dir:
        print("no run dir found.")

        print(
            TerminalColor.red(
                f"n_pickles were: "
                + df["n_pickles"].values
                + " but expected: "
                + n_pickles_should_be
            )
        )

    dataset = dataset_mapping[dataset_name]
    ranker = estimator_mapping[ranker_name]
    validator = estimator_mapping[validator_name]

    if writing_to_file:
        sys.stdout = f
        # "++storage_provider.run_id={run.id}" \
        # "validator.load_cache=never" \
        print(
            f"""fseval --multirun \
    "callbacks=[wandb]" \
    "+storage_provider=local" \
    "++storage_provider.load_dir={run_dir}" \
    "+dataset={dataset}" \
    "+estimator@validator={validator}" \
    "+estimator@ranker={ranker}" \
    "ranker.load_cache=must" \
    "n_bootstraps=25" \
    "n_jobs=1" \
    "++callbacks.wandb.id={run.id}" \
    "++callbacks.wandb.log_metrics=false" \
    "++callbacks.wandb.project=fseval" \
    "++callbacks.wandb.resume=allow" \
    "++callbacks.wandb.group={group_and_queue_name}" \
    "hydra/launcher=rq" \
    "hydra.launcher.queue={group_and_queue_name}" \
    "hydra.launcher.enqueue.result_ttl=1d" \
    "hydra.launcher.enqueue.failure_ttl=60d" \
    "hydra.launcher.stop_after_enqueue=true" \
    "hydra.launcher.fail_hard=true" """
        )
        sys.stdout = original_stdout

print("✨ all done " + TerminalColor.green("✓"))
wandb.finish()
