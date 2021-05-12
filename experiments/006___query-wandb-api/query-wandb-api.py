#%%
import wandb

api = wandb.Api()

runs = api.runs(
    "dunnkers/toy-wandb-fs",
    {"$or": [{"ranker.name": "Chi-Squared"}]},
)
print("Found %i" % len(runs))


#%%
import wandb

api = wandb.Api()
run = api.run("dunnkers/msc-thesis-experiments_007___wandb-run-id-multiprocessing/684")
print(run.history())
