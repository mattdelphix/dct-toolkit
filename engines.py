from helpers import *

# Engine API

def engine_list():
    resp = url_GET("/management/engines?limit=50&sort=id")
    if resp.status_code == 200:
        report_data = resp.json()['items']
        if report_data:
            tabular_report("DELPHIX Data Control Tower - ENGINE LIST",report_data)
            return report_data
        else:
            print(f"\nNo Engines defined.")
            return
    else:
        print(f"ERROR: Status = {resp.status_code} - {resp.text}")
        sys.exit(1)
    return

def engine_search(FILTER):
    payload = {}
    payload["filter_expression"] = "SEARCH '"+FILTER+"'"
    resp = url_POST("/management/engines/search?limit=50&sort=id",payload)
    if resp.status_code == 200:
        report_data = resp.json()['items']
        if report_data:
            tabular_report("DELPHIX Data Control Tower - ENGINE SEARCH",report_data)
            return report_data
        else:
            print(f"\nNo Engines match search criteria.")
            return
    else:
        print(f"ERROR: Status = {resp.status_code} - {resp.text}")
        sys.exit(1)
    return
