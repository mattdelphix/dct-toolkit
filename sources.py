from helpers import *


# Source API


def source_list():
    resp = url_GET("/sources?limit=50&sort=id")
    if resp.status_code == 200:
        report_data = resp.json()['items']
        if report_data:
            tabular_report("DELPHIX Data Control Tower - SOURCES LIST", report_data)
            return report_data
        else:
            print(f"\nNo Sources defined.")
            return
    else:
        print(f"ERROR: Status = {resp.status_code} - {resp.text}")
        sys.exit(1)

