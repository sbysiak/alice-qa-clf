# $1 = run e.g. "295581"

export RUN=$1;
for STAGE in 01 02 03; do
    time alien_find -x files_to_be_merged /alice/data/2018/LHC18r/000$RUN/pass1/18000$RUN$STAGE* QAresults.root | grep . > files_to_be_merged_${RUN}_$STAGE.xml
done

output_file="files_to_be_merged_${RUN}.xml"

head -3 files_to_be_merged_${RUN}_01.xml > $output_file
for STAGE in 01 02 03; do
    in_file="files_to_be_merged_${RUN}_$STAGE.xml"
    n_lines=$(wc -l $in_file | cut -d " " -f1)
    cat $in_file | head -$(( $n_lines-3 )) | tail -$(( $n_lines-6 )) >> $output_file
done
tail -3 files_to_be_merged_${RUN}_01.xml >> $output_file
