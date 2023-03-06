#include json and os librareries
import json
import os
import sys
import time
from Utils import *


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

    frame_size = int(float(os.environ.get("framesize_RFC"))) if os.environ.get("framesize_RFC") else None
    throughput = float(os.environ.get("throuput_RFC")) if os.environ.get("throuput_RFC") else None
    min_delay = float(os.environ.get("min_RFC") ) if os.environ.get("min_RFC") else None
    max_delay = float(os.environ.get("max_RFC")) if os.environ.get("max_RFC") else None
    avg_delay = float(os.environ.get("avg_RFC")) if os.environ.get("avg_RFC") else None
    #json object
    results_dict =\
    {
        "ocp_version":os.environ.get("ocp_version_RFC"),\
        "ocp_build":os.environ.get("ocp_build_RFC"),\
        "cpu":os.environ.get("cpu_PTP"),\
        "test_type":"rfc2544",\
        "node_name":os.environ.get("cluster_RFC"),\
        "histogram":os.environ.get("hist_RFC"),\
        "kernel":os.environ.get("kernel_RFC"),\
        "duration":os.environ.get("duration_RFC"),\
        "nic":os.environ.get("nic_RFC"),\
        "frame_size":frame_size,\
        "throughput":throughput,\
        "min_delay":min_delay,\
        "max_delay":max_delay,\
        "avg_delay":avg_delay
    }
    json_file_path = "RFC2544/rfc2544-"
else :
    ptp4l_avg_offset = float(os.environ.get("ptp4l_avg_offset_PTP")) if os.environ.get("ptp4l_avg_offset_PTP") else None
    ptp4l_max_offset = float(os.environ.get("ptp4l_max_offset_PTP")) if os.environ.get("ptp4l_max_offset_PTP") else None
    ptp4l_min_offset = float(os.environ.get("ptp4l_min_offset_PTP")) if os.environ.get("ptp4l_min_offset_PTP") else None
    phc2sys_avg_offset = float(os.environ.get("phc2sys_avg_offset_PTP")) if os.environ.get("phc2sys_avg_offset_PTP") else None
    phc2sys_max_offset = float(os.environ.get("phc2sys_max_offset_PTP")) if os.environ.get("phc2sys_max_offset_PTP") else None
    phc2sys_min_offset = float(os.environ.get("phc2sys_min_offset_PTP")) if os.environ.get("phc2sys_min_offset_PTP") else None
    #json object
    results_dict =\
    {
        "ocp_version":os.environ.get("ocp_version_PTP"),\
        "ocp_build":os.environ.get("ocp_build_PTP"),\
        "cpu":os.environ.get("cpu_PTP"),\
        "test_type":"ptp",\
        "node_name":os.environ.get("cluster_PTP"),\
        "config":os.environ.get("config_PTP"),\
        "kernel":os.environ.get("kernel_PTP"),\
        "duration":os.environ.get("duration_PTP"),\
        "nic":os.environ.get("nic_PTP"),\
        "ptp4l_avg_offset":ptp4l_avg_offset,\
        "ptp4l_max_offset":ptp4l_max_offset,\
        "ptp4l_min_offset":ptp4l_min_offset,\
        "phc2sys_avg_offset":phc2sys_avg_offset,\
        "phc2sys_max_offset":phc2sys_max_offset,\
        "phc2sys_min_offset":phc2sys_min_offset
    }
    json_file_path = "PTP/ptp-"

#extract ansible fields values
results_dict = assign_anisble_fields(results_dict=results_dict)

# open a file and write the JSON data to it
#add uniuqe id to file name (using unix time)
timestamp = str(time.time()).replace('.', '')

with open(json_file_path+timestamp+".json", "w") as json_file:
    json.dump(results_dict, json_file)