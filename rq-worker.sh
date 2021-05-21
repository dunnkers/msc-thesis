#!/bin/bash
#SBATCH --time=02:00:00
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --partition=regular
#SBATCH --mem=10000
#SBATCH --output=/data/s2995697/logs/slurm-%A_%a.out

echo "Running worker in directory:"
pwd
module load Python
python -m venv venv
source venv/bin/activate
pip uninstall fseval --yes
pip install git+https://github.com/dunnkers/fseval.git@2.0
rq worker -u $REDIS_URL