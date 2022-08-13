from helpers import *

# Job API

def job_status_by_id(JOB_ID):
    resp = url_GET("/jobs/"+JOB_ID)
    if resp.status_code == 200:
        return json.loads(resp.text)
    else:
        print(f"ERROR: Status = {resp.status_code} - {resp.text}")
        sys.exit(1)
    return

def job_monitor(JOB_ID):
    job = {"status": ""}
    while job['status'] not in ['TIMEDOUT', 'CANCELED', 'FAILED', 'COMPLETED']:
        time.sleep(3)
        job = job_status_by_id(JOB_ID)
    if job['status'] != 'COMPLETED':
        raise RuntimeError(f"Job {job['id']} failed {job['error_details']}")
    else:
        print(f"Job {JOB_ID} COMPLETED - {job['update_time']}")
    return
