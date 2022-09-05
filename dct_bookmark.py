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

# define create parms
create.add_argument('--name', type=str, required=True, help="Name of the new BookmarkT")
create.add_argument('--vdb_id', type=str, required=True, help="List of VDB IDs separated by commas")
create.add_argument('--retention', type=int, required=False, help="Bookmark retention period in days", default=365)

# define delete parms
delete.add_argument('--id', type=str, required=True, help="Bookmark ID to be deleted")

# force help if no parms
args = parser.parse_args(args=None if sys.argv[1:] else ['--help'])

if args.command == 'list':
    print("Processing Bookmarks list")
    rs = bookmark_list()
    print(rs)

if args.command == 'create':
    print("Processing Bookmarks create")
    rs = bookmark_create(args.name, args.vdb_id, args.retention)
    print(rs)

if args.command == 'delete':
    print("Processing Bookmark delete ID="+args.id)
    rs = bookmark_delete(args.id)
    print(rs)
