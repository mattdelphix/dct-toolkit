from helpers import *

# VDB group


def vdbgroup_list():
    resp = url_GET("/vdb-groups?limit=50&sort=id")
    if resp.status_code == 200:
        report_data = resp.json()['items']
        if report_data:
            tabular_report("DELPHIX Data Control Tower - VDBGROUPS LIST",report_data)
            return report_data
        else:
            print(f"\nNo VDBGroups defined.")
            return
    else:
        print(f"ERROR: Status = {resp.status_code} - {resp.text}")
        sys.exit(1)

def vdbgroup_create(NAME, VDBG_ID):
    # create VDB_ID list
    vdb_id_list = VDBG_ID.split(",")
    # build payload
    payload = {}
    payload["name"] = NAME
    payload["vdb_ids"] = vdb_id_list
    resp = url_POST("/vdb-groups",payload)
    if resp.status_code == 201:
        vdbg=resp.json()['vdb_group']
        print(f"Created VDBGroup with ID={vdbg['id']}")
        return vdbg
    else:
        print(f"ERROR: Status = {resp.status_code} - {resp.text}")
        sys.exit(1)

def vdbgroup_search(FILTER):
    payload = {}
    payload["filter_expression"] = "SEARCH '"+FILTER+"'"
    resp = url_POST("/vdb-groups/search?limit=50&sort=id", payload)
    if resp.status_code == 200:
        report_data = resp.json()['items']
        if report_data:
            tabular_report("DELPHIX Data Control Tower - VDB GROUP SEARCH - Name = "+FILTER,report_data)
            return report_data
        else:
            print(f"\nNo VDBGrooups match search criteria.")
            return
    else:
        print(f"ERROR: Status = {resp.status_code} - {resp.text}")
        sys.exit(1)


def vdbgroup_delete(VDBG_ID):
    resp = url_DELETE("/vdb-groups/"+urllib.parse.quote(VDBG_ID))
    if resp.status_code == 200:
        print(f"Deleted VDBGroup with ID={VDBG_ID}")
        return resp
    else:
        print(f"ERROR: Status = {resp.status_code} - {resp.text}")
        sys.exit(1)

def vdbgroup_by_id(VDBG_ID):
    resp = url_GET("/vdb-groups/"+VDBG_ID)
    if resp.status_code == 200:
        print(f"View VDBGroup with ID={VDBG_ID}")
        return resp.json()
    else:
        print(f"ERROR: Status = {resp.status_code} - {resp.text}")
        sys.exit(1)

def vdbgroup_bookmarks(DBG_ID):
    resp = url_GET("/vdb-groups/"+DBG_ID+"/bookmarks")
    if resp.status_code == 200:
        report_data = resp.json()['items']
        if report_data:
            tabular_report("DELPHIX Data Control Tower - VDB GROUP BOOKMARKS - Name = "+DBG_ID,report_data)
            return report_data
        else:
            print(f"\nNo Bookmarks match VDBGroup with ID="+DBG_ID)
            return
    else:
        print(f"ERROR: Status = {resp.status_code} - {resp.text}")
        sys.exit(1)
    return
