from helpers import *

# Environment API

def environment_by_id(ID):
    resp = url_GET("/environments/"+urllib.parse.quote(ID))
    if resp.status_code == 200:
        result = json.loads(resp.text)
        content_formatter(result)
        return result
    else:
        print(f"ERROR: Status = {resp.status_code} - {resp.text}")
        sys.exit(1)
    return

def environment_operation(ID, OPS):
    OPS = OPS.lower()
    if not any(x in OPS for x in ["enable", "disable"]):
        print("Wrong operation on environment: "+OPS)
        sys.exit(1)

    resp = url_POST("/environments/"+urllib.parse.quote(ID)+"/"+OPS,"")
    if resp.status_code == 200:
        return json.loads(resp.text)
    else:
        print(f"ERROR: Status = {resp.status_code} - {resp.text}")
        sys.exit(1)
    return

def environment_search(FILTER):
    payload = {}
    payload["filter_expression"] = "SEARCH '"+FILTER+"'"
    resp = url_POST("/environments/search?limit=50&sort=id",payload)
    if resp.status_code == 200:
        report_data = resp.json()['items']
        if report_data:
            tabular_report("DELPHIX Data Control Tower - ENVIRONMENT SEARCH",report_data)
            return report_data
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
            return report_data
        else:
            print(f"\nNo Environments defined.")
            return
    else:
        print(f"ERROR: Status = {resp.status_code} - {resp.text}")
        sys.exit(1)
    return
