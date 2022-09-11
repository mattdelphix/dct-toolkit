#
# dct_vdbgroup
#

import argparse
from helpers import *

# VDBGroup functions
def vdbgroup_create(base_url, name, vdbg_id):
    # create VDB_ID list
    vdb_id_list = vdbg_id.split(",")
    # build payload
    payload = {"name": name, "vdb_ids": vdb_id_list}
    resp = url_POST(base_url, payload)
    if resp.status_code == 201:
        vdbg = resp.json()['vdb_group']
        print(f"Created VDBGroup with ID={vdbg['id']}")
        return vdbg
    else:
        print(f"ERROR: Status = {resp.status_code} - {resp.text}")
        sys.exit(1)

# Init
parser = argparse.ArgumentParser(description="Delphix DCT VDBgroup operations")
subparser = parser.add_subparsers(dest='command')

parser.add_argument('--version', action='version', version='%(prog)s 1.0')

# define commands

lst = subparser.add_parser('list')
search = subparser.add_parser('search')
delete = subparser.add_parser('delete')
create = subparser.add_parser('create')
view = subparser.add_parser('view')
bookmarks = subparser.add_parser('bookmarks')

# define view parms
view.add_argument('--id', type=str, required=True, help="VDBGroup full name or ID to be viewed")

# define list parms
lst.add_argument('--format', type=str, required=False, help="Type of output", choices=['json', 'report'])

# define delete parms
delete.add_argument('--id', type=str, required=True, help="VDBgroup to be deleted")

# define search parms
search.add_argument('--filter', type=str, required=False, help="VDBgroup search string")
search.add_argument('--format', type=str, required=False, help="Type of output", choices=['json', 'report'])

# define create parms
create.add_argument('--name', type=str, required=True, help="Name of the new VDBgroup")
create.add_argument('--vdb_id', type=str, required=True, help="List of VDB IDs separated by commas")

# define view parms
bookmarks.add_argument('--id', type=str, required=True, help="VDBGroup full name or ID to be viewed")
bookmarks.add_argument('--format', type=str, required=False, help="Type of output", choices=['json', 'report'])

# force help if no parms
args = parser.parse_args(args=None if sys.argv[1:] else ['--help'])

# Start processing
dct_base_url = "/vdb-groups"

if args.command == 'list':
    rs = dct_search("VDBGroup List ", dct_base_url, None, "No VDBGroups defined.", args.format)
    print(rs)

if args.command == 'view':
    rs = dct_view_by_id(dct_base_url, args.id)
    print(rs)

if args.command == 'delete':
    print("Processing VDBGroup delete ID=" + args.id)
    rs = dct_delete_by_id(dct_base_url, "Deleted VDBGroup", args.id)

if args.command == 'search':
    rs = dct_search("VDBGroups List ", dct_base_url, args.filter, "No VDBGroups match the search criteria.",
                    args.format)
    print(rs)

if args.command == 'create':
    print("Processing VDBGroup create ")
    rs = vdbgroup_create(dct_base_url, args.name, args.vdb_id)
    print(rs)

if args.command == 'bookmarks':
    rs = dct_list_by_id(dct_base_url, args.id, "/bookmarks", args.format)
    print(rs)