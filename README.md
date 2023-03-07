# KPI_Splunk
Git repository for the "KPI automation scripts and splunk pushing and quries scripts.

## Overview
The repository contains scripts mainly for:<br>
    a)extracting tests results metrics and parameters, format them and create json<br> 
    files with the formatted extracted data.<br>
    b)pushing the json files to splunk instance(under this index=ecosystem-qe-dev) as new events records for later analysing and reporting.<br>
    c)queries for creating different dashboards based on the collected KPIs.<br>

## Goal
The main goal of this repo is to be served as a POC for the Splunk alternative for autamtically collacting and storing tests results and creating dashboards,
rather then menually collecting the results and store them in spreadsheets and later produce reports from them using Google data studio.


## Project structure

    ├── venv                                                       ## folder that conatin all the required files for the virtuall environment and the repo files
    │   ├──ExtractTestsResults                                     ##contains different folders with script for extracting the metrics from jenkins logs and store them in json files
    │   │   ├──CreateAvailability                                  ## folder with scripts for creating json file from oslat and cyclictest jenkins log
    │   │   │   ├──CreateAvailabilityJson.py                       ## create json file from extracted fields
    │   │   │   ├──extractResultsFromAvailability.sh               ## extract fields from jenkins log
    │   │   ├──CreateCpuUtil                                       ## folder with scripts for creating json file from cpu util jenkins log
    │   │   │   ├──CreateCpuUtilIterJson.py                        ## create json file from extracted fields
    │   │   │   ├──extractResultsFromCPUUtil.sh                    ## extract fields from jenkins log
    │   │   ├──CreateDeployment                                    ## folder with scripts for creating json file from deployment jenkins log
    │   │   │   ├──CreateDeploymentJson.py                         ## create json file from extracted fields
    │   │   │   ├──ExtractResultsFromDeployment.sh                 ## extract fields from jenkins log
    │   │   ├──CreateNetwork                                       ## folder with scripts for creating json file from rfc and ptp jenkins log
    │   │   │   ├──CreateNetworkJson.py                            ## create json file from extracted fields
    │   │   │   ├──extractResultsFromNetwork.sh                    ## extract fields from jenkins log
    │   │   ├──CreateReboot                                        ## folder with scripts for creating json file from reboot jenkins log
    │   │   │   ├──CreateRebootJson.py                             ## create json file from extracted fields
    │   │   │   ├──extractResultsFromReboot.sh                     ## extract fields from jenkins log
    │   │   ├──JenkinsLogs                                         ## folder that contains test jenkins logs samples
    │   │   ├──JsonTestsFolders                                    ## folder that contains different json files that were created from a given jenkins logs/spreadsheets
    │   │   ├──Utils                                                ## folder with different utils scripts
    │   │   │   ├──ExportAnsibleVars.sh                             ## script for exporting job parameters that were extracted via ansible playbook(still not in the repo)
    │   │   │   ├──Utils.py                                         ## utils module 
    │   │   ├──kpiRunMenu.sh                                        ## driver script for selecting the requried test metrics extraction(still not fully aotumated)
    │   ├──JsonFormatsForSplunk                                     ##  folder that contain all the corrent json formats for the tests that are pushed to splunk
    │   │   ├──AvailabilityTest.json                                ## json format for cyclictest and oslat
    │   │   ├──CpuUtilTest.json                                     ## json format for cpu util test
    │   │   ├──DeploymentTest.json                                  ## json format for deployment test
    │   │   ├──PtpTest.json                                         ## json format for ptp test
    │   │   ├──RebootTest.json                                      ## json format for reboot test
    │   │   ├──RfcTest.json                                         ## json format for rfc2544 test
    │   ├──bin                                                      ## virtual environmet files
    │   ├──lib/python3.10/site-packages                             ## virtual environmet files
    │   ├── spl_queries                                             ## folder that contain files with queries for creating the different dashboards
    │   │   │   ├── cpu_util_dashbords.txt                          ## queries for creating the cpu util dashboard
    │   ├──ExtractFromCpuSpreadSheet.ipynb                          ## script for extracting and creating json files from cpu util spreadsheets
    │   ├──Informal - RAN QE CPU Utilization.xlsx - component.csv   ## cpu util component spreadsheet sample
    │   ├──Informal - RAN QE CPU Utilization.xlsx - other.csv       ## cpu util scenarios metrics spreadsheet sample
    │   ├──lib64                                                    ## virtual environmet files
    │   ├──pyvenv.cfg                                               ## virtual environmet config file
    │   ├──splunkHecPush.py                                         ## script for pushing json files to splunk

## Notes and future plans
a) Some of the fields cannot be extracted from the jenkins logs. Those fields are divided to 2 groups:<br> 
    Fields that can be extracted via exsited ansible playbook and to be exported<br> 
    as env variables to the driver script(kpiRunMenu.sh). Fields that need to be inserted manuelly at this moment.<br>
b) The test json formats are not permanent and may change in the future, we are looking for adding more valuable data!.<br>
c) The repo is still not integrated as part of jenkins pipeline.<br>