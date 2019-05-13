PERIOD_ARG=$1

for f in $(alien_find /alice/cern.ch/user/s/sbysiak/grid-jobs/OUTPUTS/data/2018/$PERIOD_ARG "QAresults.root" | grep QA | grep -v part); do
    echo
    echo $f
    params_all=$(bash path2params.sh $f)
    year=$(echo $params_all | cut -d " " -f1)
    period=$(echo $params_all | cut -d " " -f2)
    run=$(echo $params_all | cut -d " " -f3)
    time_int=$(echo $params_all | cut -d " " -f5)
    params="$year $period $run $time_int"
    comment="done-grid: $params"
    echo $comment
    echo $comment >> already_done.txt
done

echo "=========================================="
echo "GRID CHECKED, STARTING EOS..."
echo "=========================================="


for f in $(find $eos/data/2018/$PERIOD_ARG -name "QAresults.root" | grep QA | grep -v part); do
    echo
    echo $f
    params_all=$(bash path2params.sh $f)
    year=$(echo $params_all | cut -d " " -f1)
    period=$(echo $params_all | cut -d " " -f2)
    run=$(echo $params_all | cut -d " " -f3)
    time_int=$(echo $params_all | cut -d " " -f5)
    params="$year $period $run $time_int"
    comment="done-eos: $params"
    echo $comment
    echo $comment >> already_done.txt
done
