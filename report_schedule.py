#
# dct_report_schedule
#

import argparse
from helpers import *

# TODO add sort and limit to all reports as parameter

# Report Schedule functions


# Init
parser = argparse.ArgumentParser(description="Delphix DCT Report Schedule")
subparser = parser.add_subparsers(dest='command')

parser.add_argument('--version', action='version', version='%(prog)s 1.0')

# define commands
lst = subparser.add_parser('list')
delete = subparser.add_parser('delete')
view = subparser.add_parser('view')


# define view parms
view.add_argument('--id', type=str, required=True, help="Report Schedule ID to be viewed")

# define list parms
lst.add_argument('--format', type=str, required=False, help="Type of output",  choices=['json', 'report'])

# define delete parms
delete.add_argument('--id', type=str, required=True, help="Report Schedule ID to be deleted")

# force help if no parms
args = parser.parse_args(args=None if sys.argv[1:] else ['--help'])

# Start processing
dct_base_url = "/reporting/schedule"

if args.command == 'list':
    rs = dct_search("Report Schedule List ", dct_base_url, None, "No Report Schedules defined.", args.format)
    print(rs)

if args.command == 'delete':
    print("Processing Report Schedule delete ID=" + args.id)
    rs = dct_delete_by_id(dct_base_url, "Deleted Report Schedule", args.id)

if args.command == 'view':
    rs = dct_view_by_id(dct_base_url, args.id)
    print(rs)
