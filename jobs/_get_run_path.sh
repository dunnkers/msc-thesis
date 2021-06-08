search_dir=/scratch/$PEREGRINE_USERNAME/fseval/multirun
run_dir=$(find $search_dir -maxdepth 5 -name *$1 | tail -n 1)
run_dir_abs=$(realpath $run_dir)
run_dir_files=$run_dir_abs/files
has_pickle=$(find $run_dir_files -name *.pickle -print | head -n 1 | wc -l)

if [ -d "$run_dir_files" -a $has_pickle -eq "1" ]; then
    echo $run_dir_files
else
    echo "fail"
fi

