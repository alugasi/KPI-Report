#!/bin/bash

############################################################################
# Extract Deployment metrics and global params based on user choice
# then the extracted values send to a python script that create a json file that can be send
# to splunk.
#
# Global Params:
#   $1 = test results path
#
############################################################################

# load function to export ansible extracted fields
source ../Utils/ExportAnsibleVars.sh

#Global Params:
TEST_RESULTS_PATH=$1


function extract_metric_value(){
    local metric_lines=$1
    local metric_command=$2
    local metric_arr=$(echo $metric_lines | eval $metric_command | cut -d' ' -f5)
    readarray -t metric_arr <<< "$metric_arr"
    echo ${metric_arr[0]}
}

function extract_ocp_build(){
    local ocp_build=$(cat $TEST_RESULTS_PATH | grep -o 'export RAN_METRICS_SW_VERSION="[^"]*"' | cut -d'"' -f2)
    readarray -t ocp_build <<< "$ocp_build"
    echo ${ocp_build[0]}
}

function extract_node(){
    local node_name=$(cat $TEST_RESULTS_PATH | grep -o 'export RAN_METRICS_CLUSTER=".*"' | cut -d'"' -f2)
    readarray -t node_name <<< "$node_name"
    echo ${node_name[0]}
}

function extract_operator_source(){
    local operator_arr=$(cat $TEST_RESULTS_PATH | grep -o 'SPOKE_OPERATOR_IMAGES_SOURCE:.*,'| cut -d':' -f2 | cut -d',' -f1)
    readarray -t operator_arr <<< "$operator_arr"
    echo ${operator_arr[0]}
}

function extract_cpu_model(){
    local cpu_arr=$(cat $TEST_RESULTS_PATH | grep -o 'Model name:.*'| cut -d':' -f2  | cut -d '\' -f1)
    readarray -t cpu_arr <<< "$cpu_arr"
    echo ${cpu_arr[0]}
}

function extract_metrics(){
    
    #extract metrics lines
    local deploy_sno_du_node_lines=$(cat $TEST_RESULTS_PATH | grep "Posting time for DeploySnoDuNode")
    local wait_for_du_profile_lines=$(cat $TEST_RESULTS_PATH | grep "Posting time for WaitForDuProfileApply")
    local reboot_counts_lines=$(cat $TEST_RESULTS_PATH | grep "Posting time for DeploymentRebootCount")

    #extract metrics values
    deploy_sno_du_node=$(extract_metric_value "$deploy_sno_du_node_lines" "grep -o 'Posting time for DeploySnoDuNode: [0-9]*\.*[0-9]*'")
    wait_for_du_profile=$(extract_metric_value "$wait_for_du_profile_lines" "grep -o 'Posting time for WaitForDuProfileApply: [0-9]*\.*[0-9]*'")
    reboot_count=$(extract_metric_value "$reboot_counts_lines" "grep -o 'Posting time for DeploymentRebootCount: [0-9]*\.*[0-9]*'")
    
    #extract global params
    node_name=$(extract_node)
    operator_source=$(extract_operator_source)
    ocp_build=$(extract_ocp_build)
    cpu=$(extract_cpu_model)

    #extract oc version from oc build
    ocp_version=$(echo $ocp_build | cut -d"." -f1-2)
}

function export_metrics(){
    #export global params:
    export ocp_version
    export ocp_build
    export node_name
    export operator_source
    export cpu

    #export metrics:
    export deploy_sno_du_node
    export wait_for_du_profile
    export reboot_count

    #export ansible fields:
    export_ansible_vars
}

function handle_deployment(){
    #extract metrics:
    extract_metrics
    #export metrics:
    export_metrics

    #call python script
    python3 CreateDeploymentJson.py
}

handle_deployment