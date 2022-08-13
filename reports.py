from helpers import *

# Reports API

def report_api_usage(BEGIN, END):
    date_begin = urllib.parse.quote(BEGIN)
    date_end   = urllib.parse.quote(END)
    resp = url_GET("/reporting/api-usage-report?start_date="+date_begin+"&end_date="+date_end)
    if resp.status_code == 200:
        report_data = resp.json()['items']
        if report_data:
            tabular_report("DELPHIX Data Control Tower - API USAGE REPORT",report_data)
        else:
            print(f"\nNo API Usage Report for this interval - {BEGIN} to {END}")
            return
    else:
        print(f"ERROR: Status = {resp.status_code} - {resp.text}")
        sys.exit(1)
    return

def report_storage_summary():
    resp = url_GET("/reporting/virtualization-storage-summary-report")
    if resp.status_code == 200:
        tabular_report("DELPHIX Data Control Tower - VIRTUALIZATION STORAGE SUMMARY REPORT",resp.json()['items'])
    else:
        print(f"ERROR: Status = {resp.status_code} - {resp.text}")
        sys.exit(1)
    return

def report_vdb_inventory():
    resp = url_GET("/reporting/vdb-inventory-report")
    if resp.status_code == 200:
        tabular_report("DELPHIX Data Control Tower - VDB INVENTORY REPORT",resp.json()['items'])
    else:
        print(f"ERROR: Status = {resp.status_code} - {resp.text}")
        sys.exit(1)
    return

def report_dsource_usage():
    resp = url_GET("/reporting/dsource-usage-report")
    if resp.status_code == 200:
        tabular_report("DELPHIX Data Control Tower - DSOURCE USAGE REPORT",resp.json()['items'])
    else:
        print(f"ERROR: Status = {resp.status_code} - {resp.text}")
        sys.exit(1)
    return
