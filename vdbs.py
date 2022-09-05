from helpers import *


# VDB API

def vdb_list():
    resp = url_GET("/vdbs?limit=50&sort=id")
    if resp.status_code == 200:
        report_data = resp.json()['items']
        if report_data:
            tabular_report("DELPHIX Data Control Tower - VDB LIST", report_data)
            return report_data
        else:
            print(f"\nNo VDBS defined.")
            return
    else:
        print(f"ERROR: Status = {resp.status_code} - {resp.text}")
        sys.exit(1)


def vdb_search(vdb_filter):
    payload = {"filter_expression": "SEARCH '" + vdb_filter + "'"}
    resp = url_POST("/vdbs/search?limit=50&sort=id", payload)
    if resp.status_code == 200:
        report_data = resp.json()['items']
        if report_data:
            tabular_report("DELPHIX Data Control Tower - VDB SEARCH", report_data)
            return report_data
        else:
            print(f"\nNo VDB match search criteria.")
            return
    else:
        print(f"ERROR: Status = {resp.status_code} - {resp.text}")
        sys.exit(1)


def vdb_delete(vdb_id):
    resp = url_DELETE("/vdbs/" + urllib.parse.quote(vdb_id))
    if resp.status_code == 200:
        print(f"Deleted VDB with ID={vdb_id}")
        return resp.json()
    else:
        print(f"ERROR: Status = {resp.status_code} - {resp.text}")
        sys.exit(1)
