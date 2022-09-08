import argparse
from vdbgroups import *

#TODO implement
# UPDATE
# refresh
# rollback
# TODO search should provide a generic filter as dct_report

parser = argparse.ArgumentParser(description = "Delphix DCT VDBgroup operations")
subparser = parser.add_subparsers(dest='command')

parser.add_argument('--version', action='version', version='%(prog)s 1.0')

# define commands

list = subparser.add_parser('list')
search = subparser.add_parser('search')
delete = subparser.add_parser('delete')
create = subparser.add_parser('create')
view = subparser.add_parser('view')
bookmarks = subparser.add_parser('bookmarks')

# define view parms
view.add_argument('--id', type=str, required=True, help="VDBGroup full name or ID to be viewed")

# define delete parms
delete.add_argument('--id', type=str, required=True, help="VDBgroup to be deleted")

# define search parms
search.add_argument('--name', type=str, required=True, help="VDBgroup search string")

# define create parms
create.add_argument('--name', type=str, required=True, help="Name of the new VDBgroupT")
create.add_argument('--vdb_id', type=str, required=True, help="List of VDB IDs separated by commas")

# define view parms
bookmarks.add_argument('--id', type=str, required=True, help="VDBGroup full name or ID to be viewed")

# force help if no parms
args = parser.parse_args(args=None if sys.argv[1:] else ['--help'])

if args.command == 'list':
  print("Processing VDBGroup list")
  rs = vdbgroup_list()
  print(rs)

if args.command == 'view':
  rs = vdbgroup_by_id(args.id)
  print(rs)

if args.command == 'delete':
  print("Processing VDBGroup delete ID="+args.id)
  rs = vdbgroup_delete(args.id)
  print(rs)

if args.command == 'search':
  print("Processing VDBGroup search name="+args.name)
  rs = vdbgroup_search(args.name)
  print(rs)

if args.command == 'create':
  print("Processing VDBGroup create ")
  rs = vdbgroup_create(args.name, args.vdb_id)
  print(rs)

if args.command == 'bookmarks':
  print("Processing VDBGroup Bookmarks ID="+args.id)
  rs = vdbgroup_bookmarks(args.id)
  print(rs)
