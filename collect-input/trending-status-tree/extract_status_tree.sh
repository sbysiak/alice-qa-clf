#!/bin/bash
pwd
ls

cp $ALICE_PHYSICS/PWGPP/TPC/macros/drawPerformanceTPCQAMatchTrends.C .
if [ -f "drawPerformanceTPCQAMatchTrends.C" ]; then
    echo "macro drawPerformanceTPCQAMatchTrends.C was found"
    time aliroot -b drawPerformanceTPCQAMatchTrends.C
fi
