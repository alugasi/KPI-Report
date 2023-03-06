#include json and os librareries
import json
import os
import time
import sys

# add the parent directory to the system path
sys.path.append("..")
from Utils.Utils import *



######################################################################################
#
# Build reboot json objects from the extracted metrics that are passed to the script 
# as environment variables by this bash script(extractResultsFromReboot.sh)
# The json object is then wirtten to json file which can be send to splunk.
#
######################################################################################


#GLOBAL PARAMS:
SOFT_REBOOT_STAGES = ["soft_node_reachable", "soft_cluster_reachable", "soft_workload_recover", "soft_cluster_recover", "soft_total"]
POWER_CYCLE_STAGES = ["power_cycle_node_reachable", "power_cycle_cluster_reachable", "power_cycle_workload_recover", "power_cycle_cluster_recover", "power_cycle_total"] 
JSON_DIR = "../JsonTestsFolders/reboots/reboot-"

############################################################################
#                                                                          #
#                    #################################                     #
#                    #      Helper functions         #                     #
#                    #################################                     #
#                                                                          #
############################################################################


def extract_global_params(results_dict:dict, reboot_type:str):
    """
    Read the global params env variables and write them to a the result dict that\n
    will be used to create the test's results json file.\n
    params:\n
        -results_dict(dict)-test metrics dict\n
        -reboot_type(str)-the test reboot type(power cycle/soft reboot at this moment)
    returns: python dict
    """
    results_dict["ocp_version"] = os.environ.get("ocp_version")
    results_dict["ocp_build"] = os.environ.get("ocp_build")
    results_dict["cpu"] = os.environ.get("cpu")
    results_dict["test_type"] = "reboot"
    results_dict["node_name"] = os.environ.get("node_name")
    results_dict["kernel"] = os.environ.get("kernel")
    results_dict["reboot_type"]=reboot_type
    #'sideloaded' env variable is the kernel_real_time value when it equall true it means that sideloaded is false
    results_dict["sideloaded"] = None if not os.environ.get("sideloaded") else "false" if os.environ.get("sideloaded")=="true" else "true"

    return results_dict

def extract_metrics(results_dict:dict, stages_env_names_list:list):
    """
    Read the global stages metrics and write them to a the result dict that\n
    will be used to create the test's results json file.\n
    params:\n
        -results_dict(dict)-test metrics dict\n
        -stages_list(list)-list with the names of the stages env variables\n
    returns: python dict
    """
    stages = ["node_reachable", "cluster_reachable", "workload_recover", "cluster_recover", "total_time"]
    
    at_most_iterations = os.environ.get("number_of_iters")
    at_most_iterations = int(at_most_iterations) if at_most_iterations else 0
    iterations_list = []

    for iteration in range(0, at_most_iterations):
        iteration_dict = {}
        iteration_dict["iteration"] = iteration
        for i in range(0, 5):
            stage_metrics = os.environ.get(stages_env_names_list[i])
            if stage_metrics:
                metrics_parsed = stage_metrics.split(" ")
                if iteration < len(metrics_parsed):
                    if stages[i] != "total_time":
                        iteration_dict[stages[i]] = float(metrics_parsed[iteration])
                    else:
                        iteration_dict["total_minutes"] = float(metrics_parsed[iteration])/60
            else:
                iteration_dict[stages[i]] = None
        iterations_list.append(iteration_dict)   
    
    results_dict["Iterations"] = iterations_list
    return results_dict



############################################################################
#                                                                          #
#                    #################################                     #
#                    #         Driver code           #                     #
#                    #################################                     #
#                                                                          #
############################################################################

for reboot_type, stages_list in zip(["soft_reboot","power_cycle"], [SOFT_REBOOT_STAGES, POWER_CYCLE_STAGES]):
    #extract global params
    results_dict = extract_global_params(results_dict={}, reboot_type=reboot_type)
    #extract reboot iteration metrics
    results_dict = extract_metrics(results_dict=results_dict, stages_env_names_list=stages_list)
    #extract ansible fields values
    results_dict = assign_anisble_fields(results_dict=results_dict)
    
    #create json object
    #add uniuqe id to file name (using unix time)
    timestamp = str(time.time()).replace('.', '')

    # open a file and write the JSON data to it
    with open(JSON_DIR+timestamp+".json", "w") as json_file:
        json.dump(results_dict, json_file)