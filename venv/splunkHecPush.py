#!/usr/bin/env python

### Parameters:
# python3 splunkHecPush.py -j ExtractTestsResults/cpuUtil/cpu_util-16771728269714382.json -i ecosystem-qe-dev -t 94eeb2f9-8e5f-4c86-adec-336b3368c74e


import json
import requests
import argparse

SPLUNK_URL = 'https://splunk-hec.prod.utility-us-east-2.redhat.com'
HEC_PORT = '8088'


class SplunkHEC:
    def __init__(self, token, uri, port):
        if 'http' not in uri:
            raise("no http or https found in hostname")
        self.token = token
        self.uri = uri + ":" + port + "/services/collector"

    """
    event data is the actual event data
    metadata are sourcetype, index, etc
    """
    def send(self, index, json_path):
        headers = {'Authorization': 'Splunk ' + self.token}
        params = {'index': index}
        payload = {}
        payload.update({
            "host": self.uri,
            "sourcetype": "_json"
            })
        with open(json_path, 'r') as f:
            j_data = json.load(f)
            payload.update({"event": j_data})
        r = requests.post(
            self.uri, data=json.dumps(payload),
            headers=headers,
            params=params,
            verify=False
            )
        return r.status_code, r.text, r.headers


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--index',
                        required=True,
                        default=None,
                        help='index name to push data into. example: "main"')
    parser.add_argument('-j', '--json_path',
                        required=True,
                        default=None,
                        help='json file path with the data to push to splunk')
    parser.add_argument('-t', '--token',
                        required=True,
                        default=None,
                        help='splunk HEC token')
    args = parser.parse_args()

    splunk = SplunkHEC(args.token, SPLUNK_URL, HEC_PORT)
    print(splunk.send(args.index, args.json_path))


if __name__ == "__main__":
    main()
