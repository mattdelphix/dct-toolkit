#
# dc_account
#

import argparse
from helpers import *


# Bookmark functions
def bookmark_create(base_url, name, bookmark_id, retention):
    # create VDB_ID list
    vdb_id_list = bookmark_id.split(",")
    # build payload
    payload = {"name": name, "vdb_ids": vdb_id_list, "retention": retention}
    resp = url_POST(base_url, payload)
    if resp.status_code == 200:
        bookm = resp.json()
        print(f"Created Bookmark with ID={name}, Retention={retention}")
        return bookm
    else:
        print(f"ERROR: Status = {resp.status_code} - {resp.text}")
        sys.exit(1)

# Init
parser = argparse.ArgumentParser(description="Delphix DCT Bookmark operations")
subparser = parser.add_subparsers(dest='command')

parser.add_argument('--version', action='version', version='%(prog)s 1.0')

# define commands

lst = subparser.add_parser('list')
create = subparser.add_parser('create')
delete = subparser.add_parser('delete')
search = subparser.add_parser('search')
view = subparser.add_parser('view')
vdbgroup_list = subparser.add_parser('vdbgroup_list')

# define create parms
create.add_argument('--name', type=str, required=True, help="Name of the new Bookmark")
create.add_argument('--vdb_id', type=str, required=True, help="List of VDB IDs separated by commas")
create.add_argument('--retention', type=int, required=False, help="Bookmark retention period in days", default=365)

# define delete parms
delete.add_argument('--id', type=str, required=True, help="Bookmark ID to be deleted")

# define view parms
view.add_argument('--id', type=str, required=True, help="Bookmark ID to be viewed")

# define list parms
lst.add_argument('--format', type=str, required=False, help="Type of output",  choices=['json', 'report'])

# define search parms
search.add_argument('--filter', type=str, required=False, help="Bookmark search string")
search.add_argument('--format', type=str, required=False, help="Type of output",  choices=['json', 'report'])

# define vdbgroup_list parms
vdbgroup_list.add_argument('--id', type=str, required=True, help="Bookmark ID for VDBGroup list")

# force help if no parms
args = parser.parse_args(args=None if sys.argv[1:] else ['--help'])

# Start processing
dct_base_url = "/bookmarks"

if args.command == 'view':
    rs = dct_view_by_id(dct_base_url, args.id)
    print(rs)

if args.command == 'search':
    rs = dct_search("Bookmark List", dct_base_url, args.filter, "No Bookmarks match the search criteria.",
                    args.format)
    print(rs)

if args.command == 'list':
    rs = dct_search("Bookmarks List", dct_base_url, None, "No Bookmarks defined.", args.format)
    print(rs)

if args.command == 'create':
    print("Processing Bookmarks create")
    rs = bookmark_create(dct_base_url, args.name, args.vdb_id, args.retention)
    print(rs)

if args.command == 'delete':
    print("Processing Bookmark delete ID=" + args.id)
    rs = dct_delete_by_id(dct_base_url, "Deleted Bookmark", args.id)

if args.command == 'vdbgroup_list':
    rs = dct_list_by_id(dct_base_url, args.id, "/vdb-groups", args.format)
    print(rs)