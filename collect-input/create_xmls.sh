# script creating xmls files using alien_find
# which is executed for each RUN

# # #       PARAMETERS:             # # #       # # #       # # #
#                                                               #
#  -required:                                                   #
START_DIR=${1}                                                  # e.g. "data/2018/LHC18q/" or "data/2018/"   !! end with slash !!
#  -optional:                                                   #
LOG_FILE=${2:-"$HOME/service-task/collect-input/
               LOGS/create_xml_$(date "+%m-%d_%H-%M").log"}     #
#                                                               #
# # #       # # #       # # #       # # #       # # #       # # #
echo "running with following params:
      START_DIR=$START_DIR,
      LOG_FILE=$LOG_FILE"

TIMEOUT=300               # timeout for alien_find
XML_SIZE_THRESHOLD=5000  # minimal size over which target file will be removed and copied again (in KB)


if [[ $START_DIR == *"LHC"* ]]; then
    # e.g. START_DIR=data/2018/LHC18e/
    RUN_CHARACTERS="3-11"
else
    # e.g. START_DIR=data/2018/
    RUN_CHARACTERS="10-18"
fi

cd "/afs/cern.ch/user/s/sbysiak/service-task/collect-input/OUTPUTS/$START_DIR"
time for RUN_TMP in `find . -name "pass1"`; do
    echo
    echo $RUN_TMP
    PERIOD_RUN=`echo $RUN_TMP | cut -c 3-`
    RUN=`echo $RUN_TMP | cut -c $RUN_CHARACTERS`

    target_file="$PERIOD_RUN/files_to_be_merged.xml"
    cmd="timeout $TIMEOUT alien_find -x files_to_be_merged /alice/$START_DIR$PERIOD_RUN/1* QAresults.root > $target_file"
    rm_cmd="rm $target_file"

    if [[ -e $target_file ]]; then
        file_size_kb=`du -k "$target_file" | cut -f1`
        if (( file_size_kb > $XML_SIZE_THRESHOLD )); then
            echo "already exists and size ok ($file_size_kb KB) -- nothing to do"
        else
            echo "already exists but size is: $file_size_kb KB -- removing and creating again ..."
            echo $rm_cmd
            eval $rm_cmd
            echo $cmd
            eval $cmd
        fi
    else
        echo "no such file -- creating ..."
        echo $cmd
        eval $cmd
    fi

    STATUS=$?
    echo "STATUS = $STATUS"
    if (( $STATUS != 0 )); then
        echo "$PERIOD_RUN processed with error code=$STATUS" >> $LOG_FILE
    fi
done
