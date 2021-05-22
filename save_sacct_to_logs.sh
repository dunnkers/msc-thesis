helpformat=$(sacct --helpformat)
params=$(echo $helpformat | sed 's/ /,/g')
sacct --format="$params" \
    --starttime 2021-05-20 \
    -u $USER \
    --parsable2 \
    --verbose \
    --delimiter=';' \
    > /data/$USER/logs/sacct.csv