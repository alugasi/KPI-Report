#include json and os librareries
import json
import os
import time
import sys

# add the parent directory to the system path
sys.path.append("..")
from Utils.Utils import *



############################################################################
#
# Build cpu util json object from the extracted metrics that are passed to the script 
# as environment variables by this bash script(extractResultsFromCPUUtil.sh)
# The json object is then wirtten to json file which can be send to splunk.
#
############################################################################


#GLOBAL PARAMS:
SCENARIOS_LIST = ["idle", "workloadlaunch", "mustgather", "promquery", "steadyworkload"]
JSON_DIR = "../JsonTestsFolders/cpuUtil/cpu_util-"


############################################################################
#                                                                          #
#                    #################################                     #
#                    #      Helper functions         #                     #
#                    #################################                     #
#                                                                          #
############################################################################


def extract_global_params(results_dict:dict):
    """
    Read the global params env variables and write them to a the result dict that\n
    will be used to create the test's results json file.\n
    params:\n
        -results_dict(dict)-test metrics dict\n
    returns: python dict
    """

    results_dict["ocp_version"] = os.environ.get("ocp_version")
    results_dict["ocp_build"] = os.environ.get("ocp_build")
    results_dict["cpu"] = os.environ.get("cpu")
    results_dict["test_type"] = "cpu_util"
    results_dict["node_name"] = os.environ.get("cluster")
    results_dict["kernel"] = os.environ.get("kernel")

    #'sideloaded' env variable is the kernel_real_time value when it equall true it means that sideloaded is false
    results_dict["sideloaded"] = None if not os.environ.get("sideloaded") else "false" if os.environ.get("sideloaded")=="true" else "true"

    return results_dict


def extract_scenarios_by_types_metrics(results_dict:dict):
    """
    Read the scenarios metrics by types and write them to a the result dict that\n
    will be used to create the test's results json file.\n
    params:\n
        -results_dict(dict)-test metrics dict\n
    returns: python dict
    """
    scenarios_list = []
    for scenario in SCENARIOS_LIST:
        #array_str = os.environ.get(scenario)
        array_str=os.environ.get(scenario)
        scenario_dict = array_str.split(" ")
        scenario_record = {}
        scenario_record["scenario_name"] = scenario
        types_list = []

        for type_cpu in scenario_dict:
            splited_type_cpu = type_cpu.split(":")
            types_list.append({"type_name": splited_type_cpu[0], "max_cpu": float(splited_type_cpu[1])})

        scenario_record["types"] = types_list
        # get components metrics for steady workload
        if scenario == "steadyworkload":
            scenario_record = extract_components(steady_workload_dict=scenario_record)
        scenarios_list.append(scenario_record)

    results_dict["scenarios"] = scenarios_list

    return results_dict


def extract_os_daemon_components_metrics(steady_workload_dict:dict, acum_sum:float):
    """
    Read the os daemon components metrics and write them to a the steady_workload_dict that\n
    will be used to create the test's results json file.\n
    params:\n
        -steady_workload_dict(dict)-test steady workload metrics dict\n
        -acum_sum(float)-acumulate sum of the cpu, used for calculate total avg steadyworkload cpu
    returns: python dict, float
    """
    os_daemon_list = []
    os_services = os.environ.get("os_daemon").split(" ")
    for service in os_services:
        if service:
            service_parsed = service.split(":")
            metric = float(service_parsed[1])
            os_daemon_list.append({"group_name":service_parsed[0], "avg_cpu":metric})
            acum_sum+=metric

    steady_workload_dict["components_os_daemon"] = os_daemon_list

    return steady_workload_dict, acum_sum


def  extract_infra_pods_components_metrics(steady_workload_dict:dict, acum_sum:float):
    """
    Read the infra pods components metrics and write them to a the steady_workload_dict that\n
    will be used to create the test's results json file.\n
    params:\n
        -steady_workload_dict(dict)-test steady workload metrics dict\n
        -acum_sum(float)-acumulate sum of the cpu, used for calculate total avg steadyworkload cpu
    returns: python dict, float
    """
    infra_pods_list = []
    infra_pods = os.environ.get("infra_pods").split(" ")
    for component in infra_pods:
        if component:
            component_parsed = component.split(":")
            metric = float(component_parsed[2])
            infra_pods_list.append({"namespace":component_parsed[0], "pod":component_parsed[1], "avg_cpu":metric})
            acum_sum+=metric

    steady_workload_dict["components_infra_pods"] = infra_pods_list

    return steady_workload_dict, acum_sum


def extract_components(steady_workload_dict:dict):
    """
    Read the components metrics and write them to a the steady_workload_dict that\n
    will be used to create the test's results json file.\n
    It also calculate the avg steadyworkload\n
    params:\n
        -steady_workload_dict(dict)-test steady workload metrics dict\n
    returns: python dict 
    """
    #extract os daemon servieces metrics
    steady_workload_dict, acum_sum = extract_os_daemon_components_metrics(steady_workload_dict=steady_workload_dict, acum_sum=0.0)
    #extract infra pod metrics
    steady_workload_dict, acum_sum = extract_infra_pods_components_metrics(steady_workload_dict=steady_workload_dict, acum_sum=acum_sum)
    steady_workload_dict["avg_cpu_total"] = acum_sum
    steady_workload_dict["duration"] = os.environ.get("duration").replace("\"", "") if os.environ.get("duration") else None

    return steady_workload_dict



############################################################################
#                                                                          #
#                    #################################                     #
#                    #         Driver code           #                     #
#                    #################################                     #
#                                                                          #
############################################################################

#extract global params
results_dict = extract_global_params(results_dict={})
#extract scenarios metrics
results_dict = extract_scenarios_by_types_metrics(results_dict=results_dict)
#extract ansible fields values
results_dict = assign_anisble_fields(results_dict=results_dict)

#create json object
#add uniuqe id to file name (using unix time)
timestamp = str(time.time()).replace('.', '')

# open a file and write the JSON data to it
with open(JSON_DIR+timestamp+".json", "w") as json_file:
    json.dump(results_dict, json_file)