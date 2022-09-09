from helpers import *


# Reports API

# TODO add sort and limit to all reports as parameter

def report_api_usage(begin, end):
    date_begin = urllib.parse.quote(begin)
    date_end = urllib.parse.quote(end)
    resp = url_GET("/reporting/api-usage-report?start_date=" + date_begin + "&end_date=" + date_end)
    if resp.status_code == 200:
        report_data = resp.json()['items']
        if report_data:
            tabular_report(f"DELPHIX Data Control Tower - API USAGE REPORT\nInterval: {begin} to {end}", report_data)
        else:
            print(f"\nNo API Usage Report for this interval - {begin} to {end}")
            return
    else:
        print(f"ERROR: Status = {resp.status_code} - {resp.text}")
        sys.exit(1)


def report_product_info():
    resp = url_GET("/reporting/product_info")
    if resp.status_code == 200:
        tabular_report("DELPHIX Data Control Tower - PRODUCT INFO", resp.json())
    else:
        print(f"ERROR: Status = {resp.status_code} - {resp.text}")
        sys.exit(1)


def report_vdb_inventory(report_filter):
    display_filter = ""
    if report_filter is not None:
        payload = {"filter_expression": report_filter}
        display_filter = "SEARCH: "+report_filter
        resp = url_POST("/reporting/vdb-inventory-report/search", payload)
    else:
        resp = url_GET("/reporting/vdb-inventory-report")
    if resp.status_code == 200:
        report_data = resp.json()['items']
        if report_data:
            tabular_report("DELPHIX Data Control Tower - DSource Usage Report " + display_filter, report_data)
            return report_data
        else:
            print(f"\nNo DSources match search criteria.")
            return
    else:
        print(f"ERROR: Status = {resp.status_code} - {resp.text}")
        sys.exit(1)


def report_dsource_usage(report_filter):
    display_filter = ""
    if report_filter is not None:
        payload = {"filter_expression": report_filter}
        display_filter = "SEARCH: "+report_filter
        resp = url_POST("/reporting/dsource-usage-report/search", payload)
    else:
        resp = url_GET("/reporting/dsource-usage-report")
    if resp.status_code == 200:
        report_data = resp.json()['items']
        if report_data:
            tabular_report("DELPHIX Data Control Tower - DSource Usage Report " + display_filter, report_data)
            return report_data
        else:
            print(f"\nNo DSources match search criteria.")
            return
    else:
        print(f"ERROR: Status = {resp.status_code} - {resp.text}")
        sys.exit(1)


def report_storage_summary(report_filter):
    display_filter = ""
    if report_filter is not None:
        payload = {"filter_expression": report_filter}
        display_filter = "SEARCH: "+report_filter
        resp = url_POST("/reporting/virtualization-storage-summary-report/search", payload)
    else:
        resp = url_GET("/reporting/virtualization-storage-summary-report")
    if resp.status_code == 200:
        report_data = resp.json()['items']
        if report_data:
            tabular_report("DELPHIX Data Control Tower - Storage summary Report " + display_filter, report_data)
            return report_data
        else:
            print(f"\nNo Delphix Engines match search criteria.")
            return
    else:
        print(f"ERROR: Status = {resp.status_code} - {resp.text}")
        sys.exit(1)
