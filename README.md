# KPI_Splunk
Git repository for the "KPI automation scripts and splunk pushing and quries scripts.

## Overview

The repository contains scripts mainly for:
    -extracting tests results metrics and parameters, format them and create json 
     files with the formatted extracted data.

    -pushing the json files to splunk instance(under this index=ecosystem-qe-dev) as new events records for later analysing and reporting.

    -queries for creating different dashboards based on the collected KPIs.

## Goal
The main goal of this repo is to be served as a POC for the Splunk alternative for autamtically collacting and storing tests results and creating dashboards,
rather then menually collecting the results and store them in spreadsheets and later produce reports from them using Google data studio.


## Project structure

├── venv                                                        ## folder that conatin all the required files for the virtuall environment and the repo files<br>
│   ├──ExtractTestsResults                                      ##contains different folders with script for extracting the metrics from jenkins logs and store them in json files<br>
│   │   │   ├──CreateAvailability                               ## folder with scripts for creating json file from oslat and cyclictest jenkins log<br>
│   │   │   │   │   ├──CreateAvailabilityJson.py                ## create json file from extracted fields<br>
│   │   │   │   │   ├──extractResultsFromAvailability.sh        ## extract fields from jenkins log<br>
│   │   │   ├──CreateCpuUtil                                    ## folder with scripts for creating json file from cpu util jenkins log<br>
│   │   │   │   │   ├──CreateCpuUtilIterJson.py                 ## create json file from extracted fields<br>
│   │   │   │   │   ├──extractResultsFromCPUUtil.sh             ## extract fields from jenkins log<br>
│   │   │   ├──CreateDeployment                                 ## folder with scripts for creating json file from deployment jenkins log<br>
│   │   │   │   │   ├──CreateDeploymentJson.py                  ## create json file from extracted fields<br>
│   │   │   │   │   ├──ExtractResultsFromDeployment.sh          ## extract fields from jenkins log<br>
│   │   │   ├──CreateNetwork                                    ## folder with scripts for creating json file from rfc and ptp jenkins log<br>
│   │   │   │   │   ├──CreateNetworkJson.py                     ## create json file from extracted fields<br>
│   │   │   │   │   ├──extractResultsFromNetwork.sh             ## extract fields from jenkins log<br>
│   │   │   ├──CreateReboot                                     ## folder with scripts for creating json file from reboot jenkins log<br>
│   │   │   │   │   ├──CreateRebootJson.py                      ## create json file from extracted fields<br>
│   │   │   │   │   ├──extractResultsFromReboot.sh              ## extract fields from jenkins log<br>
│   │   │   ├──JenkinsLogs                                      ## folder that contains test jenkins logs samples<br>
│   │   │   ├──JsonTestsFolders                                 ## folder that contains different json files that were created from a given jenkins logs/spreadsheets<br>
│   │   │   ├──Utils                                            ## folder with different utils scripts<br>
│   │   │   │   │   ├──ExportAnsibleVars.sh                     ## script for exporting job parameters that were extracted via ansible playbook(still not in the repo)<br>
│   │   │   │   │   ├──Utils.py                                 ## utils module <br>
│   │   │   ├──kpiRunMenu.sh                                    ## driver script for selecting the requried test metrics extraction(still not fully aotumated)<br>
│   ├──JsonFormatsForSplunk                                     ##  folder that contain all the corrent json formats for the tests that are pushed to splunk<br>
│   │   │   ├──AvailabilityTest.json                            ## json format for cyclictest and oslat<br>
│   │   │   ├──CpuUtilTest.json                                 ## json format for cpu util test<br>
│   │   │   ├──DeploymentTest.json                              ## json format for deployment test<br>
│   │   │   ├──PtpTest.json                                     ## json format for ptp test<br>
│   │   │   ├──RebootTest.json                                  ## json format for reboot test<br>
│   │   │   ├──RfcTest.json                                     ## json format for rfc2544 test<br>
│   ├──bin                                                      ## virtual environmet files<br>
│   ├──lib/python3.10/site-packages                             ## virtual environmet files<br>
│   ├── spl_queries                                             ## folder that contain files with queries for creating the different dashboards<br>
│   │   │   ├── cpu_util_dashbords.txt                          ## queries for creating the cpu util dashboard<br>
│   ├──ExtractFromCpuSpreadSheet.ipynb                          ## script for extracting and creating json files from cpu util spreadsheets<br>
│   ├──Informal - RAN QE CPU Utilization.xlsx - component.csv   ## cpu util component spreadsheet sample<br>
│   ├──Informal - RAN QE CPU Utilization.xlsx - other.csv       ## cpu util scenarios metrics spreadsheet sample<br>
│   ├──lib64                                                    ## virtual environmet files<br>
│   ├──pyvenv.cfg                                               ## virtual environmet config file<br>
│   ├──splunkHecPush.py                                         ## script for pushing json files to splunk<br>



## Notes and future plans:
    1. Some of the fields cannot be extracted from the jenkins logs. Those fields are divided to 2 groups:
        - Fields that can be extracted via exsited ansible playbook and to be exported as env variables to the driver script(kpiRunMenu.sh).
        - Fields that need to be inserted manuelly at this moment.
    2. The test json formats are not permant and may change in the future, we are looking for adding more valuable data!.
    3. The repo is still not integrated as part of jenkins pipeline.