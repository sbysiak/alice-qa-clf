RUN_DIR="data/2018/LHC18d/000286129/"

for fpath in `alien_find /alice/cern.ch/user/s/sbysiak/grid-jobs/OUTPUTS/$RUN_DIR QAresults.root | grep QAres`; do 
    echo $fpath
    rel_path=$(echo $fpath | sed 's/OUTPUTS\// /' | cut -d " " -f 2)
    echo $rel_path
    rel_dir=$(dirname $rel_path)
    source_file="/alice/cern.ch/user/s/sbysiak/grid-jobs/OUTPUTS/$rel_path"
    target_dir="/home/alidock/service-task/collect-input/OUTPUTS/$rel_dir"
    target_file="$target_path/QAresults.root"
    mkdir_cmd="mkdir -p $target_dir"
    rm_cmd="rm $target_file"
    copy_cmd="alien_cp alien:///$source_file file:$target_dir"

    if [[ -e $target_file  ]]; then
        file_size_kb=`du -k "$target_file" | cut -f1` 
        if (( file_size_kb > 100 )); then
            echo "already exists and size ok ($file_size_kb KB) -- nothing to do"
        else
            echo "already exists but size is: $file_size_kb KB -- removing and downloading again ..."
            echo $rm_cmd
            #eval $rm_cmd
            echo $copy_cmd
            #eval $copy_cmd
        fi
    else
        echo "no such file -- copying ..."
        echo $mkdir_cmd
        #eval $mkdir_cmd
        echo $copy_cmd
        #eval $copy_cmd
    fi
done