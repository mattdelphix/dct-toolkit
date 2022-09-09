import argparse
from vdbgroups import *

# TODO implement
# UPDATE
# refresh
# rollback
# TODO search should provide a generic filter as dct_report

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

# force help if no parms
args = parser.parse_args(args=None if sys.argv[1:] else ['--help'])

if args.command == 'list':
    rs = dct_search("VDBGroup List ", "/vdb-groups", None, "No VDBGroups defined.", args.format)
    print(rs)

if args.command == 'view':
    rs = dct_view_by_id("/vdb-groups", args.id)
    print(rs)

if args.command == 'delete':
    print("Processing VDBGroup delete ID=" + args.id)
    rs = vdbgroup_delete(args.id)
    print(rs)

if args.command == 'search':
    rs = dct_search("VDBGroups List ", "/vdb-groups", args.filter, "No VDBgroups match the search criteria.",
                    args.format)
    print(rs)

if args.command == 'create':
    print("Processing VDBGroup create ")
    rs = vdbgroup_create(args.name, args.vdb_id)
    print(rs)

if args.command == 'bookmarks':
    print("Processing VDBGroup Bookmarks ID=" + args.id)
    rs = vdbgroup_bookmarks(args.id)
    print(rs)
