#!/bin/bash

############################################################################
# menu for running test results extraction and pushing automation script.
############################################################################

function menu() {
   options=("PTP" "RFC" "CYCLICT" "OSLAT" "CPU UTIL" "Quit")

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
            "CYCLICT")
                echo "You selected CYCLICT"
                read -p "enter CYCLICT test output path: " path
                read -p "enter CYCLICT test operator version: " operator_version
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
            "Quit")
                echo "Exiting"
                exit 0
                ;;
            *) echo "Invalid option";;
            esac
        done
    done
}

menu