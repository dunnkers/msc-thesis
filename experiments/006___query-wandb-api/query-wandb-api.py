#%%
import wandb

api = wandb.Api()

runs = api.runs(
    "dunnkers/toy-wandb-fs",
    {"$or": [{"ranker.name": "Chi-Squared"}]},
)
print("Found %i" % len(runs))
