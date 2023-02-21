#include json and os librareries
import json
import os
import sys
import time



############################################################################
#
# Build OSLAT/Cyclict json object from the extracted metrics that are passed to the script 
# as environment variables by this bash script(extractResultsFromAvailability.sh)
# The json object is then wirtten to json file which can be send to splunk.
#
############################################################################

############################################################################
#                                                                          #
#                    #################################                     #
#                    #      Helper functions         #                     #
#                    #################################                     #
#                                                                          #
############################################################################


def extract_metrics_values(max_list:list, min_list:list, avg_list:list, avail_list:list):
    """
    The fucntion takes the raw metrics lists of OSLAT/Cyclict test results and return a list\n
    where the keys are the indexes of the threads/cores and the values are min, max, avg latencies and\n
    availibilities values of each one of them.\n
    params:\n
        -max_list(list)-the max latencies list of the threads/cores.\n
        -min_list(list)-the min latencies list of the threads/cores.\n
        -avg_list(list)-the avg latencies list of the threads/cores.\n
        -avail_list(list)-the availability list of the threads/cores.\n
    returns: a python list.
    """
    metrics_list = []
    thread = 0
    for max, min, avg, avail in zip(max_list, min_list, avg_list, avail_list):
        number_of_nines = calc_nines(avail=str(avail))
        metrics_list.append({"Index": thread,"Max_Latency":max, "Min_Latency":min, "Avg_Latency":avg, "Availability": avail, "Number_Of_Nines": number_of_nines})
        thread += 1
    return metrics_list



def read_lists_of_latencies():
    """
    create and return the list of latencies.\n
    returns: 3 lists of latencies, and availability list
    """
    # read lists from env variables and convert to int
    min_list = [int(x) for x in os.environ.get("min_str").split(" ") if x]
    max_list = [int(x) for x in os.environ.get("max_str").split(" ") if x]
    avg_list = [float(x) for x in os.environ.get("avg_str").split(" ") if x]
    avail_list = [float(x) for x in os.environ.get("avail_str").split(" ") if x]
    # return the lists
    return min_list, max_list, avg_list, avail_list

def calc_nines(avail:str):
    """
    Calculate and return the number of nines based on a given availability\n
    params:\n
        -avail(str)-a given core/thread availabilty as string\n
    returns: the number of nines
    """
    number_of_nines=0
    if avail.startswith("100"):
        number_of_nines=100
    else:
        for digit in avail:
            if digit == '9':
                number_of_nines+=1
            else:
                if digit != '.':
                    break
    return number_of_nines


def get_global_params(results_dict:dict):
    """
    read and return the global params of the test result:(ocp version, node name, kernel, sideloaded, duration and operator version)\n
    params:\n
        -results_dict(dict)-dict of the test results\n
    returns: the results dict
    """
    #read global params
    results_dict["OCP_Main_Version"] = os.environ.get("oc_main_version")
    results_dict["OCP_Minor_Version"] = os.environ.get("oc_minor_version")
    results_dict["Node_Name"] = os.environ.get("cluster")
    results_dict["Duration"] = float(os.environ.get("duration"))
    results_dict["Kernel"] = os.environ.get("kernel")

    #'sideloaded' env variable is the kernel_real_time value when it equall true it means that sideloaded is false
    results_dict["Side_Loaded"] = "false" if os.environ.get("sideloaded")=="true" else "true"
    #TODO:remmember to change when info will be in the test results!
    results_dict["Operator_Version"] = sys.argv[2]

    # return the results dict
    return results_dict



############################################################################
#                                                                          #
#                    #################################                     #
#                    #         Driver code           #                     #
#                    #################################                     #
#                                                                          #
############################################################################



#check if OSLAT/Cyclict
if len(sys.argv) > 1 and sys.argv[1].lower() == "true":
    is_oslat = True
    type="OSLAT"
    json_file_path="oslats/oslat-"
else:
    is_oslat = False
    type="Cyclict"
    json_file_path="cyclicts/cyclict-"

results_dict = {}
results_dict["Type"] = type

#read global params
results_dict = get_global_params(results_dict=results_dict)
#read latencies lists and convert to int lists
min_list, max_list,  avg_list, avail_list = read_lists_of_latencies()
#exract metrics values
results_dict["Test_Units"] = extract_metrics_values(max_list=max_list, min_list=min_list, avg_list=avg_list, avail_list=avail_list)

#create json object
#add uniuqe id to file name (using unix time)
timestamp = str(time.time()).replace('.', '')

# open a file and write the JSON data to it
with open(json_file_path+timestamp+".json", "w") as json_file:
    json.dump(results_dict, json_file)