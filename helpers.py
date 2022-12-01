#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Copyright (c) 2022 by Delphix. All rights reserved.
#
# Author  : Matteo Ferrari, Ruben Catarrunas
# Date    : September 2022


import sys
import json
import tabulate
import requests
import urllib.parse
import pandas as pd
import cfg
import ast
import pathlib
import time
import argparse
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


# TODO add -format table/csv/json (default) to output
# TODO unify by_id API output in one single function
# TODO Post_by_id needs error checking

# general helpers
def build_headers():
    headers = {'content-type': "application/json", 'accept': "application/json", 'authorization': cfg.apikey}
    return headers


def tabular_report(title, ldict):
    # function prints list of dictionaries as a tabular report
    if not ldict:
        print("Empty report request.")
        return
    # normalize data
    df = pd.json_normalize(ldict)
    # remove NaN
    df2 = df.fillna("")
    print("\n" + title)
    print(tabulate.tabulate(df2, headers='keys', tablefmt='psql'))
    # print(tabulate.tabulate(rows, header, tablefmt="psql", showindex=False, numalign="right"))

    return


def url_GET(url_encoded_text):
    rsp = requests.get(cfg.host + "/v2" + url_encoded_text, headers=build_headers(), verify=False)
    return rsp


def url_POST(url_encoded_text, json_data):
    # print(url_encoded_text)
    # print(json_data)
    if json_data:
        rsp = requests.post(cfg.host + "/v2" + url_encoded_text, headers=build_headers(), json=json_data,
                            verify=False)
    else:
        rsp = requests.post(cfg.host + "/v2" + url_encoded_text, headers=build_headers(), verify=False)
    return rsp


def url_PUT(url_encoded_text, json_data):
    # print(JSON_DATA)
    if json_data:
        rsp = requests.put(cfg.host + "/v2" + url_encoded_text, headers=build_headers(), json=json_data,
                           verify=False)
    else:
        rsp = requests.put(cfg.host + "/v2" + url_encoded_text, headers=build_headers(), verify=False)
    return rsp


def url_PATCH(url_encoded_text, json_data):
    # print(JSON_DATA)
    if json_data:
        rsp = requests.patch(cfg.host + "/v2" + url_encoded_text, headers=build_headers(), json=json_data,
                             verify=False)
    else:
        rsp = requests.patch(cfg.host + "/v2" + url_encoded_text, headers=build_headers(), verify=False)
    return rsp


def url_DELETE(url_encoded_text):
    rsp = requests.delete(cfg.host + "/v2" + url_encoded_text, headers=build_headers(), verify=False)
    return rsp


def content_formatter(dct):
    # print formatted key, value for a dictionary
    for key, value in dct.items():
        print(f" {key} = {value}")
    return


def dct_search(dct_title, dct_query, dct_filter, dct_error, dct_output="json"):
    # this function satisfies both list and search API calls

    if dct_filter is not None:
        payload = {"filter_expression": dct_filter}
        resp = url_POST(dct_query + "/search", payload)
    else:
        resp = url_GET(dct_query)
    if cfg.level == 2:
        dct_print_response(resp)

    if resp.status_code == 200:
        report_data = resp.json()
        if report_data:
            if dct_output == "report":
                return tabular_report("DELPHIX Data Control Tower - " + dct_title + " - Filter = " + str(dct_filter),
                                      report_data)
            else:
                # return report_data
                print(json.dumps(report_data, indent=4))
                return
        else:
            print(f"\n" + dct_error)
            return
    else:
        print(f"ERROR: Status = {resp.status_code} - {resp.text}")
        sys.exit(1)


def dct_view_by_id(dct_query, view_id, dct_output="json"):
    resp = url_GET(dct_query + "/" + view_id)
    if cfg.level == 2:
        dct_print_response(resp)

    if resp.status_code == 200:
        return resp.json()
        # return json.dumps(resp.json(), indent=4)
    else:
        print(f"ERROR: Status = {resp.status_code} - {resp.text}")
        sys.exit(1)


def dct_create(dct_base_query, payload, dct_output="json"):
    resp = url_POST(dct_base_query, payload)
    if cfg.level == 2:
        dct_print_response(resp)

    if resp.status_code == 200:
        return resp.json()
    else:
        print(f"ERROR: Status = {resp.status_code} - {resp.text}")
        sys.exit(1)


def dct_list_by_id(dct_base_query, view_id, dct_operation, dct_output="json"):
    resp = url_GET(dct_base_query + "/" + view_id + dct_operation)
    if cfg.level == 2:
        dct_print_response(resp)

    if resp.status_code == 200:
        # return resp.json()
        return json.dumps(resp.json(), indent=4)
    else:
        print(f"ERROR: Status = {resp.status_code} - {resp.text}")
        sys.exit(1)


def dct_delete_by_id(dct_query, dct_message, delete_id):
    resp = url_DELETE(dct_query + "/" + urllib.parse.quote(delete_id))
    if cfg.level == 2:
        dct_print_response(resp)

    if resp.status_code == 200:
        print(dct_message + " - ID=" + delete_id)
        return resp.json()
    else:
        print(f"ERROR: Status = {resp.status_code} - {resp.text}")
        sys.exit(1)


def dct_delete_ref_by_id(dct_query, dct_message, delete_id, dct_operation, ref_id):
    # this function deletes a ref_id from a primary object
    resp = url_DELETE(
        dct_query + "/" + urllib.parse.quote(delete_id) + "/" + dct_operation + "/" + urllib.parse.quote(ref_id))
    if cfg.level == 2:
        dct_print_response(resp)

    if resp.status_code == 200:
        print(dct_message + " - ID=" + delete_id + "/" + ref_id)
        return resp.json()
    else:
        print(f"ERROR: Status = {resp.status_code} - {resp.text}")
        sys.exit(1)


def dct_update_ref_by_id(dct_query, dct_message, update_id, payload, dct_operation, ref_id):
    # this function updates a ref_id from a primary object
    resp = url_POST(
        dct_query + "/" + urllib.parse.quote(update_id) + "/" + dct_operation + "/" + urllib.parse.quote(ref_id),
        payload)
    if cfg.level == 2:
        dct_print_response(resp)

    if resp.status_code == 200:
        print(dct_message + " - ID=" + update_id + "/" + ref_id)
        return resp.json()
    else:
        print(f"ERROR: Status = {resp.status_code} - {resp.text}")
        sys.exit(1)


def dct_update_by_id(dct_query, dct_message, update_id, payload, dct_operation):
    resp = url_POST(dct_query + "/" + urllib.parse.quote(update_id) + "/" + dct_operation, payload)
    if cfg.level == 2:
        dct_print_response(resp)

    if resp.status_code == 200:
        print(dct_message + " - ID=" + update_id)
        return resp.json()
    else:
        print(f"ERROR: Status = {resp.status_code} - {resp.text}")
        sys.exit(1)


def dct_post_by_id(dct_query, update_id, payload, dct_operation):
    resp = url_POST(dct_query + "/" + urllib.parse.quote(update_id) + "/" + dct_operation, payload)
    return resp


def dct_post_ref_by_id(dct_query, update_id, payload, dct_operation, ref_id, post_operation):
    resp = url_POST(dct_query + "/" + urllib.parse.quote(update_id) + "/" + dct_operation + "/" + urllib.parse.quote(
        ref_id) + "/" + urllib.parse.quote(post_operation), payload)
    return resp


def dct_print_response(response):
    print(f"Status: {response.status_code}")
    print(response.json())


def dct_read_config(filename):
    if filename is None:
        fnm = "dct-toolkit.conf"
    else:
        fnm = filename
        flex = pathlib.Path(fnm)
        if not flex.exists():
            print("Error: Config file " + fnm + " does not exist.")
            exit(1)

    file = open(fnm, "r")
    contents = file.read()
    dictionary = ast.literal_eval(contents)
    file.close()
    # TODO add logic to check configuration
    cfg.apikey = dictionary['apikey']
    cfg.host = dictionary['host']
    cfg.level = dictionary['level']
    if cfg.level == 2:
        print(f"Config={fnm} - Host={cfg.host} - Output level={cfg.level}")

    return dictionary


def dct_job_monitor(job_id):
    job = {"status": "RUNNING"}
    print(f"Job {job_id} check...")
    while job['status'] not in ['TIMEDOUT', 'CANCELED', 'FAILED', 'COMPLETED']:
        job = dct_view_by_id("/jobs", job_id)
        time.sleep(3)

    if job['status'] != 'COMPLETED':
        if 'error_details' in job:
            print(f"Job {job_id} {job['status']} - {job['error_details']}")
        else:
            print(f"Job {job_id} {job['status']} - {job['update_time']}")
        exit(1)
    else:
        print(f"Job {job_id} COMPLETED - {job['update_time']}")


class dct_parsetags(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, dict())
        tgs = None
        for value in values:
            key, value = value.split('=')
            getattr(namespace, self.dest)[key] = value
            tgs = [{"key": k, "value": v} for (k, v) in namespace.tags.items()]
        namespace.tags = tgs
