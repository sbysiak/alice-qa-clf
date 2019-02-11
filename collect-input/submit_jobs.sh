MAIN_DIR="OUTPUTS/data/2018/LHC18d/"
for f in `find $MAIN_DIR -name "files_to_be_merged_*.xml"`; do 
    year=`echo $f | cut -d "/" -f 3`
    period=`echo $f | cut -d "/" -f 4`
    run=`echo $f | cut -d "/" -f 5 | cut -c 4-`
    time_int=`echo $f | cut -d "/" -f 7 | cut -d "." -f 1 | cut -d "_" -f 5`
    cmd="alien_submit mergeJDL $year $period $run $time_int"
    echo $cmd
    eval $cmd
done
