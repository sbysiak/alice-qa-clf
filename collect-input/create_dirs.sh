# # #        PARAMETERS:          # # #
#  -required:
YEAR=${1}                 # e.g. "2018"
PERIOD=${2}               # e.g. "LHC18r"
PASS=${3}                 # e.g. "pass2"
# # #      # # #      # # #      # # #


alien_main_dir="/alice/data/$YEAR/$PERIOD/"

for run in $(alien_ls $alien_main_dir); do
    echo $run
    alien_dir="$alien_main_dir/$run/$PASS/"
    dir_to_create=$(echo $alien_dir | sed 's/\/alice/OUTPUTS/g')
    cmd_mkdir="mkdir -p $dir_to_create"
    cmd_ls="alien_ls $alien_dir"
    
    ls_output=$(eval $cmd_ls)
    status=$?
    if (( $status == 0 )); then
        echo $cmd_mkdir
        eval $cmd_mkdir
    else
        if [[ $ls_output == *"no such file or directory"* ]]; then
            # RUN without PASS directory inside - just skip
            :
        else
            echo "Unexpected error occured: $ls_output (status: $status)"
        fi
    fi
done
