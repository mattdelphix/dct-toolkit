from helpers import *


# Source API

def source_list():
    resp = url_GET("/sources?limit=50&sort=id")
    if resp.status_code == 200:
        report_data = resp.json()['items']
        if report_data:
            tabular_report("DELPHIX Data Control Tower - SOURCES LIST", report_data)
            return report_data
        else:
            print(f"\nNo Sources defined.")
            return
    else:
        print(f"ERROR: Status = {resp.status_code} - {resp.text}")
        sys.exit(1)


def source_search(source_filter):
    payload = {}
    payload["filter_expression"] = "SEARCH '" + source_filter + "'"
    resp = url_POST("/sources/search?limit=50&sort=id", payload)
    if resp.status_code == 200:
        report_data = resp.json()['items']
        if report_data:
            tabular_report("DELPHIX Data Control Tower - SOURCE SEARCH", report_data)
            return report_data
        else:
            print(f"\nNo SOURCE match search criteria.")
            return
    else:
        print(f"ERROR: Status = {resp.status_code} - {resp.text}")
        sys.exit(1)
