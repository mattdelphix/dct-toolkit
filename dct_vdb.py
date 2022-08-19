import argparse
from vdbs import *

#TODO VDB report is wrong

parser = argparse.ArgumentParser(description = "Delphix DCT VDB operations")
subparser = parser.add_subparsers(dest='command')

parser.add_argument('--version', action='version', version='%(prog)s 1.0')

# define commands

list = subparser.add_parser('list')
create = subparser.add_parser('create')
search = subparser.add_parser('search')
delete = subparser.add_parser('delete')
view = subparser.add_parser('view')


# define view parms
view.add_argument('--id', type=str, required=True, help="VDB to be viewed")

# define delete parms
delete.add_argument('--id', type=str, required=True, help="VDB to be deleted")

# define search parms
search.add_argument('--name', type=str, required=True, help="VDB search string")
create.add_argument('--vdb_id', type=str, required=True, help="List of VDB IDs separated by commas")

# force help if no parms
args = parser.parse_args(args=None if sys.argv[1:] else ['--help'])

if args.command == 'list':
  print("Processing VDB list")
  rs = vdb_list()
  print(rs)

if args.command == 'view':
  print("Processing VDB view ID="+args.id)
  rs = vdb_by_id(args.id)
  print(rs)

if args.command == 'delete':
  print("Processing VDB delete ID="+args.id)
  rs = vdb_delete(args.id)
  print(rs)

if args.command == 'search':
  print("Processing VDB search name="+args.name)
  rs = vdb_search(args.name)
  print(rs)

if args.command == 'register':
  print("Processing VDB register ")
  rs = vdb_register(args.name, args.hostname, args.user, args.password, args.insecure_ssl, args.unsafe_ssl_hostname_check)
  print(rs)