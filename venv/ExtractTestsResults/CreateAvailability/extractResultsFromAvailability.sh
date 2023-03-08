#!/bin/bash

############################################################################
# Extract oslat/cyclict metrics and global params based on user choice
# then the extracted values send to a python script that create a json file that can be send
# to splunk.
#
# Global Params:
#   $1= oslat/cyclict indicator
#   $2= test results path
#   $3= operator version
#
############################################################################

# load function to export ansible extracted fields
source Utils/ExportAnsibleVars.sh

#Global params
IS_CYCLICT=$1
TEST_RESULTS_PATH=$2
OPERATOR_VERSION=$3



function extract_metrics() {
    #extract metrics lines:
    min_list=$(cat $TEST_RESULTS_PATH | grep "$GREP_MIN_STR")
    max_list=$(cat $TEST_RESULTS_PATH | grep "$GREP_MAX_STR")
    avg_list=$(cat $TEST_RESULTS_PATH | grep "$GREP_AVG_STR")
    availability_list=$(cat $TEST_RESULTS_PATH | grep "$GREP_AVAIL_STR")
    #seperate cores/thread metrics results by core
    #createing an array from each metric string where each element 'i' is the metric value for core 'i'
    readarray -t min_list <<< "$min_list"
    readarray -t max_list <<< "$max_list"
    readarray -t avg_list <<< "$avg_list"
    readarray -t availability_list <<< "$availability_list"

    #extract global params:
    kernel=$(echo ${min_list[0]} | grep -o 'kernel_version="[^"]*"' | cut -d'"' -f2)
    duration=$(echo ${min_list[0]} | grep -o 'duration="[^"]*"'| cut -d'=' -f2)
    cluster=$(echo ${min_list[0]} | grep -o 'cluster="[^"]*"' | cut -d'"' -f2)
    sideloaded=$(echo ${min_list[0]} | grep -o 'kernel_realtime="[^"]*"' | cut -d'"' -f2)
    ocp_build=$(echo ${min_list[0]} | grep -o 'sw_version="[^"]*"' | cut -d'"' -f2)
    cpu=$(echo ${min_list[0]} | grep -o 'cpu_type="[^"]*"' | cut -d'"' -f2)

    #extract oc main version
    ocp_version=$(echo $ocp_build | cut -d"." -f1-2)

    #extract cores/threads values lists from metrics lines arrays
    min_str=""
    max_str=""
    avg_str=""
    avail_str=""
    for i in "${!min_list[@]}"
    do
        min=$(echo ${min_list[$i]} | grep -o '} [0-9]*\ to url ' | cut -d' ' -f2)
        max=$(echo ${max_list[$i]} | grep -o '} [0-9]*\ to url ' | cut -d' ' -f2)
        avg=$(echo ${avg_list[$i]} | grep -o '} [0-9]*\.*[0-9]* to url ' | cut -d' ' -f2)
        avail=$(echo ${availability_list[$i]} | grep -o '} [0-9]*\.[0-9]* to url ' | cut -d' ' -f2)
        min_str="$min_str $min"
        max_str="$max_str $max"
        avg_str="$avg_str $avg"
        avail_str="$avail_str $avail"
    done
}

function export_metrics() {
    #export global:
    export duration
    export kernel
    export cluster
    export sideloaded
    export ocp_build
    export ocp_version
    export cpu

    #export metrics:
    export min_str
    export max_str
    export avg_str
    export avail_str

    #export ansible fields:
    export_ansible_vars
}

function handle_availability() {
    #extract metrics:
    extract_metrics
    #export metrics
    export_metrics

    #call python script
    python3 CreateAvailability/CreateAvailabilityJson.py $IS_OSLAT  $OPERATOR_VERSION 
}

if [ $IS_CYCLICT -eq 1 ]; 
then
    GREP_MIN_STR="\[INFO\] Pushing ranmetrics_cyclictest_min"
    GREP_MAX_STR="\[INFO\] Pushing ranmetrics_cyclictest_max"
    GREP_AVG_STR="\[INFO\] Pushing ranmetrics_cyclictest_avg"
    GREP_AVAIL_STR="\[INFO\] Pushing ranmetrics_cyclictest_availability"
    IS_OSLAT="False"
else
    GREP_MIN_STR="+ step '\[INFO\] Pushing ranmetrics_oslat_test_min"
    GREP_MAX_STR="+ step '\[INFO\] Pushing ranmetrics_oslat_test_max"
    GREP_AVG_STR="+ step '\[INFO\] Pushing ranmetrics_oslat_test_avg"
    GREP_AVAIL_STR="+ step '\[INFO\] Pushing ranmetrics_oslat_test_availability"
    IS_OSLAT="True"
fi

handle_availability