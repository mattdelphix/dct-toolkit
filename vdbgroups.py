from helpers import *


# VDB group


def vdbgroup_list():
    resp = url_GET("/vdb-groups?limit=50&sort=id")
    if resp.status_code == 200:
        report_data = resp.json()['items']
        if report_data:
            tabular_report("DELPHIX Data Control Tower - VDBGROUPS LIST", report_data)
            return report_data
        else:
            print(f"\nNo VDBGroups defined.")
            return
    else:
        print(f"ERROR: Status = {resp.status_code} - {resp.text}")
        sys.exit(1)


def vdbgroup_create(name, vdbg_id):
    # create VDB_ID list
    vdb_id_list = vdbg_id.split(",")
    # build payload
    payload = {"name": name, "vdb_ids": vdb_id_list}
    resp = url_POST("/vdb-groups", payload)
    if resp.status_code == 201:
        vdbg = resp.json()['vdb_group']
        print(f"Created VDBGroup with ID={vdbg['id']}")
        return vdbg
    else:
        print(f"ERROR: Status = {resp.status_code} - {resp.text}")
        sys.exit(1)


def vdbgroup_delete(vdbg_id):
    resp = url_DELETE("/vdb-groups/" + urllib.parse.quote(vdbg_id))
    if resp.status_code == 200:
        print(f"Deleted VDBGroup with ID={vdbg_id}")
        return resp
    else:
        print(f"ERROR: Status = {resp.status_code} - {resp.text}")
        sys.exit(1)


def vdbgroup_by_id(vdbg_id):
    resp = url_GET("/vdb-groups/" + vdbg_id)
    if resp.status_code == 200:
        return resp.json()
    else:
        print(f"ERROR: Status = {resp.status_code} - {resp.text}")
        sys.exit(1)


def vdbgroup_bookmarks(dbg_id):
    resp = url_GET("/vdb-groups/" + dbg_id + "/bookmarks")
    if resp.status_code == 200:
        report_data = resp.json()['items']
        if report_data:
            tabular_report("DELPHIX Data Control Tower - VDB GROUP BOOKMARKS - Name = " + dbg_id, report_data)
            return report_data
        else:
            print(f"\nNo Bookmarks match VDBGroup with ID=" + dbg_id)
            return
    else:
        print(f"ERROR: Status = {resp.status_code} - {resp.text}")
        sys.exit(1)
