helpformat=$(sacct --helpformat)
params=$(echo $helpformat | sed 's/ /,/g')
sacct --format='$params' \
    --starttime 2021-05-20 \
    -u $USER \
    --parsable2 \
    --verbpse \
    --delimiter=';' \
    > /data/$USER/logs/sacct.csv