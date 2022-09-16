#
# common functions
#
import os
import sys
import json
# import time
import tabulate
import requests
import urllib.parse
import pandas as pd
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


# TODO add -format table/csv/json (default) to output
# TODO unify by_id API output in one single function

# general helpers
def build_headers():
    os.environ.setdefault('API_KEY', 'apk 2.YYgpjHxljW7A7gdU1Llu8ZiUacHw84gfbnuaqSXmNFpP8yFxsOxF1xt4urW9D3ZN')
    api_key = os.environ['API_KEY']
    if api_key is None:
        raise Exception("Set environment variable API_KEY with a valid API KEY")
    headers = {'content-type': "application/json", 'accept': "application/json", 'authorization': api_key}
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


def get_host_name():
    os.environ.setdefault('HOST', 'https://uvo18oz1uisfurv1b4l.vm.cld.sr')
    # os.environ.setdefault('HOST', 'https://172.16.111.50')
    host = os.environ['HOST']
    if host is None:
        raise Exception("Set environment variable HOST in the form: https://hostname")
    return host


def url_GET(url_encoded_text):
    rsp = requests.get(get_host_name() + "/v2" + url_encoded_text, headers=build_headers(), verify=False)
    return rsp


def url_POST(url_encoded_text, json_data):
    # print(json_data)
    if json_data:
        rsp = requests.post(get_host_name() + "/v2" + url_encoded_text, headers=build_headers(), json=json_data,
                            verify=False)
    else:
        rsp = requests.post(get_host_name() + "/v2" + url_encoded_text, headers=build_headers(), verify=False)
    return rsp


def url_PUT(url_encoded_text, json_data):
    # print(JSON_DATA)
    if json_data:
        rsp = requests.put(get_host_name() + "/v2" + url_encoded_text, headers=build_headers(), json=json_data,
                           verify=False)
    else:
        rsp = requests.put(get_host_name() + "/v2" + url_encoded_text, headers=build_headers(), verify=False)
    return rsp


def url_DELETE(url_encoded_text):
    rsp = requests.delete(get_host_name() + "/v2" + url_encoded_text, headers=build_headers(), verify=False)
    return rsp


def content_formatter(dct):
    # print formatted key, value for a dictionary
    for key, value in dct.items():
        print(f" {key} = {value}")
    return


def dct_search(dct_title, dct_query, dct_filter, dct_error, dct_output="json"):
    # this function satisifes both list and search AP calls

    if dct_filter is not None:
        payload = {"filter_expression": dct_filter}
        resp = url_POST(dct_query + "/search", payload)
    else:
        resp = url_GET(dct_query)
    if resp.status_code == 200:
        report_data = resp.json()['items']
        if report_data:
            if dct_output == "report":
                return tabular_report("DELPHIX Data Control Tower - " + dct_title + " - Filter = " + str(dct_filter),
                                      report_data)
            else:
                # return report_data
                return json.dumps(report_data, indent=4)
        else:
            print(f"\n" + dct_error)
            return
    else:
        print(f"ERROR: Status = {resp.status_code} - {resp.text}")
        sys.exit(1)


def dct_view_by_id(dct_query, view_id, dct_output="json"):
    resp = url_GET(dct_query + "/" + view_id)
    if resp.status_code == 200:
        # return resp.json()
        return json.dumps(resp.json(), indent=4)
    else:
        print(f"ERROR: Status = {resp.status_code} - {resp.text}")
        sys.exit(1)


def dct_list_by_id(dct_base_query, view_id, dct_operation, dct_output="json"):
    resp = url_GET(dct_base_query + "/" + view_id + dct_operation)
    if resp.status_code == 200:
        # return resp.json()
        return json.dumps(resp.json(), indent=4)
    else:
        print(f"ERROR: Status = {resp.status_code} - {resp.text}")
        sys.exit(1)


def dct_delete_by_id(dct_query, dct_message, delete_id):
    resp = url_DELETE(dct_query + "/" + urllib.parse.quote(delete_id))
    if resp.status_code == 204:
        print(dct_message + " - ID=" + delete_id)
        return
    else:
        print(f"ERROR: Status = {resp.status_code} - {resp.text}")
        sys.exit(1)


def dct_update_by_id(dct_query, dct_message, update_id, payload, dct_operation):
    resp = url_POST(dct_query + "/" + urllib.parse.quote(update_id) + "/" + dct_operation, payload)
    if resp.status_code == 200:
        print(dct_message + " - ID=" + update_id)
        return
    else:
        print(f"ERROR: Status = {resp.status_code} - {resp.text}")
        sys.exit(1)


def dct_post_by_id(dct_query, update_id, payload, dct_operation):
    resp = url_POST(dct_query + "/" + urllib.parse.quote(update_id) + "/" + dct_operation, payload)
    return resp
    #if resp.status_code == 201:
    #    print(dct_message + " - ID=" + update_id)
    #    return
    #else:
    #    print(f"ERROR: Status = {resp.status_code} - {resp.text}")
    #    sys.exit(1)