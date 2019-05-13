ARG=$1

year=`echo $ARG | grep -Po "(?<=\/)([0-9]{4})(?=\/)"`
period=`echo $ARG | grep -Po "LHC[0-9]{2}[a-z]"`
run=`echo $ARG | grep -Po "(?<="000")([0-9]{6})"`
pass=`echo $ARG | grep -Po "(?<=[0-9]{9}\/)(.*pass.*?)(?=\/)"`
chunkID=`echo $ARG | grep -Po "(?<=time_interval_)([0-9]{3})"`
part=`echo $ARG | grep -Po "part_[0-9]" | sed 's/_//'`
params="$year $period $run $pass $chunkID $part"
echo $params
