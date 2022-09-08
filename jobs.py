from helpers import *


# Job API

def job_status_by_id(job_id):
    resp = url_GET("/jobs/" + job_id)
    if resp.status_code == 200:
        return resp.json()
    else:
        print(f"ERROR: Status = {resp.status_code} - {resp.text}")
        sys.exit(1)


def job_monitor(job_id):
    job = {"status": ""}
    while job['status'] not in ['TIMEDOUT', 'CANCELED', 'FAILED', 'COMPLETED']:
        time.sleep(3)
        job = job_status_by_id(job_id)
    if job['status'] != 'COMPLETED':
        raise RuntimeError(f"Job {job['id']} failed {job['error_details']}")
    else:
        print(f"Job {job_id} COMPLETED - {job['update_time']}")


def job_list():
    resp = url_GET("/jobs?limit=50&sort=id")
    if resp.status_code == 200:
        report_data = resp.json()['items']
        if report_data:
            tabular_report("DELPHIX Data Control Tower - JOBS LIST", report_data)
            return report_data
        else:
            print(f"\nNo Jobs defined.")
            return
    else:
        print(f"ERROR: Status = {resp.status_code} - {resp.text}")
        sys.exit(1)


def job_search(job_filter):
    payload = ""
    display_filter = ""
    if job_filter is not None:
        payload = {"filter_expression": job_filter}
        display_filter = "SEARCH: "+job_filter
        resp = url_POST("/jobs/search", payload)
    else:
        resp = url_GET("/jobs")
    if resp.status_code == 200:
        report_data = resp.json()['items']
        if report_data:
            tabular_report("DELPHIX Data Control Tower - Job " + display_filter, report_data)
            return report_data
        else:
            print(f"\nNo Jobs match search criteria.")
            return
    else:
        print(f"ERROR: Status = {resp.status_code} - {resp.text}")
        sys.exit(1)
