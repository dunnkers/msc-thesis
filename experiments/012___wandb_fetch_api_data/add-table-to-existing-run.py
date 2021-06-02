#%%
import wandb

GROUP = "cohort-1"

api = wandb.Api()
runs = api.runs("dunnkers/fseval-stats", filters={"$or": [{"group": GROUP}]})
print(f"Found {len(runs)} runs.")

#%%
run = runs[len(runs) - 1]
run

df = pd.DataFrame([{"a": 3}])

# construct table
table = wandb.Table(dataframe=df)

# construct artifact
artifact_name = f"run-{run.id}-meta_data"
artifact = wandb.Artifact(artifact_name, type="run_table")
artifact.add(table, "data")
artifact.save()

#%%
# artifact = api.artifact(f"dunnkers/project/{artifact_name}")
# run.log_artifact(artifact)
