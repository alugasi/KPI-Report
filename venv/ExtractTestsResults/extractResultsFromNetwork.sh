#!/bin/bash

############################################################################
# Extract RFC2544/PTP metrics and global params based on user choice
# then the extracted values send to a python script that create a json file that can be send
# to splunk.
#
# Global Params:
#   $1= rfc/ptp indicator
#   $2= test results path
#   $3= nic for rfc or config for ptp
#
############################################################################


# load function to export ansible extracted fields
source ExportAnsibleVars.sh

#export ansible fields
export_ansible_vars

#Global params
IS_RFC=$1
TEST_RESULTS_PATH=$2
KERNEL=$OS_KERNEL_VERSION

function extract_RFC() {
    #function input
    kernel_RFC=$1
    nic_RFC=$2

    #extract RFC2544 metrics lines
    throuput_line=$(cat $TEST_RESULTS_PATH | grep "Pushing ranmetrics_rfc2544_test_throughput")
    min_line=$(cat $TEST_RESULTS_PATH | grep "Pushing ranmetrics_rfc2544_test_min")
    max_line=$(cat $TEST_RESULTS_PATH | grep "Pushing ranmetrics_rfc2544_test_max")
    avg_line=$(cat $TEST_RESULTS_PATH | grep "Pushing ranmetrics_rfc2544_test_avg")
    hist_line=$(cat $TEST_RESULTS_PATH | grep "Pushing ranmetrics_rfc2544_histograms")

    #extract global params:
    cluster_RFC=$(echo $throuput_line | grep -o 'cluster="[^"]*"' | cut -d'"' -f2)
    ocp_build_RFC=$(echo $throuput_line | grep -o 'sw_version="[^"]*"' | cut -d'"' -f2)
    duration_RFC=$(echo $throuput_line | grep -o 'duration="[^"]*"' | cut -d'"' -f2)
    framesize_RFC=$(echo $throuput_line | grep -o 'framesize="[^"]*"' | cut -d'"' -f2)
    cpu_RFC=$(echo $throuput_line | grep -o 'cpu_type="[^"]*"' | cut -d'"' -f2)
    
    #extract main version from full version
    ocp_version_RFC=$(echo $ocp_build_RFC | cut -d"." -f1-2)

    #extract RFC2544 metrics from RFC2455 metrics lines
    throuput_RFC=$(echo $throuput_line | grep -o '} [0-9]*\.[0-9]* to url ' | cut -d' ' -f2)
    min_RFC=$(echo $min_line | grep -o '} [0-9]*\.[0-9]* to url ' | cut -d' ' -f2)
    max_RFC=$(echo $max_line | grep -o '} [0-9]*\.[0-9]* to url ' | cut -d' ' -f2)
    avg_RFC=$(echo $avg_line | grep -o '} [0-9]*\.[0-9]* to url ' | cut -d' ' -f2)
    #
    #(?<=\}\s)-only matches substrings that come after '} '
    #.*?-any character repeated zero or more times.
    #(?=\s+to\s+url)- only matches substrings that end with ' to url'
    # 
    hist_RFC=$(echo $hist_line | grep -oP '(?<=\}\s).*?(?=\s+to\s+url)')
}

function export_RFC() {
    ######export variables######
    #export globals
    export cluster_RFC
    export ocp_build_RFC
    export duration_RFC
    export ocp_version_RFC
    export nic_RFC
    export kernel_RFC
    export framesize_RFC
    export cpu_RFC

    #export RFC2544 metrics
    export throuput_RFC
    export min_RFC
    export max_RFC
    export avg_RFC
    export hist_RFC

}

function handle_RFC() {
    #read test uniuqe input
    nic_RFC=$1

    #exract metrics
    extract_RFC $KERNEL $nic_RFC
    #export metrics
    export_RFC

    #call python script
    local is_PTP="False"
    python3 CreateNetworkJson.py $is_PTP
}

function extract_PTP() {  
    #function input
    kernel_PTP=$1
    config_PTP=$2

    #extract PTP metrics lines
    ptp4l_avg_offset_line=$(cat $TEST_RESULTS_PATH | grep "+ step '\[INFO\] Pushing ranmetrics_ptp4l_avg_offset")
    ptp4l_min_offset_line=$(cat $TEST_RESULTS_PATH | grep "+ step '\[INFO\] Pushing ranmetrics_ptp4l_min_offset")
    ptp4l_max_offset_line=$(cat $TEST_RESULTS_PATH | grep "+ step '\[INFO\] Pushing ranmetrics_ptp4l_max_offset")
    phc2sys_avg_offset_line=$(cat $TEST_RESULTS_PATH | grep "+ step '\[INFO\] Pushing ranmetrics_phc2sys_avg_offset")
    phc2sys_min_offset_line=$(cat $TEST_RESULTS_PATH | grep "+ step '\[INFO\] Pushing ranmetrics_phc2sys_min_offset")
    phc2sys_max_offset_line=$(cat $TEST_RESULTS_PATH | grep "+ step '\[INFO\] Pushing ranmetrics_phc2sys_max_offset")


    #extract global params:
    cluster_PTP=$(echo $ptp4l_avg_offset_line | grep -o 'cluster="[^"]*"' | cut -d'"' -f2)
    ocp_build_PTP=$(echo $ptp4l_avg_offset_line | grep -o 'sw_version="[^"]*"' | cut -d'"' -f2)
    duration_PTP=$(echo $ptp4l_avg_offset_line | grep -o 'duration="[^"]*"' | cut -d'"' -f2)
    nic_PTP=$(echo $ptp4l_avg_offset_line | grep -o 'nic1="[^"]*"' | cut -d'"' -f2)
    cpu_PTP=$(echo $ptp4l_avg_offset_line | grep -o 'cpu_type="[^"]*"' | cut -d'"' -f2)

    #extract main version from full version
    ocp_version_PTP=$(echo $ocp_build_PTP | cut -d"." -f1-2)
    #extract PTP metrics from PTP metrics lines
    ptp4l_avg_offset_PTP=$(echo $ptp4l_avg_offset_line | grep -o '} [0-9]*\.*[0-9]* to url ' | cut -d' ' -f2)
    ptp4l_max_offset_PTP=$(echo $ptp4l_max_offset_line | grep -o '} [0-9]*\.*[0-9]* to url ' | cut -d' ' -f2)
    ptp4l_min_offset_PTP=$(echo $ptp4l_min_offset_line | grep -o '} [0-9]*\.*[0-9]* to url ' | cut -d' ' -f2)
    phc2sys_avg_offset_PTP=$(echo $phc2sys_avg_offset_line | grep -o '} [0-9]*\.*[0-9]* to url ' | cut -d' ' -f2)
    phc2sys_max_offset_PTP=$(echo $phc2sys_max_offset_line | grep -o '} [0-9]*\.*[0-9]* to url ' | cut -d' ' -f2)
    phc2sys_min_offset_PTP=$(echo $phc2sys_min_offset_line | grep -o '} [0-9]*\.*[0-9]* to url ' | cut -d' ' -f2)
}

function export_PTP() {
    ######export variables######
    #export globals
    export config_PTP
    export cluster_PTP
    export ocp_build_PTP
    export duration_PTP
    export ocp_version_PTP
    export nic_PTP
    export kernel_PTP
    export cpu_PTP

    #export PTP metrics
    export ptp4l_avg_offset_PTP
    export ptp4l_max_offset_PTP
    export ptp4l_min_offset_PTP
    export phc2sys_avg_offset_PTP
    export phc2sys_max_offset_PTP
    export phc2sys_min_offset_PTP
}

function handle_PTP() {
    #read test uniuqe input
    config_PTP=$1

    #extract metrics
    extract_PTP $KERNEL "$config_PTP"
    #export metrics
    export_PTP
    
    #call python script
    local is_PTP="True"
    python3 CreateNetworkJson.py $is_PTP
}

if [ $IS_RFC -eq 1 ]; 
then
    handle_RFC $3
else
    handle_PTP "$3"
fi