#!/usr/bin/env bash

# # # # #
# copies set number of random QAresults.root files from grid to local
# # # # #
#
# copying, in alien shell: 
# > cp /alice/data/2018/LHC18e/000286454/pass1/18000286454027.904/QA_archive.zip file:data/QAresults_18000286454027.904.root
#

time {
for RUN_ID in 286454 ; do
    #CHUNK_A_START=19
    #CHUNK_A_STOP=39
    #for CHUNK_A in $(seq $CHUNK_A_STAR $CHUNK_A_STOP); do
    for CHUNK_A in {19..39}; do  # there is no `seq` in aliensh
        echo

        # make array of all chunks B for certain chunk A
        FILES_LIST=$(ls /alice/data/2018/LHC18e/000$RUN_ID/pass1/ | grep "${RUN_ID}0${CHUNK_A}" | cut -d "." -f 2)
        readarray -t FILES_ARR <<<"$FILES_LIST"
        ARR_SIZE=${#FILES_ARR[@]}
        echo "array size for chunkA=$CHUNK_A = $ARR_SIZE"

        # randomly choose a couple of chunks B for each chunk A
        for i in {1..20}; do  # PUT NUMBER OF FILES HERE
                              # there is no seq in aliensh and {X..Y} syntax doesn't work with variables
            RNDM=$(($RANDOM % ARR_SIZE + 1))
            #echo $RNDM
            CHUNK_B=${FILES_ARR[$RNDM]}
            CHUNK_ID="18000${RUN_ID}0${CHUNK_A}.${CHUNK_B}"
            #echo $CHUNK_ID
            echo copying /alice/data/2018/LHC18e/000${RUN_ID}/pass1/${CHUNK_ID}/QA_archive.zip file:data/QAarchive_${CHUNK_ID}.zip
            #cp /alice/data/2018/LHC18e/000${RUN_ID}/pass1/${CHUNK_ID}/QA_archive.zip file:data/QAarchive_${CHUNK_ID}.zip
        done
    done
done
}
