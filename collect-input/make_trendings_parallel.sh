#!/bin/bash

# # #  PARAMETERS   # #
export files_trending=$1
export trending_size_lowlim="50"  # in KB

# export ocdbStorage="raw://"
export ocdbStorage="local:///net/archive/groups/plggaliceo2/qcml/OCDB-storage/cvmfs/alice-ocdb.cern.ch/calibration/data/2018/OCDB/"
#DATA_DIR="/net/people/plgsbysiak/service-task/eos/user/a/aliqat/www/qcml/data/2018/LHC18q"
#export dataType="data"
# # # # # # # # # # # #

source TPC.sh

echo "---------------------------"
echo "content of $files_trending":
cat $files_trending
echo "---------------------------"



IFS=$'\n'       # make newlines the only separator
set -f          # disable globbing
for f in $(cat $files_trending); do
    echo $f
    params=$(bash path2params.sh $f)
    export year=$(     echo $params | cut -d " " -f1)
    export period=$(   echo $params | cut -d " " -f2)
    export runNumber=$(echo $params | cut -d " " -f3)
    export pass=$(     echo $params | cut -d " " -f4)
    export chunkID=$(  echo $params | cut -d " " -f5)

    export outfile="trending$(date "+%H%M%N").root"
    echo "run number = $runNumber"
    echo "chunk ID = $chunkID"
    fdir=$(dirname $f)
    target_file="$fdir/trending.root"
    cmd_run="time runLevelQA $f $outfile"
    cmd_mv="mv $outfile $target_file"
    cmd_rm="rm $target_file"

    if [[ -e $target_file ]]; then
        file_size_kb=$(du -k "$target_file" | cut -f1)
        if (( file_size_kb > $trending_size_lowlim )); then
            echo "already exists and size ok ($file_size_kb KB) -- nothing to do"
        else
            echo "already exists but size is: $file_size_kb KB -- removing and running again ..."
            echo $cmd_rm
            eval $cmd_rm
            echo $cmd_run
            eval $cmd_run
            echo $cmd_mv
            eval $cmd_mv
        fi
    else
        echo "no such file -- running ..."
        echo $cmd_run
        eval $cmd_run
        echo $cmd_mv
        eval $cmd_mv
    fi
done
