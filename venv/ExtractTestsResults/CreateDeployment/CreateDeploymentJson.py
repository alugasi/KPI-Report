#include json and os librareries
import json
import os
import time
import sys

# add the parent directory to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Utils/')))
from Utils import *


######################################################################################
#
# Build deployment json object from the extracted metrics that are passed to the script 
# as environment variables by this bash script(extractResultsFromDeployment.sh)
# The json object is then wirtten to json file which can be send to splunk.
#
######################################################################################

#GLOBAL PARAMS:
JSON_DIR="JsonTestsFolders/Deployments/deployment-"

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
    results_dict["test_type"] = "deployment"
    results_dict["node_name"] = os.environ.get("node_name")
    results_dict["operator_source"] = os.environ.get("operator_source")

    return results_dict


def extract_metrics(results_dict:dict):
    """
    Read the deployment stages metrics metrics and write them to a the result dict that\n
    will be used to create the test's results json file.\n
    params:\n
        -results_dict(dict)-test metrics dict\n
    returns: python dict
    """
    stages_list = []
    total_minutes = 0
    for stage in ["deploy_sno_du_node", "wait_for_du_profile"]:
        time_str = os.environ.get(stage)
        time = int(time_str) if time_str else None
        if time:
            total_minutes+=time
        stages_list.append({"stage_name":stage , "time":time})

    results_dict["stages"] = stages_list
    results_dict["total_minutes"] = total_minutes/60
    results_dict["reboot_count"] = int(os.environ.get("reboot_count")) if os.environ.get("reboot_count") else None

    return results_dict


############################################################################
#                                                                          #
#                    #################################                     #
#                    #         Driver code           #                     #
#                    #################################                     #
#                                                                          #
############################################################################

#read global params
results_dict = extract_global_params(results_dict={})
#read test metrics
results_dict = extract_metrics(results_dict=results_dict)
#extract ansible fields values
results_dict = assign_anisble_fields(results_dict=results_dict)

#create json object
#add uniuqe id to file name (using unix time)
timestamp = str(time.time()).replace('.', '')

# open a file and write the JSON data to it
with open(JSON_DIR+timestamp+".json", "w") as json_file:
    json.dump(results_dict, json_file)