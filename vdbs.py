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


def vdb_by_id(vdb_id):
    resp = url_GET("/vdbs/" + vdb_id)
    if resp.status_code == 200:
        return resp.json()
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


def vdb_operation(vdb_id, ops):
    ops = ops.lower()
    if not any(x in ops for x in ["enable", "disable", "stop", "start"]):
        print("Wrong operation on VDB: "+ops)
        sys.exit(1)
    payload =""
    if ops == "enable":
        payload = {"attempt_start": "true"}
    if ops == "disable":
        payload = {"attempt_cleanup": "true"}
    resp = url_POST("/vdbs/"+urllib.parse.quote(vdb_id)+"/"+ops, payload)
    if resp.status_code == 200:
        return json.loads(resp.text)
    else:
        print(f"ERROR: Status = {resp.status_code} - {resp.text}")
        sys.exit(1)
