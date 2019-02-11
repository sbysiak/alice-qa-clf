# script counting how many files with name files_to_be_merged.xml 
# located under given directory are full and how many are empty

cd "/afs/cern.ch/user/s/sbysiak/OUTPUTS/data/2018/"
for period in `ls`; do 
    echo $period
    full=0
    empty=0
    for f in $(find $period -name "files_to_be_merged.xml"); do 
        nl=`wc -l $f | cut -d " " -f 1`
        if [[ $nl > 10 ]]; then 
            full=$(( full+1 ))
        else 
            empty=$(( empty+1 ))
        fi
    done
    echo "N_full=$full N_empty=$empty fraction of full = 0.$(( $full*100/(full+empty)))"
    echo
done
