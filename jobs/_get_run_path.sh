#!/bin/bash
search_dir=/scratch/$PEREGRINE_USERNAME/fseval/multirun
run_dir=$(find $search_dir -maxdepth 5 -name *$1 | tail -n 1)
run_dir_abs=$(realpath $run_dir)
run_dir_files=$run_dir_abs/files
echo "found dir: $run_dir_files"
n_pickles=$(find $run_dir_files -maxdepth 1 -name *.pickle -print | wc -l)

if [ -d "$run_dir_files" -a "$n_pickles" -gt "0" ]; then
    echo $n_pickles
    echo $run_dir_files
else
    echo "found $n_pickles pickle files: insufficient"
    echo "fail"
fi

