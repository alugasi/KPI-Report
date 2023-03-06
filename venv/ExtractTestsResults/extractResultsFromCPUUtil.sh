#!/bin/bash

############################################################################
# Extract cpu util metrics and global params based on user choice
# then the extracted values send to a python script that create a json file that can be send
# to splunk.
#
# Global Params:
#   $1= test results path
#
############################################################################

# load function to export ansible extracted fields
source ExportAnsibleVars.sh

#Global params
TEST_RESULTS_PATH=$1

GREP_OS_DAEMON_STR="Pushing ranmetrics_cpu_os_daemon_steadyworkload_avg"
GREP_INFRA_PODS_STR="Pushing ranmetrics_cpu_infra_pods_steadyworkload_avg"

function push_other_metrics() {
    local -n array_str=$1
    total_str=$(cat $TEST_RESULTS_PATH | grep "Pushing ranmetrics_cpu_total_$2_max")
    os_deamon_str=$(cat $TEST_RESULTS_PATH | grep "Pushing ranmetrics_cpu_os_daemon_$2_max")
    infra_pods_str=$(cat $TEST_RESULTS_PATH | grep "Pushing ranmetrics_cpu_infra_pods_$2_max")
    total_str=$(echo $total_str | grep -o '} [0-9]*\.[0-9]*' | cut -d' ' -f2)
    os_deamon_str=$(echo $os_deamon_str | grep -o '} [0-9]*\.[0-9]*' | cut -d' ' -f2)
    infra_pods_str=$(echo $infra_pods_str | grep -o '} [0-9]*\.[0-9]*' | cut -d' ' -f2)
    array_str="total:$total_str"
    array_str="$array_str os_daemon:$os_deamon_str"
    array_str="$array_str infra_pods:$infra_pods_str"
}

function extract_iter_metrics() {
    #components metrics:
    components_os_daemon_list=$(cat $TEST_RESULTS_PATH | grep "$GREP_OS_DAEMON_STR")
    components_infra_pods_list=$(cat $TEST_RESULTS_PATH | grep "$GREP_INFRA_PODS_STR")
    #seperate metrics results by component
    #createing an array from each metric string where each element 'i' is the metric value for core 'i'
    readarray -t components_os_daemon_list <<< "$components_os_daemon_list"
    readarray -t components_infra_pods_list <<< "$components_infra_pods_list"
    
    #other metrics:
    idle=""   
    workloadlaunch=""
    mustgather=""
    promquery=""
    steadyworkload=""

    scenario_types=("idle" "workloadlaunch" "mustgather" "promquery" "steadyworkload")
    cpu_scenarios_array=(idle workloadlaunch mustgather promquery steadyworkload)

    # Loop over the array of scenarios, extract and format the "other" metrics as strings
    for ((i=0; i<${#scenario_types[@]}; i++)); do
        scenario_type=${scenario_types[$i]}
        scenario_name=${cpu_scenarios_array[$i]}
        push_other_metrics $scenario_name "$scenario_type"
    done
    
    os_daemon=""
    infra_pods=""

    # Loop over the array of os services components, extract and format the results as string
    for ((i=0; i<${#components_os_daemon_list[@]}; i++)); do
        os_component_line=${components_os_daemon_list[$i]}
        os_component_groupname=$(echo $os_component_line | grep -o 'groupname="[^"]*"' | cut -d'"' -f2)
        os_component_cpu=$(echo $os_component_line | grep -o '} [0-9]*\.[0-9]*' | cut -d' ' -f2)
        os_daemon="$os_daemon $os_component_groupname:$os_component_cpu"
    done

    # Loop over the array of platform pod components, extract and format the results as string
    for ((i=0; i<${#components_infra_pods_list[@]}; i++)); do
        platfrom_pod_component_line=${components_infra_pods_list[$i]}
        platfrom_pod_component_namespace=$(echo $platfrom_pod_component_line | grep -o 'namespace="[^"]*"' | cut -d'"' -f2)
        platfrom_pod_component_pod=$(echo $platfrom_pod_component_line | grep -o 'pod="[^"]*"' | cut -d'"' -f2)
        platfrom_pod_component_cpu=$(echo $platfrom_pod_component_line | grep -o '} [0-9]*\.[0-9]*' | cut -d' ' -f2)
        infra_pods="$infra_pods $platfrom_pod_component_namespace:$platfrom_pod_component_pod:$platfrom_pod_component_cpu"
    done
    
    #global params:
    kernel=$(echo ${components_infra_pods_list[0]} | grep -o 'kernel_version="[^"]*"' | cut -d'"' -f2)
    duration=$(echo ${components_infra_pods_list[0]} | grep -o 'duration="[^"]*"' | cut -d'=' -f2)
    cluster=$(echo ${components_infra_pods_list[0]} | grep -o 'cluster="[^"]*"' | cut -d'"' -f2)
    sideloaded=$(echo ${components_infra_pods_list[0]} | grep -o 'kernel_realtime="[^"]*"' | cut -d'"' -f2)
    ocp_build=$(echo ${components_infra_pods_list[0]} | grep -o 'sw_version="[^"]*"' | cut -d'"' -f2)
    cpu=$(echo ${components_infra_pods_list[0]} | grep -o 'cpu_type="[^"]*"' | cut -d'"' -f2)
    #extract oc main version
    ocp_version=$(echo $ocp_build | cut -d"." -f1-2)
}

function export_iter_metrics(){
    #export global params:
    export kernel
    export duration
    export cluster
    export sideloaded
    export ocp_build
    export ocp_version
    export cpu
    
    #export metrics:
    export os_daemon
    export infra_pods
    export idle
    export workloadlaunch
    export mustgather
    export promquery
    export steadyworkload

    #export ansible fields:
    export_ansible_vars

}

function handle_cpu_util_iter(){

    #extract metrics:
    extract_iter_metrics

    #export params:
    export_iter_metrics

    #call python script
    python3 CreateCpuUtilIterJson.py
}


handle_cpu_util_iter