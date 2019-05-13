# # #       PARAMETERS:          # # #           # # #               # # #
#                                                                        #
# DATA_DIR is appended to SOURCE_ / TARGET_MAIN                          #
#  -required:                                                            #
DATA_DIR=${1}                                                            # e.g. "data/2018/LHC18q/"
#  -optional:                                                            #
SOURCE_MAIN=${2:-"/alice/cern.ch/user/s/sbysiak/grid-jobs/OUTPUTS/"}     # std output of grid merging
TARGET_MAIN=${3:-"/eos/user/a/aliqat/www/qcml/"}                         # TARGET_MAIN="/eos/user/a/aliqat/www/qcml/"                        # when copying on EOS
                                                                         # TARGET_MAIN="/home/alidock/service-task/collect-input/OUTPUTS/"   # when copying locally
LOG_FILE=${4:-"$HOME/service-task/collect-input/LOGS/copy_job_ouput_$(date "+%m-%d_%H-%M").log"}
#                                                                        #
# # #            # # #           # # #           # # #               # # #

echo "running with following params:
      DATA_DIR=$DATA_DIR,
      SOURCE_MAIN=$SOURCE_MAIN,
      TARGET_MAIN=$TARGET_MAIN,
      LOG_FILE=$LOG_FILE"

FILE_SIZE_THRESHOLD=5000  # minimal size over which target file will be removed and copied again (in KB)
TIMEOUT=180               # timeout for alien_cp

cd $TARGET_MAIN  # for eos
for fpath in `alien_find /alice/cern.ch/user/s/sbysiak/grid-jobs/OUTPUTS/$DATA_DIR QAresults.root | grep QAres`; do
    echo
    echo $fpath
    rel_path=$(echo $fpath | sed 's/OUTPUTS\// /' | cut -d " " -f 2)
    #echo $rel_path
    rel_dir=$(dirname $rel_path)
    source_file="$SOURCE_MAIN/$rel_path"
    target_dir="$TARGET_MAIN/$rel_dir/"
    target_file="$target_dir/QAresults.root"
    # mkdir_cmd="mkdir -p $target_dir"
    mkdir_cmd="mkdir -p $rel_dir"
    rm_cmd="rm $target_file"  # removes from target not source!
    copy_cmd="timeout $TIMEOUT alien_cp alien:///$source_file file:$target_dir"

    if [[ -e $target_file ]]; then
        file_size_kb=`du -k "$target_file" | cut -f1`
        if (( file_size_kb > $FILE_SIZE_THRESHOLD )); then
            :
            echo "already exists and size ok ($file_size_kb KB) -- nothing to do"
        else
            echo "already exists but size is: $file_size_kb KB -- removing and downloading again ..."
            echo $rm_cmd
            eval $rm_cmd
            echo $copy_cmd
            eval $copy_cmd
        fi
    else
        echo "no such file -- copying ..."
        echo $mkdir_cmd
        eval $mkdir_cmd
        echo $copy_cmd
        eval $copy_cmd
    fi
    status=$?
    if (( $status != 0 )); then
        echo "STATUS = $status"
        echo "" >> $LOG_FILE
        echo "$copy_cmd" >> $LOG_FILE
        echo "processed with error code=$status" >> $LOG_FILE
    fi
done
