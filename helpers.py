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

# Engine API
def engine_register(NAME, HOSTNAME, USERNAME, PASSWORD):
    payload = {}
    payload['name'] = NAME
    payload['hostname'] = HOSTNAME
    payload['username'] = USERNAME
    payload['password'] = PASSWORD
    payload['insecure_ssl'] = "true"
    payload['unsafe_ssl_hostname_check'] = "true"
    resp = url_POST("/management/engines" , payload)
    if resp.status_code == 201:
        print(resp.text)
    else:
        print(f"ERROR: Status = {resp.status_code} - {resp.text}")
        sys.exit(1)
    return

def engine_list():
    resp = url_GET("/management/engines?limit=50&sort=id")
    if resp.status_code == 200:
        tabular_report("DELPHIX Data Control Tower - ENGINE LIST",resp.json()['items'])
    else:
        print(f"ERROR: Status = {resp.status_code} - {resp.text}")
        sys.exit(1)
    return

# environment API
def environment_search(FILTER):
    payload = {}
    payload["filter_expression"] = "SEARCH '"+FILTER+"'"
    resp = url_POST("/environments/search?limit=50&sort=id",payload)
    if resp.status_code == 200:
        report_data = resp.json()['items']
        if report_data:
            tabular_report("DELPHIX Data Control Tower - ENVIRONMENT SEARCH",report_data)
        else:
            print(f"\nNo Environments match search criteria.")
            return
    else:
        print(f"ERROR: Status = {resp.status_code} - {resp.text}")
        sys.exit(1)
    return


def environment_list():
    resp = url_GET("/environments?limit=50&sort=id")
    if resp.status_code == 200:
        report_data = resp.json()['items']
        if report_data:
            tabular_report("DELPHIX Data Control Tower - ENVIRONMENT LIST",report_data)
        else:
            print(f"\nNo Environments defined.")
            return
    else:
        print(f"ERROR: Status = {resp.status_code} - {resp.text}")
        sys.exit(1)
    return


# Reports

def report_api_usage(BEGIN, END):
    date_begin = urllib.parse.quote(BEGIN)
    date_end   = urllib.parse.quote(END)
    resp = url_GET("/reporting/api-usage-report?start_date="+date_begin+"&end_date="+date_end)
    if resp.status_code == 200:
        report_data = resp.json()['items']
        if report_data:
            tabular_report("DELPHIX Data Control Tower - API USAGE REPORT",report_data)
        else:
            print(f"\nNo API Usage Report for this interval - {BEGIN} to {END}")
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

# VDB API
def vdb_list():
    resp = url_GET("/vdbs?limit=50&sort=id")
    if resp.status_code == 200:
        report_data = resp.json()['items']
        if report_data:
            tabular_report("DELPHIX Data Control Tower - VDB LIST",report_data)
        else:
            print(f"\nNo VDBS defined.")
            return
    else:
        print(f"ERROR: Status = {resp.status_code} - {resp.text}")
        sys.exit(1)
    return
def vdb_search(FILTER):
    payload = {}
    payload["filter_expression"] = "SEARCH '"+FILTER+"'"
    resp = url_POST("/vdbs/search?limit=50&sort=id",payload)
    if resp.status_code == 200:
        report_data = resp.json()['items']
        if report_data:
            tabular_report("DELPHIX Data Control Tower - VDB SEARCH",report_data)
        else:
            print(f"\nNo VDB match search criteria.")
            return
    else:
        print(f"ERROR: Status = {resp.status_code} - {resp.text}")
        sys.exit(1)
    return

# VDB group
def vdbgroup_list():
    resp = url_GET("/vdb-groups?limit=50&sort=id")
    if resp.status_code == 200:
        report_data = resp.json()['items']
        if report_data:
            tabular_report("DELPHIX Data Control Tower - VDB GROUPS LIST",report_data)
        else:
            print(f"\nNo VDB Groups defined.")
            return
    else:
        print(f"ERROR: Status = {resp.status_code} - {resp.text}")
        sys.exit(1)
    return

def vdbgroup_search(FILTER):
    payload = {}
    payload["filter_expression"] = "SEARCH '"+FILTER+"'"
    resp = url_POST("/vdb-groups/search?limit=50&sort=id",payload)
    if resp.status_code == 200:
        report_data = resp.json()['items']
        if report_data:
            tabular_report("DELPHIX Data Control Tower - VDB GROUP SEARCH",report_data)
        else:
            print(f"\nNo VDB GROUPS match search criteria.")
            return
    else:
        print(f"ERROR: Status = {resp.status_code} - {resp.text}")
        sys.exit(1)
    return


# Source API
def source_list():
    resp = url_GET("/sources?limit=50&sort=id")
    if resp.status_code == 200:
        report_data = resp.json()['items']
        if report_data:
            tabular_report("DELPHIX Data Control Tower - SOURCES LIST",report_data)
        else:
            print(f"\nNo Sources defined.")
            return
    else:
        print(f"ERROR: Status = {resp.status_code} - {resp.text}")
        sys.exit(1)
    return
def source_search(FILTER):
    payload = {}
    payload["filter_expression"] = "SEARCH '"+FILTER+"'"
    resp = url_POST("/sources/search?limit=50&sort=id",payload)
    if resp.status_code == 200:
        report_data = resp.json()['items']
        if report_data:
            tabular_report("DELPHIX Data Control Tower - SOURCE SEARCH",report_data)
        else:
            print(f"\nNo SOURCE match search criteria.")
            return
    else:
        print(f"ERROR: Status = {resp.status_code} - {resp.text}")
        sys.exit(1)
    return

# Dsource API
def dsource_list():
    resp = url_GET("/dsources?limit=50&sort=id")
    if resp.status_code == 200:
        report_data = resp.json()['items']
        if report_data:
            tabular_report("DELPHIX Data Control Tower - DSOURCES LIST",report_data)
        else:
            print(f"\nNo DSources defined.")
            return
    else:
        print(f"ERROR: Status = {resp.status_code} - {resp.text}")
        sys.exit(1)
    return
def dsource_search(FILTER):
    payload = {}
    payload["filter_expression"] = "SEARCH '"+FILTER+"'"
    resp = url_POST("/dsources/search?limit=50&sort=id",payload)
    if resp.status_code == 200:
        report_data = resp.json()['items']
        if report_data:
            tabular_report("DELPHIX Data Control Tower - DSOURCE SEARCH",report_data)
        else:
            print(f"\nNo DSOURCE match search criteria.")
            return
    else:
        print(f"ERROR: Status = {resp.status_code} - {resp.text}")
        sys.exit(1)
    return


# general helpers
def build_headers():
    os.environ.setdefault('API_KEY', 'APK 2.YYgpjHxljW7A7gdU1Llu8ZiUacHw84gfbnuaqSXmNFpP8yFxsOxF1xt4urW9D3ZN')
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
    header = ldict[0].keys()
    rows = [x.values() for x in ldict]
    print("\n"+TITLE)
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
    #print(JSON_DATA)
    rsp = requests.post(get_host_name() + "/v2" + url_encoded_text, headers=build_headers(), json=JSON_DATA, verify=False)
    return rsp