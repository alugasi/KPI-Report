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


def validate_field_exist(field:str):
    """
    validate that a field is not none,\n
    in case it is. return True else False\n
    params:\n
        -field(str)= the field we want to validate, usually was read from an evnironment variable from the calling script.\n
    returns: bool indicator.
    """
    return True if field else False


def assign_none_for_missing(results_dict:dict, field_name:str):
    """
    In case the field is missing it assign a None value for it in the results dict\n
    params:\n
        -results_dict(dict)-test metrics dict\n
        -field_name(str)-the missing field key in the dict.\n
    returns: python dict.
    """
    results_dict[field_name]=None
    return results_dict

