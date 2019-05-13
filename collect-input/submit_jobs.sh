# # #       PARAMETERS:             # # #       # # #       # # #
#                                                               #
#  -required:                                                   #
MAIN_DIR=${1}                                                   # e.g. "OUTPUTS/data/2018/LHC18q/"
SYSTEM=${2}                                                     # e.g. "pp" or "PbPb"
#  -optional:                                                   #
TTL=${3:-43200}                                                 # in seconds
LOG_FILE=${4:-"$HOME/service-task/collect-input/LOGS/submit_jobs_$(date "+%m-%d_%H-%M").log"}
#                                                               #
# # #       # # #       # # #       # # #       # # #       # # #
echo "running with following params:
      MAIN_DIR=$MAIN_DIR,
      SYSTEM=$SYSTEM,
      TTL=$TTL,
      LOG_FILE=$LOG_FILE"


for f in `find $MAIN_DIR -name "files_to_be_merged_*.xml" | grep -v "_part"`; do
    echo 2>&1 | tee -a $LOG_FILE
    echo $f 2>&1 | tee -a $LOG_FILE
    params_all=$(bash path2params.sh $f)
    year=$(echo $params_all | cut -d " " -f1)
    period=$(echo $params_all | cut -d " " -f2)
    run=$(echo $params_all | cut -d " " -f3)
    time_int=$(echo $params_all | cut -d " " -f5)
    params="$year $period $run $time_int"
    cmd="alien_submit mergeJDL $year $period $run $time_int $SYSTEM $TTL"

    is_submitted=$(grep "$params" already_submitted.txt | grep -v "part")
    is_done=$(grep "$params" already_done.txt | grep -v "part")
    if [[ $is_submitted  != "" ]]; then
        echo "job with such params is already submitted - doing nothing" 2>&1 | tee -a $LOG_FILE
    elif
       [[ $is_done != "" ]] ; then
        echo "job with such params is already done - doing nothing" 2>&1 | tee -a $LOG_FILE
    else
        echo $cmd 2>&1 | tee -a $LOG_FILE
        eval $cmd 2>&1 | tee -a $LOG_FILE
    fi
done
