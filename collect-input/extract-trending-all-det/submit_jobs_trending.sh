#
# !!!! REMOVES OUTPUTS FROM THE GRID
# !!!! AFTER RUNNING ALWAYS COPY OUTPUTS: copy_job_trending_ouput.sh
#
ARG_PERIOD=$1
ARG_DETECTOR=${2:-""}  # optional, if empty then searches for any trending_*.root (with underscore)
LOG_FILE=${3:-"$HOME/service-task/collect-input/LOGS/submit_jobs_trending_$(date "+%m-%d_%H-%M").log"}

TTL=3600
ALL_DET="ITS:TOF:T0:TRD:EVS"
FILE_SIZE_THRESHOLD=5

for f in `alien_find /alice/cern.ch/user/s/sbysiak/grid-jobs/OUTPUTS/extractTrending/data/2018/$ARG_PERIOD/ "QAresults.root" | grep -v "part" | grep QA`; do
    printf "\n$f\n"
    dir=$(dirname $f)

    params=$(bash ../path2params.sh $dir)
    echo "params = $params"
    export year=$(     echo $params | cut -d " " -f1)
    export period=$(   echo $params | cut -d " " -f2)
    export runNumber=$(echo $params | cut -d " " -f3)
    export pass=$(     echo $params | cut -d " " -f4)
    export chunkID=$(  echo $params | cut -d " " -f5)

    cmd_submit="alien_submit extractTrendingJDL $year $period $runNumber $chunkID $TTL"
    eos_path="/eos/user/a/aliqat/www/qcml/data/${year}/${period}/000${runNumber}/${pass}/time_interval_${chunkID}"
    grid_path=$(echo $eos_path | sed 's+eos/user/a/aliqat/www/qcml+alice/cern.ch/user/s/sbysiak/grid-jobs/OUTPUTS/extractTrending+') # sed can use any separator, here: "+"
    #                                            replace this    /|\    with this

    printf "EOS PATH::: $eos_path\n"

    anyOnEos=$(find $eos_path | grep "trending_"  )
    #anyOnGrid=$(alien_ls $dir | grep "trending_")

    det_to_submit=""

    #if [[ ! $anyOnEos && ! $anyOnGrid ]]; then
    if [[ ! $anyOnEos ]]; then
        printf "\t trending not found for any detector -- running for all: $ALL_DET\n"
        cmd_submit="alien_submit extractTrendingJDL $year $period $runNumber $chunkID $ALL_DET $TTL"
        echo $cmd_submit
        eval $cmd_submit
    else
        printf "\t trending found for some detector -- now checking for each  ...\n"
        for det in $(echo $ALL_DET | sed 's/:/ /g'); do
            if [[ ! $(find $eos_path | grep "trending_$det") ]]; then
                printf "\t\t trending_$det.root not found -- clearing dir on grid from files related to this detector and adding to submition\n"
                det_to_submit="$det_to_submit:$det"
                alien_rm_cmd="alien_rm $grid_path/stdout $grid_path/stderr $grid_path/trending_$det.root $grid_path/*.zip"
                printf "\t\t $alien_rm_cmd\n"
                eval $alien_rm_cmd
            else
                file_size_kb=$(du -k "$eos_path/trending_$det.root" | cut -f1)
                if (( file_size_kb < FILE_SIZE_THRESHOLD )); then
                    printf "\t\t trending_$det.root found but size=$file_size_kb is below threshold=$FILE_SIZE_THRESHOLD -- removing from eos, clearing dir on grid and adding to submition\n"
                    alien_rm_cmd="alien_rm $grid_path/stdout $grid_path/stderr $grid_path/trending_*.root $grid_path/*.zip"
                    eos_rm_cmd="rm $eos_path/trending_$det.root"
                    printf "\t\t $alien_rm_cmd\n"
                    eval $alien_rm_cmd
                    printf "\t\t $eos_rm_cmd\n"
                    eval $eos_rm_cmd

                    det_to_submit="$det_to_submit:$det"
                fi
            fi
        done
        if [[ $det_to_submit ]]; then
            det_to_submit=$(echo $det_to_submit | sed 's/://')  # remove leading ":"
            printf "\t trending not found for some detectors -- running for: $det_to_submit\n"
            cmd_submit="alien_submit extractTrendingJDL $year $period $runNumber $chunkID $det_to_submit $TTL"
            echo $cmd_submit
            eval $cmd_submit
        else
            printf "\t ... found for all -- continue\n"
        fi
    fi



    # if [[ $onEos ]]; then
    #     echo "some trending already present on EOS -- skip"
    # else
    #     onGrid=$(alien_ls $dir | grep "trending_${ARG_DETECTOR}")
    #     if [[ $onGrid ]]; then
    #         echo "some trending already present on GRID -- skip"
    #     else
    #         echo $cmd_submit
    #         # eval $cmd_submit
    #     fi
    # fi
done
