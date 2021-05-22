#!/bin/bash
#SBATCH --time=00:15:00
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --partition=short
#SBATCH --job-name=logs-uploader
#SBATCH --mem=2500
#SBATCH --output=/data/s2995697/slurm/logs/slurm-%A_%a.out

module load Python
python -m venv venv
source venv/bin/activate
pip install humanfriendly pandas wandb
sh src/sacct_to_csv.sh $SACCT_JOB_ID | python src/sacct_csv_to_wandb.py