from helpers import *


# Job API

def job_status_by_id(job_id):
    resp = url_GET("/jobs/" + job_id)
    if resp.status_code == 200:
        return json.loads(resp.text)
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
