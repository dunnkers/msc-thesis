#%%
import sys

import numpy as np

import wandb

ROWS = 1000


def f(i):
    print(f"f({i})")

    np.random.seed(0)
    run_id = np.random.randint(1000)
    print(f"run_id={run_id}")

    data = np.random.normal(size=ROWS)
    gaussian_value = data[int(i)]
    print(f"gaussian_value={gaussian_value}")

    # wandb
    wandb.init(id=str(run_id), resume="allow")
    wandb.log({"gaussian_value": gaussian_value})
    wandb.finish()


if __name__ == "__main__":
    f(sys.argv[1])
