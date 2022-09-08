#
# common functions
#
import os
import sys
import json
import time
import tabulate
import requests
import urllib.parse
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
import pandas as pd

# TODO add -format table/csv/json (default) to output
# TODO unify by_id API output in one single function

# general helpers
def build_headers():
    os.environ.setdefault('API_KEY', 'apk 2.YYgpjHxljW7A7gdU1Llu8ZiUacHw84gfbnuaqSXmNFpP8yFxsOxF1xt4urW9D3ZN')
    API_KEY = os.environ['API_KEY']

    if API_KEY is None:
        raise Exception("Set environment variable API_KEY with a valid API KEY")

    headers = {}
    headers['content-type'] = "application/json"
    headers['accept'] = "application/json"
    headers['authorization'] = API_KEY
    return headers

def tabular_report(TITLE, ldict):
    # function prints list of dictionaries as a tabular report
    if not ldict:
        print("Empty report request.")
        return
    #normalize data
    df = pd.json_normalize(ldict)
    # remove NaN
    df2 = df.fillna("")
    print("\n"+TITLE)
    print(tabulate.tabulate(df2, headers='keys', tablefmt='psql'))
    #print(tabulate.tabulate(rows, header, tablefmt="psql", showindex=False, numalign="right"))

    return

def get_host_name():
    #os.environ.setdefault('HOST', 'https://uvo18oz1uisfurv1b4l.vm.cld.sr')
    os.environ.setdefault('HOST', 'https://172.16.111.50')
    HOST = os.environ['HOST']
    if HOST is None:
        raise Exception("Set environment variable HOST in the form: https://hostname")
    return HOST

def url_GET(url_encoded_text):
    rsp = requests.get(get_host_name() + "/v2" + url_encoded_text, headers=build_headers(), verify=False)
    return rsp

def url_POST(url_encoded_text,JSON_DATA):
    #print(JSON_DATA)
    if JSON_DATA:
        rsp = requests.post(get_host_name() + "/v2" + url_encoded_text, headers=build_headers(), json=JSON_DATA, verify=False)
    else:
        rsp = requests.post(get_host_name() + "/v2" + url_encoded_text, headers=build_headers(), verify=False)
    return rsp

def url_DELETE(url_encoded_text):
    rsp = requests.delete(get_host_name() + "/v2" + url_encoded_text, headers=build_headers(), verify=False)
    return rsp

def content_formatter(dct):
    # print formatted key, value for a dictionary
    for key, value in dct.items():
        print(f" {key} = {value}")
    return