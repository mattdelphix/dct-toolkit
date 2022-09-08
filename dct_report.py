import argparse
from datetime import datetime

from reports import *

# TODO add sort and limit to all reports as parameter

parser = argparse.ArgumentParser(description = "Delphix DCT Reports")
subparser = parser.add_subparsers(dest='command')

parser.add_argument('--version', action='version', version='%(prog)s 1.0')

# define commands

api_usage = subparser.add_parser('api_usage')
dsource_usage = subparser.add_parser('dsource_usage')
vdb_inventory = subparser.add_parser('vdb_inventory')
storage_summary = subparser.add_parser('storage_summary')
product_info = subparser.add_parser('product_info')

# Get current date time in ISO FORMAT
#TODO to be implemented logic to set current time as API end timestamp
end_time = datetime.now().isoformat()
#print(end_time)

# define api_usage parms
api_usage.add_argument('--begin', type=str, required=False, help="begin timestamp for report", default='2020-01-01T15:00:00-00:00')
api_usage.add_argument('--end', type=str, required=False, help="end timestamp for report", default='2099-01-01T15:00:00-00:00')

# define vdb_inventory parms
vdb_inventory.add_argument('--filter', type=str, required=False, help="VDB search string")

# define storage_summary parms
storage_summary.add_argument('--filter', type=str, required=False, help="Storage Summary search string")

# define storage_summary parms
dsource_usage.add_argument('--filter', type=str, required=False, help="DSource Usage search string")

# force help if no parms
args = parser.parse_args(args=None if sys.argv[1:] else ['--help'])

if args.command == 'api_usage':
    rs = report_api_usage(args.begin, args.end)

if args.command == 'vdb_inventory':
    rs = report_vdb_inventory(args.filter)

if args.command == 'dsource_usage':
    rs = report_dsource_usage(args.filter)

if args.command == 'storage_summary':
    rs = report_storage_summary(args.filter)

if args.command == 'product_info':
    rs = report_product_info()


