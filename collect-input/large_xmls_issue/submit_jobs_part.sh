# 1) run cmd_mkdir and cmd_cp_xml
# 2) run cmd_submit

MAIN_DIR="OUTPUTS/data/2018/LHC18q/"
datetime=$(date "+%m-%d_%H-%M")
LOG_FILE="LOGS/submit_part_$datetime"
TTL="43200"

counter=0
for f in `find $MAIN_DIR -name "files_to_be_merged_*.xml" | grep "_part2"`; do 
    echo 
    echo $f
    year=`echo $f | cut -d "/" -f 3`
    period=`echo $f | cut -d "/" -f 4`
    run=`echo $f | cut -d "/" -f 5 | cut -c 4-`
    time_int=`echo $f | cut -d "_" -f3 | cut -d "/" -f1`
    part=`echo $f | cut -d "_" -f 8 | cut -c 5`
    params="$year $period $run $time_int"  # without $part
    rel_dir=$(dirname $f)
    target_dir="/alice/cern.ch/user/s/sbysiak/grid-jobs/$rel_dir"
    source_dir="$rel_dir"
    output_dir="$target_dir/part_$part"
    cmd_submit="alien_submit mergeJDLPart $year $period $run $time_int $part $TTL"
    cmd_mkdir="alien_mkdir $output_dir"
    cmd_cp_xml="alien_cp file:$f alien:$target_dir"

    is_submitted_whole=$(grep "$params" already_submitted.txt | grep -v "part")
    is_submitted_part=$(grep "$params" already_submitted.txt | grep "part$part")
    if [[ $is_submitted_whole  != "" ]]; then 
        echo "job with such params is already submitted (whole) - doing nothing"
    elif [[ $is_submitted_part  != "" ]]; then 
        echo "job with such params is already submitted (part) - doing nothing"
    else
        for cmd in "$cmd_mkdir" "$cmd_cp_xml"; do
        #for cmd in "$cmd_submit"; do
            echo $cmd
            eval $cmd
            STATUS=$? 
            echo "STATUS = $STATUS"
            if (( $STATUS != 0 )); then
                printf "$cmd \n\t processed with error code=$STATUS\n" >> $LOG_FILE
            fi
        done
        counter=$(( counter+1 ))
        echo "N = $counter files submitted / processed"
    fi
done
