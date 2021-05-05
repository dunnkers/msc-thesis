#!/bin/bash
#SBATCH --time=00:30:00
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --partition=short
#SBATCH --mem=10000
#SBATCH --output=/data/$USER/logs/slurm-%A_%a.out

module load Python
python -m venv venv
source venv/bin/activate
pip install git+https://github.com/dunnkers/fseval.git@2.0
rq worker -u $REDIS_URL