#include json and os librareries
import json
import os
import sys
import time


############################################################################
#
# Build RFC/PTP json object from the extracted metrics that are passed to the script 
# as environment variables by this bash script(extractResultsFromNetwork.sh)
# The json object is then wirtten to json file which can be send to splunk.
#
############################################################################

#check if RFC/PTP
if len(sys.argv) > 1 and sys.argv[1].lower() == "true":
    is_ptp = True
else:
    is_ptp = False

if not is_ptp:
    #json object
    json_object =\
    {
        "OCP_Main_Version":float(os.environ["main_version_RFC"]),\
        "OCP_Minor_Version":os.environ["minor_version_RFC"],\
        "TYPE":"RFC2544",\
        "Node_Name":os.environ["cluster_RFC"],\
        "Histogram":os.environ["hist_RFC"],\
        "Kernel":os.environ["kernel_RFC"],\
        "Duration":float(os.environ["duration_RFC"]),\
        "Nic":os.environ["nic_RFC"],\
        "Frame_Size":int(float(os.environ["framesize_RFC"])),\
        "Throughput":float(os.environ["throuput_RFC"]),\
        "Min_Delay":float(os.environ["min_RFC"]),\
        "Max_Delay":float(os.environ["max_RFC"]),\
        "Avg_Delay":float(os.environ["avg_RFC"])
    }
    json_file_path = "RFC2544/RFC2544-"
else :
    #json object
    json_object =\
    {
        "OCP_Main_Version":float(os.environ["main_version_PTP"]),\
        "OCP_Minor_Version":os.environ["minor_version_PTP"],\
        "TYPE":"PTP",\
        "Node_Name":os.environ["cluster_PTP"],\
        "Config":os.environ["config_PTP"],\
        "Kernel":os.environ["kernel_PTP"],\
        "Duration":float(os.environ["duration_PTP"]),\
        "Nic":os.environ["nic_PTP"],\
        "Ptp4l_Avg_Offset":float(os.environ["ptp4l_avg_offset_PTP"]),\
        "Ptp4l_Max_Offset":int(os.environ["ptp4l_max_offset_PTP"]),\
        "Ptp4l_Min_Offset":int(os.environ["ptp4l_min_offset_PTP"]),\
        "Phc2sys_Avg_Offset":float(os.environ["phc2sys_avg_offset_PTP"]),\
        "Phc2sys_Max_Offset":int(os.environ["phc2sys_max_offset_PTP"]),\
        "Phc2sys_Min_Offset":int(os.environ["phc2sys_min_offset_PTP"])
    }
    json_file_path = "PTP/PTP-"


# open a file and write the JSON data to it
#add uniuqe id to file name (using unix time)
timestamp = str(time.time()).replace('.', '')

with open(json_file_path+timestamp+".json", "w") as json_file:
    json.dump(json_object, json_file)