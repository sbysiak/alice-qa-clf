# # #  PARAMETERS   # #
export pass="pass1"; 
export ocdbStorage="raw://"

DATA_DIR="/home/alidock/service-task/collect-input/OUTPUTS/data/2018/LHC18d"
export dataType="data"; 
export year="2018"; 
export period="LHC18d"; 
# # # # # # # # # # # #

source TPC.sh

for f in `find $DATA_DIR -name "QAresults.root"`; do
    echo $f
    export runNumber=`echo $f | cut -d "/" -f 10 | cut -c 4-9`
    echo "run number = $runNumber"
    fdir=$(dirname $f)
    target_file="$fdir/trending.root"
    cmd_run="time runLevelQA $f"
    cmd_mv="time mv trending.root $target_file"
    cmd_rm="rm $target_file"

    if [[ -e $target_file ]]; then
        file_size_kb=$(du -k "$target_file" | cut -f1)
        if (( file_size_kb > 10 )); then
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
    
    
