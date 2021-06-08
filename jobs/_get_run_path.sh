#!/bin/bash
search_dir=/scratch/$PEREGRINE_USERNAME/fseval/multirun
run_dir=$(find $search_dir -maxdepth 5 -name *$1 | tail -n 1)
run_dir_abs=$(realpath $run_dir)
run_dir_files=$run_dir_abs/files
echo "found dir: $run_dir_files"

if [ -d "$run_dir_files" ]; then
    echo $run_dir_files
else
    echo "fail"
fi

