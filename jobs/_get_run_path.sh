run_dir=$(find /scratch/$PEREGRINE_USERNAME/fseval/multirun -maxdepth 5 -name * | tail -n 1)
run_dir_abs=$(realpath $run_dir)
run_dir_files=$run_dir_abs/files
has_pickle=$(find $run_dir_files -name *.pickle -print | head -n 1 | wc -l)

if [ -d "$run_dir_files" ] && ["$has_pickle" -gt 0]; then
    echo $run_dir_files
else
    echo ""
fi

