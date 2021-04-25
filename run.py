import hydra
import mleval # must import mleval at top level
from omegaconf import DictConfig

@hydra.main(config_path='conf', config_name='config')
def run(cfg: DictConfig) -> None:
    task = hydra.utils.instantiate(cfg.task)
    task.run()

if __name__ == "__main__":
    run()