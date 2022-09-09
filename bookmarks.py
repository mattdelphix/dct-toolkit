from helpers import *


# Bookmark


def bookmark_list():
    resp = url_GET("/bookmarks?limit=50&sort=id")
    if resp.status_code == 200:
        report_data = resp.json()['items']
        if report_data:
            tabular_report("DELPHIX Data Control Tower - BOOKMARKS LIST", report_data)
            return report_data
        else:
            print(f"\nNo Bookmarks defined.")
            return
    else:
        print(f"ERROR: Status = {resp.status_code} - {resp.text}")
        sys.exit(1)


def bookmark_create(name, bookmark_id, retention):
    # create VDB_ID list
    vdb_id_list = bookmark_id.split(",")
    # build payload
    payload = {"name": name, "vdb_ids": vdb_id_list, "retention": retention}
    resp = url_POST("/bookmarks", payload)
    if resp.status_code == 201:
        bookm = resp.json()
        print(f"Created Bookmark with ID={name}, Retention={retention}")
        return bookm
    else:
        print(f"ERROR: Status = {resp.status_code} - {resp.text}")
        sys.exit(1)


def bookmark_delete(bookmark_id):
    resp = url_DELETE("/bookmarks/" + urllib.parse.quote(bookmark_id))
    if resp.status_code == 200:
        print(f"Deleted VDB with ID={bookmark_id}")
        return resp.json()
    else:
        print(f"ERROR: Status = {resp.status_code} - {resp.text}")
        sys.exit(1)


def bookmark_vdbgroup_list(bookmark_id):
    resp = url_GET("/dsources/" + urllib.parse.quote(bookmark_id) + "/vdb-groups")
    if resp.status_code == 200:
        report_data = resp.json()['items']
        if report_data:
            tabular_report("DELPHIX Data Control Tower - BOOKMARK VDBGROUP LIST", report_data)
            return report_data
        else:
            print(f"\nNo VDBGroups apply to this bookmark or bookmark does not exist.")
            return
    else:
        print(f"ERROR: Status = {resp.status_code} - {resp.text}")
        sys.exit(1)
