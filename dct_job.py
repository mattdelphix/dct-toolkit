import argparse
from jobs import *

# TODO job cancel not implemented
# TODO search should provide a generic filter as dct_report

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

# define monitor parms
monitor.add_argument('--id', type=str, required=True, help="job ID to be monitored")

# define search parms
search.add_argument('--filter', type=str, required=True, help="Job search string")

# force help if no parms
args = parser.parse_args(args=None if sys.argv[1:] else ['--help'])

if args.command == 'monitor':
    print("Monitor Job ID=" + args.id)
    rs = job_monitor(args.id)
    print(rs)

if args.command == 'view':
    rs = job_status_by_id(args.id)
    print(rs)

if args.command == 'cancel':
    print("Cancel Job ID=" + args.id)
    rs = job_cancel_by_id(args.id)
    print(rs)

if args.command == 'search':
    rs = job_search(args.filter)
    print(rs)

if args.command == 'list':
    rs = job_list()
    print(rs)
