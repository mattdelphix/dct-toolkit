#
# dct_vdb
#

import argparse
from helpers import *

# VDB functions
def vdb_operation(base_url, vdb_id, ops):
    ops = ops.lower()
    if not any(x in ops for x in ["enable", "disable", "stop", "start"]):
        print("Error: Wrong operation on VDB: "+ops)
        sys.exit(1)
    payload =""
    if ops == "enable":
        payload = {"attempt_start": "true"}
    if ops == "disable":
        payload = {"attempt_cleanup": "true"}
    resp = url_POST(base_url+urllib.parse.quote(vdb_id)+"/"+ops, payload)
    if resp.status_code == 200:
        return json.loads(resp.text)
    else:
        print(f"ERROR: Status = {resp.status_code} - {resp.text}")
        sys.exit(1)

# Init
parser = argparse.ArgumentParser(description='Delphix DCT VDB operations')
subparser = parser.add_subparsers(dest='command')

parser.add_argument('--version', action='version', version='%(prog)s 1.0')

# define commands

lst = subparser.add_parser('list')
create = subparser.add_parser('create')
search = subparser.add_parser('search')
delete = subparser.add_parser('delete')
view = subparser.add_parser('view')
disable = subparser.add_parser('disable')
enable = subparser.add_parser('enable')
stop = subparser.add_parser('stop')
start = subparser.add_parser('start')


# define view parms
view.add_argument('--id', type=str, required=True, help="VDB ID to be viewed")

# define list parms
lst.add_argument('--format', type=str, required=False, help="Type of output",  choices=['json', 'report'])

# define enable parms
enable.add_argument('--id', type=str, required=True, help="VDB ID to be enabled")

# define disable parms
disable.add_argument('--id', type=str, required=True, help="VDB ID to be disabled")

# define stop parms
stop.add_argument('--id', type=str, required=True, help="VDB ID to be stopped")

# define start parms
start.add_argument('--id', type=str, required=True, help="VDB ID to be started")

# define delete parms
delete.add_argument('--id', type=str, required=True, help="VDB ID to be deleted")

# define search parms
search.add_argument('--filter', type=str, required=False, help="VDB search string")
search.add_argument('--format', type=str, required=False, help="Type of output",  choices=['json', 'report'])

# force help if no parms
args = parser.parse_args(args=None if sys.argv[1:] else ['--help'])

# Start processing
dct_base_url = "/vdbs"

if args.command == 'list':
    rs = dct_search("VDB List ", dct_base_url, None, "No VDBs defined.", args.format)
    print(rs)

if args.command == 'view':
    rs = dct_view_by_id(dct_base_url, args.id)
    print(rs)

if args.command == 'delete':
    print("Processing VDB delete ID=" + args.id)
    rs = dct_delete_by_id(dct_base_url, "Deleted VDB", args.id)

if args.command == 'search':
    rs = dct_search("VDB List ", dct_base_url, args.filter, "No VDBs match the search criteria.",
                    args.format)
    print(rs)

if args.command == 'enable':
    print("Processing VDB enable ID="+args.id)
    rs = vdb_operation(dct_base_url, args.id, args.command)
    print(rs)

if args.command == 'disable':
    print("Processing VDB disable ID="+args.id)
    rs = vdb_operation(dct_base_url, args.id, args.command)
    print(rs)

if args.command == 'stop':
    print("Processing VDB stop ID="+args.id)
    rs = vdb_operation(dct_base_url, args.id, args.command)
    print(rs)

if args.command == 'start':
    print("Processing VDB start ID="+args.id)
    rs = vdb_operation(dct_base_url, args.id, args.command)
    print(rs)
