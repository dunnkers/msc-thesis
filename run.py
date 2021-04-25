import hydra
import mleval # must import mleval at top level
from omegaconf import DictConfig
from mleval.datasrc import DataSource
from mleval.tasks import Task
from mleval.output import Output

@hydra.main(config_path='conf', config_name='config')
def run(cfg: DictConfig) -> None:
    datasrc: DataSource = hydra.utils.instantiate(cfg.datasrc)
    task: Task = hydra.utils.instantiate(cfg.task, datasrc=datasrc)
    result = task.run()
    
    output: Output = hydra.utils.instantiate(cfg.output)
    output.write(result)

if __name__ == "__main__":
    run()