from helpers import *


# Job API


def job_monitor(job_id):
    job = {"status": ""}
    while job['status'] not in ['TIMEDOUT', 'CANCELED', 'FAILED', 'COMPLETED']:
        time.sleep(3)
        job = dct_view_by_id("/jobs", job_id)
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
