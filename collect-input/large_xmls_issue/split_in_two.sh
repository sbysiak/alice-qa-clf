MAIN_DIR="../OUTPUTS/data/2018/LHC18r/"
SIZE_THRESHOLD=2  # in KB
for f in `find $MAIN_DIR -name "files_to_be_merged_*.xml" | grep -v "_part"`; do
    echo
    echo $f

    # skip already done sets of params
    year=`echo $f | cut -d "/" -f 4`
    period=`echo $f | cut -d "/" -f 5`
    run=`echo $f | cut -d "/" -f 6 | cut -c 4-`
    time_int=`echo $f | cut -d "/" -f 8 | cut -d "." -f1 | cut -d "_" -f5`
    params="$year $period $run $time_int"
    echo $params
    is_done=$(grep "$params" ../already_done.txt | grep -v "part")
    if [[ $is_done != "" ]] ; then
        echo "job with such params is already done - doing nothing"
        continue
    fi

    # skip files with size < threshold
    file_size_kb=`du -k "$f" | cut -f1`
    if (( file_size_kb < $SIZE_THRESHOLD )); then
        echo "file is smaller then threshold ($SIZE_THRESHOLD) : $file_size_kb  -- skip"
        continue
    fi

    # split file into two with equal size
    n_lines=`wc -l $f | cut -d " " -f1`
    n_root_files=$(( ($n_lines-4)/3  ))
    if [[ $(( $n_root_files/2*2 )) == $n_root_files ]]; then
        echo "n_root_files is even"
        n_first=$(( $n_root_files/2 ))
        n_second=$(( $n_root_files/2 ))
    else
        echo "n_root_files is odd"
        n_first=$(( $n_root_files/2+1 ))
        n_second=$(( $n_root_files/2 ))
    fi

    new_fname_trunk=$(echo $f | sed 's/.xml//g')

    first_fname="${new_fname_trunk}_part1.xml"
    n_lines_cp=$(( $n_first*3 ))
    echo "$first_fname :: $n_lines_cp"
    head -2 $f                                          > $first_fname
    head -$(( 2+$n_lines_cp )) $f | tail -$n_lines_cp  >> $first_fname
    tail -3 $f                                         >> $first_fname

    second_fname="${new_fname_trunk}_part2.xml"
    n_lines_cp=$(( $n_second*3 ))
    echo "$second_fname :: $n_lines_cp"
    head -2 $f                                          > $second_fname
    tail -$(( 3+$n_lines_cp )) $f | head -$n_lines_cp  >> $second_fname
    tail -3 $f                                         >> $second_fname

done
