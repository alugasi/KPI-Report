import os

######################################################################################
#
# This script contains different utils functions
#
######################################################################################

def assign_anisble_fields(results_dict:dict):
    """
    Assign the keys values pairs of the extracted ansible fields to the results dict.\n
    params:\n
        -results_dict(dict)= -test metrics dict\n
    returns: python dict
    """
    results_dict["os_architecture"] = os.environ.get("OS_ARCHITECTURE")
    results_dict["os_family"] = os.environ.get("OS_FAMILY")
    results_dict["os_distro_major_version"] = os.environ.get("OS_DISTRO_MAJOR_VERSION")
    results_dict["os_distro_version"] = os.environ.get("OS_DISTRO_VERSION")
    results_dict["os_distro_release"] = os.environ.get("OS_DISTRO_RELEASE")
    results_dict["python_version"] = os.environ.get("PYTHON_VERSION")
    results_dict["selinux_status"] = os.environ.get("SELINUX_STATUS")
    return results_dict



