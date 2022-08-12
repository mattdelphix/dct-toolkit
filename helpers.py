#
# common functions
#
import os
import sys
import tabulate
import requests
import urllib.parse
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def report_api_usage(BEGIN, END):
    date_begin = urllib.parse.quote(BEGIN)
    date_end   = urllib.parse.quote(END)
    resp = url_GET("/reporting/api-usage-report?start_date="+date_begin+"&end_date="+date_end)
    if resp.status_code == 200:
        report_data = resp.json()['items']
        if report_data:
            tabular_report("DELPHIX Data Control Tower - API USAGE REPORT",report_data)
        else:
            print(f"No API Usage Report for this interval - {BEGIN} to {END}")
            return
    else:
        print(f"ERROR: Status = {resp.status_code} - {resp.text}")
        sys.exit(1)
    return

def report_storage_summary():
    resp = url_GET("/reporting/virtualization-storage-summary-report")
    if resp.status_code == 200:
        tabular_report("DELPHIX Data Control Tower - VIRTUALIZATION STORAGE SUMMARY REPORT",resp.json()['items'])
    else:
        print(f"ERROR: Status = {resp.status_code} - {resp.text}")
        sys.exit(1)
    return

def report_vdb_inventory():
    resp = url_GET("/reporting/vdb-inventory-report")
    if resp.status_code == 200:
        tabular_report("DELPHIX Data Control Tower - VDB INVENTORY REPORT",resp.json()['items'])
    else:
        print(f"ERROR: Status = {resp.status_code} - {resp.text}")
        sys.exit(1)
    return

def report_dsource_usage():
    resp = url_GET("/reporting/dsource-usage-report")
    if resp.status_code == 200:
        tabular_report("DELPHIX Data Control Tower - DSOURCE USAGE REPORT",resp.json()['items'])
    else:
        print(f"ERROR: Status = {resp.status_code} - {resp.text}")
        sys.exit(1)
    return

def build_headers():
    os.environ.setdefault('API_KEY', 'APK 2.YYgpjHxljW7A7gdU1Llu8ZiUacHw84gfbnuaqSXmNFpP8yFxsOxF1xt4urW9D3ZN')
    API_KEY = os.environ['API_KEY']

    if API_KEY is None:
        raise Exception("Set environment variable API_KEY with a valid API KEY")

    headers = {}
    headers['content'] = "application/json"
    headers['accept'] = "application/json"
    headers['authorization'] = API_KEY
    return headers

def tabular_report(TITLE, ldict):
    # function prints list of dictionaries as a tabular report
    if not ldict:
        raise Exception("Empty report request.")
        return
    header = ldict[0].keys()
    rows = [x.values() for x in ldict]
    print(TITLE)
    print(tabulate.tabulate(rows, header, tablefmt="psql", showindex=False, numalign="right"))
    return

def get_host_name():
    os.environ.setdefault('HOST', 'https://uvo18oz1uisfurv1b4l.vm.cld.sr')
    HOST = os.environ['HOST']
    if HOST is None:
        raise Exception("Set environment variable HOST in the form: https://hostname")
    return HOST

def url_GET(url_encoded_text):
    rsp = requests.get(get_host_name() + "/v2" + url_encoded_text, headers=build_headers(), verify=False)
    return rsp

def url_POST(url_encoded_text,JSON_DATA):
    rsp = requests.post(get_host_name() + "/v2" + url_encoded_text, data=JSON_DATA, headers=build_headers(), verify=False)
    return rsp