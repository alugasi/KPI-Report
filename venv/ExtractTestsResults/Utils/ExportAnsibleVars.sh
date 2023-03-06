#!/bin/bash

######################################################################################################################################################
#
# This script export the following fields:
#    -OS_ARCHITECTURE
#    -OS_FAMILY
#    -OS_DISTRO_MAJOR_VERSION
#    -OS_DISTRO_VERSION
#    -OS_DISTRO_RELEASE
#    -OS_KERNEL_VERSION
#    -PYTHON_VERSION
#    -SELINUX_STATUS
#
# The fields were extracted by Peri's ansible playbook. It is crucial to call the requested extract results scripts from the jenkins logs
# after calling Peri's ansible playbook(dont appear in this repo at this moment).
#
######################################################################################################################################################
function export_ansible_vars(){

    export OS_ARCHITECTURE
    export OS_FAMILY
    export OS_DISTRO_MAJOR_VERSION
    export OS_DISTRO_VERSION
    export OS_DISTRO_RELEASE
    export OS_KERNEL_VERSION
    export PYTHON_VERSION
    export SELINUX_STATUS
}