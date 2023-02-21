#include json and os librareries
import json
import os
import time
import ast



############################################################################
#
# Build cpu util json object from the extracted metrics that are passed to the script 
# as environment variables by this bash script(extractResultsFromCPUUtil.sh)
# The json object is then wirtten to json file which can be send to splunk.
#
############################################################################


#GLOBAL PARAMS:
SCENARIOS_LIST = ["idle", "workloadlaunch", "mustgather", "promquery", "steadyworkload"]
JSON_DIR = "cpuUtil/cpuUtil-"


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

    results_dict["OCP_Main_Version"] = os.environ.get("oc_main_version")
    results_dict["OCP_Minor_Version"] = os.environ.get("oc_minor_version")
    results_dict["TYPE"] = "cpu util"
    results_dict["Node_Name"] = os.environ.get("cluster")
    results_dict["Duration"] = float(os.environ.get("duration"))
    results_dict["Kernel"] = os.environ.get("kernel")

    #'sideloaded' env variable is the kernel_real_time value when it equall true it means that sideloaded is false
    results_dict["Side_Loaded"] = "false" if os.environ.get("sideloaded")=="true" else "true"

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
        scenario_record["Scenario_Name"] = scenario
        types_list = []
        Max_CPU = 0

        for type_cpu in scenario_dict:
            splited_type_cpu = type_cpu.split(":")
            types_list.append({"Type_Name": splited_type_cpu[0], "CPU": float(splited_type_cpu[1])})
            Max_CPU+=float(splited_type_cpu[1])

        scenario_record["Types"] = types_list
        scenario_record["MAX_CPU"] = Max_CPU

        scenarios_list.append(scenario_record)

    results_dict["Scenarios"] = scenarios_list

    return results_dict


def extract_os_service_components_metrics(results_dict:dict, acum_sum:float):
    """
    Read the os service components metrics and write them to a the result dict that\n
    will be used to create the test's results json file.\n
    params:\n
        -results_dict(dict)-test metrics dict\n
        -acum_sum(float)-acumulate sum of the cpu, used for calculate avg steadyworkload cpu
    returns: python dict, float, int 
    """
    os_service_list = []
    os_services = os.environ.get("Os_ServiceGroup").split(" ")
    number_services = 0
    for service in os_services:
        if service:
            number_services +=1
            service_parsed = service.split(":")
            metric = float(service_parsed[1])
            os_service_list.append({"GroupName":service_parsed[0], "CPU":metric})
            acum_sum+=metric

    results_dict["Components_OsServiceGroup"] = os_service_list

    return results_dict, acum_sum, number_services


def  extract_platformpod_components_metrics(results_dict:dict, acum_sum:float):
    """
    Read the platform pod components metrics and write them to a the result dict that\n
    will be used to create the test's results json file.\n
    params:\n
        -results_dict(dict)-test metrics dict\n
        -acum_sum(float)-acumulate sum of the cpu, used for calculate avg steadyworkload cpu
    returns: python dict, float, int 
    """
    platformpod_list = []
    platformpods = os.environ.get("PlatformPod").split(" ")
    number_services = 0
    for component in platformpods:
        if component:
            number_services +=1
            component_parsed = component.split(":")
            metric = float(component_parsed[2])
            platformpod_list.append({"NameSpace":component_parsed[0], "Pod":component_parsed[1], "CPU":metric})
            acum_sum+=metric

    results_dict["Components_PlatformPod"] = platformpod_list

    return results_dict, acum_sum, number_services


def extract_components(results_dict:dict):
    """
    Read the components metrics and write them to a the result dict that\n
    will be used to create the test's results json file.\n
    It also calculate the avg steadyworkload\n
    params:\n
        -results_dict(dict)-test metrics dict\n
    returns: python dict 
    """
    #extract os servieces metrics
    results_dict, acum_sum, number__os_services = extract_os_service_components_metrics(results_dict=results_dict, acum_sum=0.0)
    #extract platform pod metrics
    results_dict, acum_sum, number__platformpod_services = extract_platformpod_components_metrics(results_dict=results_dict, acum_sum=acum_sum)
    results_dict["Steady_Avg_cpu"] = acum_sum/(number__os_services+number__platformpod_services)

    return results_dict



############################################################################
#                                                                          #
#                    #################################                     #
#                    #         Driver code           #                     #
#                    #################################                     #
#                                                                          #
############################################################################

results_dict = extract_global_params(results_dict={})
results_dict = extract_scenarios_by_types_metrics(results_dict=results_dict)
results_dict = extract_components(results_dict=results_dict)

#create json object
#add uniuqe id to file name (using unix time)
timestamp = str(time.time()).replace('.', '')

# open a file and write the JSON data to it
with open(JSON_DIR+timestamp+".json", "w") as json_file:
    json.dump(results_dict, json_file)