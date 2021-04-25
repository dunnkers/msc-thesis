from dataclasses import dataclass
import wandb

@dataclass
class Output:
    def write(self) -> None: raise NotImplementedError

@dataclass
class Stdout(Output):
    def write(self, data) -> None:
        print(data)

# @dataclass
# class WandbArtifact(Output):
#     def write(self, data) -> None:
#         artifact = wandb.Artifact(ds.name, type='feature-ranking')
#         columns = [f'X{p}' for p in range(1, p_ds + 1)]
#         table = wandb.Table(columns=columns,
#             data=[fimps])
#         artifact.add(table, "chi2")
#         run.log_artifact(artifact)