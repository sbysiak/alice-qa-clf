
export period="$1"
export n_xmls_local_before=$(    find OUTPUTS/data/2018/$period/ -name "files_to_be_merged.xml"                  | wc -l)
export n_xmls_local_after=$(     find OUTPUTS/data/2018/$period/ -name "files_to_be_merged_*.xml" | grep -v part | wc -l)
export n_xmls_local_after_part=$(find OUTPUTS/data/2018/$period/ -name "files_to_be_merged_*.xml" | grep part    | wc -l)
export n_qaresults_eos=$(        find $eos/data/2018/$period/ -name "QAresults.root"              | grep -v part | wc -l)
export n_qaresults_eos_part=$(   find $eos/data/2018/$period/ -name "QAresults.root"              | grep part    | wc -l)
export n_trending_eos=$(         find $eos/data/2018/$period/ -name "trending.root" | wc -l)

export n_xmls_grid=$(         alien_find /alice/cern.ch/user/s/sbysiak/grid-jobs/OUTPUTS/data/2018/$period/  "files_to_be_merged_*.xml" | grep -v part | grep data | wc -l )
export n_xmls_grid_part=$(    alien_find /alice/cern.ch/user/s/sbysiak/grid-jobs/OUTPUTS/data/2018/$period/  "files_to_be_merged_*.xml" | grep part    | grep data | wc -l )
export n_qaresults_grid=$(    alien_find /alice/cern.ch/user/s/sbysiak/grid-jobs/OUTPUTS/data/2018/$period/  "QAresults.root"           | grep -v part | grep data | wc -l )
export n_qaresults_grid_part=$(alien_find /alice/cern.ch/user/s/sbysiak/grid-jobs/OUTPUTS/data/2018/$period/ "QAresults.root"           | grep part    | grep data | wc -l )

#echo "For $period there are $n_qares QAresults.root on grid and , $n_xmls local xmls (split)"

export n_xmls_grid_part=$(( $n_xmls_grid_part / 2 ))
export n_xmls_local_after_part=$(( $n_xmls_local_after_part / 2 ))
export n_qaresults_grid_part=$(( $n_qaresults_grid_part / 2 ))
export n_qaresults_eos_part=$(( $n_qaresults_eos_part / 2 ))



date
echo "For $period there are:"
echo -e "\tXMLs:"
echo -e "\t\tlocal before split: $n_xmls_local_before"
echo -e "\t\tlocal after  split: $n_xmls_local_after (+ $n_xmls_local_after_part parts = $(( $n_xmls_local_after + $n_xmls_local_after_part )))"
echo -e "\t\tgrid (after split): $n_xmls_grid (+ $n_xmls_grid_part parts = $(( $n_xmls_grid + $n_xmls_grid_part )))"

echo -e "\tQAresults.root:"
echo -e "\t\tgrid: $n_qaresults_grid (+ $n_qaresults_grid_part parts = $(( $n_qaresults_grid + $n_qaresults_grid_part )))"
echo -e "\t\tEOS:  $n_qaresults_eos (+ $n_qaresults_eos_part parts = $(( $n_qaresults_eos + $n_qaresults_eos_part )))"

echo -e "\ttrending.root:"
echo -e "\t\tEOS:  $n_trending_eos"
echo
