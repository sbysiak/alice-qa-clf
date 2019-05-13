#!/bin/bash


printf "params passed to executable: \nP1: $1\nP2: $2\nP3: $3\n"

params=$2
detectors=$3
echo $detectors >> detectors.txt  # for validation script

export year=$(echo $params | cut -d ":" -f1)
export period=$(echo $params | cut -d ":" -f2)
export runNumber=$(echo $params | cut -d ":" -f3)
# export time_interval=$(echo $params | cut -d ":" -f4)

# export time_interval=$JDLVAR_time_interval
export ocdbStorage="raw://"
export dataType="data"
export pass="pass1"

printf "year=${year}\nperiod=${period}\nrunNumber=${runNumber}"


qa="QAresults.root"

for detector in $(echo "$detectors" | sed 's/:/ /g'); do
    printf "\n\n*** $detector ***\n\n"
    source $ALICE_PHYSICS/PWGPP/QA/detectorQAscripts/$detector.sh
    if [[ $detector == "EVS" ]]; then
        func="runLevelEventStatQA"
    else
        func="runLevelQA"
    fi
    time $func $qa
    mv trending.root trending_${detector}.root
done

# for detector in ITS TRD TOF T0 EVS; do
#     printf "\n\n*** $detector ***\n\n"
#     source $ALICE_PHYSICS/PWGPP/QA/detectorQAscripts/$detector.sh
#     if [[ $detector == "EVS" ]]; then
#         func="runLevelEventStatQA"
#     else
#         func="runLevelQA"
#     fi
#     time $func $qa
#     mv trending.root trending_${detector}.root
# done

echo
echo "list files after completing the job:"
ls
