#!/bin/bash

############################################################################
# Extract Reboot metrics and global params based on user choice
# then the extracted values send to a python script that create a json file that can be send
# to splunk.
#
# Global Params:
#   $1 = test results path
#   $2 = operator version
#
############################################################################

# load function to export ansible extracted fields
source ../Utils/ExportAnsibleVars.sh

#Global Params:
TEST_RESULTS_PATH=$1
OPERATOR_VERSION=$2

function extract_reboot_type_metrics(){
    

    local reboot_type_lines=$(cat $TEST_RESULTS_PATH | grep "Pushing ranmetrics_$1$2")
    
    echo $(echo $reboot_type_lines | grep -o '} [0-9]*\.*[0-9]* to url ' | cut -d' ' -f2)


}

function extract_metrics(){
    #extract iterations metrics:
    soft_node_reachable=$(extract_reboot_type_metrics "soft_reboot" "_1_node_reachable")
    power_cycle_node_reachable=$(extract_reboot_type_metrics "power_cycle" "_1_node_reachable")
    soft_cluster_reachable=$(extract_reboot_type_metrics "soft_reboot" "_2_cluster_reachable")
    power_cycle_cluster_reachable=$(extract_reboot_type_metrics "power_cycle" "_2_cluster_reachable")
    soft_workload_recover=$(extract_reboot_type_metrics "soft_reboot" "_3_workload_recover")
    power_cycle_workload_recover=$(extract_reboot_type_metrics "power_cycle" "_3_workload_recover")
    soft_cluster_recover=$(extract_reboot_type_metrics "soft_reboot" "_4_cluster_recover")
    power_cycle_cluster_recover=$(extract_reboot_type_metrics "power_cycle" "_4_cluster_recover")
    soft_total=$(extract_reboot_type_metrics "soft_reboot" "_total")
    power_cycle_total=$(extract_reboot_type_metrics "power_cycle" "_total")

    #
    #this is used as indicator to the number of possible completed iterations at most.
    #help to extract all the metrics, that apear in the Jenkins log file.
    #
    number_of_iters=$(echo $soft_node_reachable | wc -w)
    
    soft_node_reachable_lines=$(cat $TEST_RESULTS_PATH | grep "Pushing ranmetrics_soft_reboot_1_node_reachable")
    readarray -t soft_node_reachable_lines <<< "$soft_node_reachable_lines"
    #extract global params:
    kernel=$(echo ${soft_node_reachable_lines[0]} | grep -o 'kernel_version="[^"]*"' | cut -d'"' -f2)
    node_name=$(echo ${soft_node_reachable_lines[0]} | grep -o 'cluster="[^"]*"' | cut -d'"' -f2)
    sideloaded=$(echo ${soft_node_reachable_lines[0]} | grep -o 'kernel_realtime="[^"]*"' | cut -d'"' -f2)
    ocp_build=$(echo ${soft_node_reachable_lines[0]} | grep -o 'sw_version="[^"]*"' | cut -d'"' -f2)
    cpu=$(echo ${soft_node_reachable_lines[0]} | grep -o 'cpu_type="[^"]*"' | cut -d'"' -f2)
    
    #extract oc main version
    ocp_version=$(echo $ocp_build | cut -d"." -f1-2)
}

function export_metrics(){

    #export global:
    export kernel
    export node_name
    export sideloaded
    export ocp_build
    export ocp_version
    export cpu

    #export metrics:
    export soft_node_reachable
    export power_cycle_node_reachable
    export soft_cluster_reachable
    export power_cycle_cluster_reachable
    export soft_workload_recover
    export power_cycle_workload_recover
    export soft_cluster_recover
    export power_cycle_cluster_recover
    export soft_total
    export power_cycle_total

    #export ansible fields:
    export_ansible_vars

    #export indicator:
    export number_of_iters
}

function handle_reboot(){
    #extract metrics:
    extract_metrics

    #export metrics:
    export_metrics

    #call python script
    python3 CreateRebootJson.py
}

handle_reboot