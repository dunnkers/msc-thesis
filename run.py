import hydra
import mleval # must import mleval at top level
from omegaconf import DictConfig
from mleval.tasks import Task
from mleval.datasrc import DataSource

@hydra.main(config_path='conf', config_name='config')
def run(cfg: DictConfig) -> None:
    datasrc: DataSource = hydra.utils.instantiate(cfg.datasrc)
    task: Task = hydra.utils.instantiate(cfg.task, datasrc=datasrc)
    task.run()

if __name__ == "__main__":
    run()