#!/bin/bash

echo "start of validation script"

status=0
for detector in $(cat detectors.txt | sed 's/:/ /g'); do
    trending_found=$(ls | grep "$detector")
    if [[ ! $trending_found ]]; then
        echo "VALIDATION ERROR: trending_${detector}.root not found !"
        status=1
    fi
done

echo "end of validation script"

if (( status > 0 )); then
    exit 1
fi

exit 0
