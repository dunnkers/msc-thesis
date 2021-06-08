cd /scratch/$PEREGRINE_USERNAME/fseval/multirun
run_dir=$(find ./ -maxdepth 5 -name *$1 | tail -n 1)
run_dir_abs=$(realpath $run_dir)
echo $run_dir_abs/files
