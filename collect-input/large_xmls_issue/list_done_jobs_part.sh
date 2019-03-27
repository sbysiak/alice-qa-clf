PERIOD_ARG=$1

cd ..

for f in $(alien_find /alice/cern.ch/user/s/sbysiak/grid-jobs/OUTPUTS/data/2018/$PERIOD_ARG "QAresults.root" | grep QA | grep part); do
    echo
    echo $f
    year=`echo $f | cut -d "/" -f 10`
    period=`echo $f | cut -d "/" -f 11`
    run=`echo $f | cut -d "/" -f 12 | cut -c 4-`
    time_int=`echo $f | cut -d "/" -f 14 | cut -d "_" -f 3`
    part=`echo $f | cut -d "/" -f 15 | cut -d "_" -f2`
    params="$year $period $run $time_int $part"
    comment="done-grid PART: $params"
    echo $comment
    echo $comment >> already_done.txt
done

echo "=========================================="
echo "GRID CHECKED, STARTING EOS..."
echo "=========================================="


for f in $(find $eos/data/2018/$PERIOD_ARG -name "QAresults.root" | grep QA | grep  part); do
    echo
    echo $f
    year=`echo $f | cut -d "/" -f 10`
    period=`echo $f | cut -d "/" -f 11`
    run=`echo $f | cut -d "/" -f 12 | cut -c 4-`
    time_int=`echo $f | cut -d "/" -f 14 | cut -d "_" -f 3`
    part=`echo $f | cut -d "/" -f 15 | cut -d "_" -f2`
    params="$year $period $run $time_int $part"
    comment="done-eos PART: $params"
    echo $comment
    echo $comment >> already_done.txt
done
