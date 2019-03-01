# # #       PARAMETERS:             # # #       # # #       # # #       
#                                                               #
#  -required:                                                   #
MAIN_DIR=${1}                                                   # e.g. "data/2018/LHC18q/"
#  -optional:                                                   #
TTL=${2:-43200}                                                 # in seconds
LOG_FILE=${4:-"$HOME/service-task/collect-input/                
               LOGS/submit_jobs_$(date "+%m-%d_%H-%M").log"}    #
#                                                               #
# # #       # # #       # # #       # # #       # # #       # # #       
echo "running with following params: 
      MAIN_DIR=$MAIN_DIR, 
      TTL=$TTL, 
      LOG_FILE=$LOG_FILE"


for f in `find $MAIN_DIR -name "files_to_be_merged_*.xml" | grep -v "_part"`; do 
    echo 
    echo $f
    year=`echo $f | cut -d "/" -f 3`
    period=`echo $f | cut -d "/" -f 4`
    run=`echo $f | cut -d "/" -f 5 | cut -c 4-`
    time_int=`echo $f | cut -d "_" -f3 | cut -d "/" -f1`
    params="$year $period $run $time_int"
    cmd="alien_submit mergeJDL $year $period $run $time_int $TTL"

    is_submitted=$(grep "$params" already_submitted.txt | grep -v "part")
    if [[ $is_submitted  != "" ]]; then 
        echo "job with such params is already submitted - doing nothing"
    else
        echo $cmd | tee -a $LOG_FILE
        eval $cmd | tee -a $LOG_FILE
    fi
done
