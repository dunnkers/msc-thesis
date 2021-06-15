import re
import time

import wandb
from fseval.types import TerminalColor
from tqdm import tqdm

for i in range(100):
    try:

        # retrieve runs from API
        api = wandb.Api()
        runs = api.runs("dunnkers/fseval-archive")
        print(f"Found {TerminalColor.yellow(str(len(runs)))} runs.")

        def is_ranker(run, ranker):
            cfg = run.config
            ranker_name = (
                cfg.get("ranker/name")
                or (cfg.get("ranker") and cfg.get("ranker").get("name"))
                or (
                    cfg.get("pipeline")
                    and cfg.get("pipeline").get("ranker")
                    and cfg.get("pipeline").get("ranker").get("name")
                )
            )

            return ranker_name and ranker_name == ranker

        is_featboost = lambda run: is_ranker(run, "FeatBoost")

        # runs = list(filter(is_featboost, runs))
        # print(f"of which {len(runs)} are featboost runs.")

        runprog = tqdm(runs)
        for run in runprog:
            files = run.files()

            runprog.set_description(f"run {run.id}    ({len(files)} files)...")

            def is_pickle(file):
                regexp = r".*\[.*\].pickle"
                match = re.match(regexp, file.name)
                return bool(match)

            files_to_process = list(filter(is_pickle, files))
            progbar = tqdm(files_to_process)
            for file in progbar:
                progbar.set_description(f"deleting {file.name}...")
                file.delete()
                time.sleep(0.05)
        break
    except Exception:
        print("failed, starting again.")
