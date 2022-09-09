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
