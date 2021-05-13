#%%
import wandb

api = wandb.Api()

runs = api.runs(
    "dunnkers/toy-wandb-fs",
    filters={
        "$or": [{"config.ranker.name": "TabNet", "config.dataset.name": "Iris Flowers"}]
    }
)
print("Found %i" % len(runs))


#%%
import wandb

api = wandb.Api()
run = api.run("dunnkers/msc-thesis-experiments_007___wandb-run-id-multiprocessing/684")
print(run.history())
