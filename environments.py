from helpers import *


# Environment API

def environment_operation(env_id, ops):
    ops = ops.lower()
    if not any(x in ops for x in ["enable", "disable", "refresh"]):
        print("Wrong operation on Environment: " + ops)
        sys.exit(1)
    resp = url_POST("/environments/" + urllib.parse.quote(env_id) + "/" + ops, "")
    if resp.status_code == 200:
        return json.loads(resp.text)
    else:
        print(f"ERROR: Status = {resp.status_code} - {resp.text}")
        sys.exit(1)


def environment_list():
    resp = url_GET("/environments?limit=50&sort=id")
    if resp.status_code == 200:
        report_data = resp.json()['items']
        if report_data:
            tabular_report("DELPHIX Data Control Tower - ENVIRONMENT LIST", report_data)
            return report_data
        else:
            print(f"\nNo Environments defined.")
            return
    else:
        print(f"ERROR: Status = {resp.status_code} - {resp.text}")
        sys.exit(1)


def environment_delete(env_id):
    resp = url_DELETE("/environments/" + urllib.parse.quote(env_id))
    if resp.status_code == 200:
        print(f"Deleted Environment with ID={env_id}")
        return resp.json()
    else:
        print(f"ERROR: Status = {resp.status_code} - {resp.text}")
        sys.exit(1)
