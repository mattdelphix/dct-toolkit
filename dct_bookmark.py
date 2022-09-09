import argparse
from bookmarks import *

# TODO implement search, view, delete, list_vdbgroups


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

if args.command == 'view':
    print("Processing Bookmark view ID="+args.id)
    rs = dct_view_by_id("/bookmarks", args.id)
    print(rs)

if args.command == 'search':
    rs = dct_search("Bookmark List ", "/bookmarks", args.filter, "No Bookmarks match the search criteria.",
                    args.format)
    print(rs)

if args.command == 'list':
    rs = dct_search("Bookmarks List ", "/bookmarks", None, "No Bookmarks defined.", args.format)
    print(rs)

if args.command == 'create':
    print("Processing Bookmarks create")
    rs = bookmark_create(args.name, args.vdb_id, args.retention)
    print(rs)

if args.command == 'delete':
    print("Processing Bookmark delete ID="+args.id)
    rs = bookmark_delete(args.id)
    print(rs)


if args.command == 'vdbgroup_list':
    print("Processing VDBGroup list for Bookmark ID="+args.id)
    rs = bookmark_vdbgroup_list(args.id)
    print(rs)
