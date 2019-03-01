# # # #
# PARAMETERS
# # # #
# example values
# ALIEN_MAIN_DIR="/alice/data/2018/LHC18p"
ALIEN_MAIN_DIR=$1

for run in `alien_ls $ALIEN_MAIN_DIR`; do
    alien_dir="$ALIEN_MAIN_DIR/$run/pass1/"
    dir_to_create=$(echo $alien_dir | sed 's/\/alice/OUTPUTS/g')
    cmd_mkdir="mkdir -p $dir_to_create"
    cmd_ls="alien_ls $alien_dir"

    #echo $cmd_ls
    ls_output=$(eval $cmd_ls)
    status=$?
    if (( $status == 0 )); then 
        echo $cmd_mkdir
        eval $cmd_mkdir
    else
        if [[ $ls_output == *"no such file or directory"* ]]; then
            # RUN without pass1 directory inside - just skip   
            :
        fi
    fi
done
