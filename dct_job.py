#
# dct_job
#

import argparse
from helpers import *

# TODO job cancel not implemented

# Job functions
def job_monitor(job_id):
    job = {"status": ""}
    while job['status'] not in ['TIMEDOUT', 'CANCELED', 'FAILED', 'COMPLETED']:
        time.sleep(3)
        job = dct_view_by_id("/jobs", job_id)
    if job['status'] != 'COMPLETED':
        raise RuntimeError(f"Job {job['id']} failed {job['error_details']}")
    else:
        print(f"Job {job_id} COMPLETED - {job['update_time']}")

# Init
parser = argparse.ArgumentParser(description="Delphix DCT Job operations")
subparser = parser.add_subparsers(dest='command')

parser.add_argument('--version', action='version', version='%(prog)s 1.0')

# define commands

view = subparser.add_parser('view')
monitor = subparser.add_parser('monitor')
cancel = subparser.add_parser('cancel')
search = subparser.add_parser('search')
lst = subparser.add_parser('list')


# define view parms
view.add_argument('--id', type=str, required=True, help="job ID to be viewed")

# define list parms
lst.add_argument('--format', type=str, required=False, help="Type of output",  choices=['json', 'report'])

# define monitor parms
monitor.add_argument('--id', type=str, required=True, help="job ID to be monitored")

# define search parms
search.add_argument('--filter', type=str, required=False, help="Job search string")
search.add_argument('--format', type=str, required=False, help="Type of output",  choices=['json', 'report'])

# force help if no parms
args = parser.parse_args(args=None if sys.argv[1:] else ['--help'])


# Start processing
dct_base_url = "/jobs"

if args.command == 'monitor':
    print("Monitor Job ID=" + args.id)
    rs = job_monitor(args.id)
    print(rs)

if args.command == 'view':
    rs = dct_view_by_id(dct_base_url, args.id)
    print(rs)

if args.command == 'cancel':
    print("Cancel Job ID=" + args.id)
    rs = job_cancel_by_id(args.id)
    print(rs)

if args.command == 'search':
    rs = dct_search("Job List ", dct_base_url, args.filter, "No Jobs match the search criteria.",
                    args.format)
    print(rs)

if args.command == 'list':
    rs = dct_search("Job List ", dct_base_url, None, "No Jobs defined.", args.format)
    print(rs)
