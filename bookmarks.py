from helpers import *

# Bookmark

def bookmark_list():
    resp = url_GET("/bookmarks?limit=50&sort=id")
    if resp.status_code == 200:
        report_data = resp.json()['items']
        if report_data:
            tabular_report("DELPHIX Data Control Tower - BOOKMARKS LIST",report_data)
            return report_data
        else:
            print(f"\nNo Bookmarks defined.")
            return
    else:
        print(f"ERROR: Status = {resp.status_code} - {resp.text}")
        sys.exit(1)
    return

def bookmark_create(NAME, VDB_ID, RETENTION):
    # create VDB_ID list
    vdb_id_list = VDB_ID.split(",")
    # build payload
    payload = {}
    payload["name"] = NAME
    payload["vdb_ids"] = vdb_id_list
    payload["retention"] = RETENTION
    resp = url_POST("/bookmarks",payload)
    if resp.status_code == 201:
        bookm=resp.json()
        print(f"Created Bookmark with ID={NAME}, Retention={RETENTION}")
        return bookm
    else:
        print(f"ERROR: Status = {resp.status_code} - {resp.text}")
        sys.exit(1)
    return
