# mleval
A Machine Learning benchmarking library. Neatly integrates with wandb and sklearn. Uses Hydra as a config parser.



## Architecture
Uses [RQ](https://python-rq.org/) (Redis Queue) as a launcher for Hydra. For this reason we require a Redis server. Follow Hydra RQ [instructions](https://hydra.cc/docs/next/plugins/rq_launcher/): set all necessary environment variables. Also:

- Take note of whether your Redis server uses SSL or not `redis` versus `rediss`. In the case of SSL, we require extra config: