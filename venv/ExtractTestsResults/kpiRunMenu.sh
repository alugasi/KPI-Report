#!/bin/bash

##############################################################################################
# menu for running test results extraction and storing them as json files automation script. #
##############################################################################################

PATH_TO_JSON_FOLDERS=$(pwd)

function menu() {
   options=("PTP" "RFC" "CYCLICTEST" "OSLAT" "CPU UTIL" "REBOOT" "DEPLYOMENT" "QUIT")

    while true; do
    # Display the menu and prompt the user for input
        select option in "${options[@]}"
        do
            case $option in
            "PTP")
                echo "You selected PTP"
                read -p "enter PTP test output path: " path
                read -p "enter PTP test Kernel: " kernel
                read -p "enter PTP test config: " config_PTP
                source ./extractResultsFromNetwork.sh 0 $path $kernel "$config_PTP"
                break
                ;;
            "RFC")
                echo "You selected RFC"
                read -p "enter RFC test output path: " path
                read -p "enter RFC test Kernel: " kernel
                read -p "enter RFC test nic: " nic_RFC
                source ./extractResultsFromNetwork.sh 1 $path $kernel $nic_RFC
                break
                ;;
            "CYCLICTEST")
                echo "You selected CYCLICTEST"
                read -p "enter CYCLICTEST output path: " path
                read -p "enter CYCLICTEST operator version: " operator_version
                source ./extractResultsFromAvailability.sh 1 $path $operator_version
                break
                ;;
            "OSLAT")
                echo "You selected OSLAT"
                read -p "enter OSLAT test output path: " path
                read -p "enter OSLAT test operator version: " operator_version
                source ./extractResultsFromAvailability.sh 0 $path $operator_version
                break
                ;;
            "CPU UTIL")
                echo "You selected CPU UTIL"
                read -p "enter CPU UTIL test output path: " path
                source ./extractResultsFromCPUUtil.sh $path
                break
                ;;
            "REBOOT")
                echo "You selected REBOOT"
                read -p "enter REBOOT test output path: " path
                read -p "enter REBOOT test operator version: " operator_version
                source ./extractResultsFromReboot.sh $path $operator_version
                break
                ;;
            "DEPLYOMENT")
                echo "You selected DEPLYOMENT"
                read -p "enter DEPLYOMENT test output path: " path
                source ./ExtractResultsFromDeployment.sh $path
                break
                ;;
            "QUIT")
                echo "Exiting"
                exit 0
                ;;
            *) echo "Invalid option";;
            esac
        done
    done
}

function validate_json_dir(){
    if [ ! -d "$PATH_TO_JSON_FOLDERS/cpuUtil" ]; then
        mkdir "$PATH_TO_JSON_FOLDERS/cpuUtil"
    fi
    if [ ! -d "$PATH_TO_JSON_FOLDERS/cyclicts" ]; then
        mkdir "$PATH_TO_JSON_FOLDERS/cyclicts"
    fi
    if [ ! -d "$PATH_TO_JSON_FOLDERS/Deployments" ]; then
        mkdir "$PATH_TO_JSON_FOLDERS/Deployments"
    fi
    if [ ! -d "$PATH_TO_JSON_FOLDERS/oslats" ]; then
        mkdir "$PATH_TO_JSON_FOLDERS/oslats"
    fi
    if [ ! -d "$PATH_TO_JSON_FOLDERS/reboots" ]; then
        mkdir "$PATH_TO_JSON_FOLDERS/reboots"
    fi
    if [ ! -d "$PATH_TO_JSON_FOLDERS/RFC2544" ]; then
        mkdir "$PATH_TO_JSON_FOLDERS/RFC2544"
    fi
    if [ ! -d "$PATH_TO_JSON_FOLDERS/PTP" ]; then
        mkdir "$PATH_TO_JSON_FOLDERS/PTP"
    fi
}

validate_json_dir
menu