# script making a file containing parameter sets for which jobs were already submitted
# mind the order - e.g. "waiting then started" may omit job which has status started and then waiting
for job_status in INSERTING STARTED ASSIGNED WAITING RUNNING DONE; do  
    echo
    echo "checking job_status=$job_status"
    echo
    for i in `seq 20`; do
        job_list=$(alien_ps -b -l 10000 -f $job_status | cut -d " " -f5)
        status_get_list=$?
        if [[ $status_get_list == 0  ]]; then
            break
        fi
        sleep 0.$i
    done
    for pid in $job_list ; do
        echo
        echo $pid
        for i in `seq 20`; do
            #echo "trial $i"
            comm=$(alien_ps -jdl $pid | grep "comm") 
            status_get_comm=$?
            if [[ $status_get_comm == 0  ]]; then
                #echo "status=$status_get_comm  - breaking!!!"
                break
            fi
            sleep 0.$i
        done
        
        comm_part=$(echo $comm | grep part)
        if [[ $comm_part != ""  ]]; then
            echo "'part' inside comment -- skip"
            continue
        fi
        
        echo $comm
        time_int=$(echo $comm | cut -d " " -f 7)
        period=$(echo $comm | cut -d " " -f 10 | cut -d "/" -f1)
        run=$(echo $comm | cut -d " " -f 10 | cut -d "/" -f2 | cut -c 1-6 )
        year="2018" 
        params="$year $period $run $time_int"
        echo "$pid: $params" >> already_submitted.txt
    done
done
