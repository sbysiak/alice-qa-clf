# Steps before jobs submission
--------

### create local directories per run (@ local)
e.g. OUTPUTS/data/2018/LHC18e/000286454/pass1/ @lxplus  
mind the leading "/"  
`bash create_dirs.sh "/alice/data/2018/$PERIOD"`

### create xmls (@lxplus)       
_duration for LHC18o: 3min_  
_be aware of [potential issue in PbPb](#largeXML)_  
`bash create_xmls.sh "data/2018/$PERIOD/"`

### split xmls (@lxplus)
_duration for LHC18o: 30min_  
`for xml in $(find OUTPUTS/data/2018/$PERIOD/ -name "files_to_be_merged.xml"); do python split_xmls.py $xml; done`

### create directories per time interval on alien <br/> AND <br/> copy xmls_per_time_interval from lxplus to alien (@lxplus)        
_LHC18o: ~2h_  

    alien_main="/alice/cern.ch/user/s/sbysiak/grid-jobs/"
    for xml in `find OUTPUTS/data/2018/$PERIOD/ -name "files_to_be_merged_*.xml"`; do
        echo $xml
        dir_to_create=$(echo $xml | sed "s/files_to_be_merged/time_interval/" | sed "s/.xml//")
        alien_mkdir $alien_main$dir_to_create
        alien_cp file:$xml alien:$alien_main$dir_to_create
    done


### submit jobs (@lxplus)
`submit_jobs.sh  "OUTPUTS/data/2018/$PERIOD" "PbPb"`

to resubmit (really submit again) failed jobs:  
first create list of jobs with status DONE or any from "in progress", e.g. RUNNING  
and then just run \`submit_jobs.sh\`  
`list_submitted_jobs.sh`  
`submit_jobs.sh "data/2018/$PERIOD"`


## Known problems
### Issue with large XMLs in PbPb
some xmls will be invalid due to `alien_find` limitations  
generating following error codes:  
* 1 - Maximum number of columns exceeded (limit of alien_find reached)  
* 124 - timeout - can be extended in create_xmls.sh  

In such cases, after \`create_xmls.sh\` check log file in order to find runs with invalid xmls. For those runs run script which executes \`alien_find\` for 3 parts and merges them in single xml  
then move it to suitable directory:  
`bash create_large_xml.sh "295589"`

split xmls into part1 and part2:  
`bash split_in_two.sh       # set MAIN_DIR`  
mkdir on alien and cp xmls there:  
`bash submit_jobs_part.sh   # with cmd = cmd_mkdir + cmd_cp`  
submit jobs:  
`bash submit_jobs_part.sh   # with cmd = cmd_submit`






# After the jobs are finished
-----------------------------

copy from grid to EOS  
`copy_jobs_output.sh "data/2018/$PERIOD/"`

### merge part_1 + part_2 in case of _large XMLs_
First `cd` to period dir on eos  
then execute:

    FILE_SIZE_THRESHOLD=1000
    time for f1 in `find . -name "QAresults.root" | grep part_1`; do
        echo
        echo $f1
        f2=`echo $f1 | sed 's/part_1/part_2/g'`;
        fmerged=`echo $f1 | sed 's/part_1\///g'`;
        if [[ ! -e $f2 ]]; then echo "$f2 does not exists -- skip"; continue; fi;
        if [[ -e  $fmerged ]]; then
            fmerged_size_kb=`du -k "$fmerged" | cut -f1`
            if (( fmerged_size_kb < FILE_SIZE_THRESHOLD )); then
                echo "merged found but has size below threshold -- removing and trying again"
                rm $fmerged
            else
                echo "$fmerged found and size is ok -- skip"
                continue
            fi
        fi;
        f1_size_kb=`du -k "$f1" | cut -f1`
        f2_size_kb=`du -k "$f2" | cut -f1`
        if (( f1_size_kb < FILE_SIZE_THRESHOLD )); then
            echo "part_1 has size = ${f1_size_kb} which is below threshold = ${FILE_SIZE_THRESHOLD} -- not merging"
            continue
        elif (( f2_size_kb < FILE_SIZE_THRESHOLD )); then
            echo "part_2 has size = ${f2_size_kb} which is below threshold = ${FILE_SIZE_THRESHOLD} -- not merging"
            continue
        else
            alihadd $fmerged $f1 $f2 > /dev/null;
            fmerged_size_kb=`du -k "$fmerged" | cut -f1`
            if (( fmerged_size_kb < FILE_SIZE_THRESHOLD )); then
                echo "merged has size below threshold (merging failed) -- removing"
                rm $fmerged
            else
                echo "merging went fine"
            fi
        fi
    done



### trends extraction (@lxplus)
copy \`QAresults.root\` to grid:  
`time bash copy_qa_to_grid.sh "data/2018/$PERIOD/"`

submit jobs and copy output  
(for TPC):  
`time bash submit_jobs_trending.sh "$PERIOD"`  
`time bash copy_job_trending_outputs.sh "data/2018/$PERIOD/"`  
OR   
(for det != TPC):    
`time bash submit_jobs_trending.sh "$PERIOD"  ["ITS:TOF:T0:TRD:EVS"]`  
`time bash copy_job_trending_outputs.sh "data/2018/$PERIOD/"`

### statusTree extraction

merge all \`trending.root\` and \`trending_EVS.root\` for given period

    qcml="/eos/user/a/aliqat/www/qcml/"
    cd $qcml/data/2018/$PERIOD
    alihadd trending_merged_$PERIOD.root $(find . -name "trending.root")
    alihadd trending_EVS_merged_$PERIOD.root $(find . -name "trending_EVS.root")

copy \`trending_merged_$PERIOD.root\` on the GRID and change its name to \`trending.root\`:
`alien_cp trending_merged_$PERIOD.root alien://alice/cern.ch/user/s/sbysiak/grid-jobs/OUTPUTS/statusTrees/data/2018/$PERIOD/input/`

extract statusTree **(@ GRID)**   
`alien_submit statusTreeJDL "2018" "$PERIOD" "60000"`

copy the result and \`trending_EVS_merged_$PERIOD.root\` to LOCAL and click through \`trending2csv_statusTreeGraphs.ipynb\`

then copy \`trending_merged_$PERIOD_withGraphs.csv\` to EOS




# ~trending extraction on PLGRID:~
~`python master_trending_jobs.py  # set params of main()`  
hadd trending and copy to eos~

~if soft for trend extraction is modified, then run:~

    # cd $ALIBUILD_WORK_DIR/BUILD/AliPhysics-latest/AliPhysics
    # cp ~/service-task/AliTPCPerformanceSummary.cxx /net/people/plgsbysiak/alice/AliPhysics/PWGPP/TPC/AliTPCPerformanceSummary.cxx
    # cp ~/service-task/AliTPCPerformanceSummary.h /net/people/plgsbysiak/alice/AliPhysics/PWGPP/TPC/AliTPCPerformanceSummary.h
    # make -j 4
    # make install -j 4
    # cp ~/.sw/slc7_x86-64/AliPhysics/master_ROOT6-1/PWGPP/TPC/macros/MakeTrend.C.modified  ~/.sw/slc7_x86-64/AliPhysics/master_ROOT6-1/PWGPP/TPC/macros/MakeTrend.C

### export trending to *.csv
`aliroot -q ".x trending2csv.C(\"trending_merged_$PERIOD.root\")"`  
`python transpose.py trending_merged_$PERIOD_transposed.csv`
