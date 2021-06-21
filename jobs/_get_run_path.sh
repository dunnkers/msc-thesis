#!/bin/bash

# Config
search_dir=/scratch/$PEREGRINE_USERNAME/fseval/multirun
run_id="$1"

# CSV header
echo "run_dir,storage_dir,n_pickles"

find $search_dir -maxdepth 5 -name *$run_id | while read wandb_dir_rel; do
    wandb_dir=$(realpath $wandb_dir_rel)
    hydra_dir=$(realpath $wandb_dir_rel/../..)

    # find wandb dir pickle files
    wandb_pickles=$(find $wandb_dir/files -maxdepth 1 -name *.pickle -print | wc -l)
    echo "$wandb_dir,$wandb_dir/files,$wandb_pickles"

    # find hydra dir pickle files
    hydra_pickles=$(find $hydra_dir -maxdepth 1 -name *.pickle -print | wc -l)

    echo "$wandb_dir,$hydra_dir,$hydra_pickles"
done
