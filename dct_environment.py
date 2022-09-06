import argparse
from environments import *

# TODO Environment delete to be tested
# TODO add job monitoring where needed

parser = argparse.ArgumentParser(description='Delphix DCT Environment operations')
subparser = parser.add_subparsers(dest='command')

parser.add_argument('--version', action='version', version='%(prog)s 1.0')

# define commands

lst = subparser.add_parser('list')
search = subparser.add_parser('search')
view = subparser.add_parser('view')
delete = subparser.add_parser('delete')
disable = subparser.add_parser('disable')
enable = subparser.add_parser('enable')
refresh = subparser.add_parser('refresh')


# define view parms
view.add_argument('--id', type=str, required=True, help="Environment ID to be viewed")

# define enable parms
enable.add_argument('--id', type=str, required=True, help="Environment ID to be enabled")

# define disable parms
disable.add_argument('--id', type=str, required=True, help="Environment ID to be disabled")

# define refresh parms
refresh.add_argument('--id', type=str, required=True, help="Environment ID to be refreshed")

# define delete parms
delete.add_argument('--id', type=str, required=True, help="Environment ID to be deleted")

# define search parms
search.add_argument('--name', type=str, required=True, help="Environment search string")

# force help if no parms
args = parser.parse_args(args=None if sys.argv[1:] else ['--help'])

if args.command == 'list':
    print("Processing Environment list")
    rs = environment_list()
    print(rs)

if args.command == 'view':
    print("Processing Environment view ID="+args.id)
    rs = environment_by_id(args.id)
    print(rs)

if args.command == 'delete':
    print("Processing Environment delete ID="+args.id)
    rs = environment_delete(args.id)
    print(rs)

if args.command == 'search':
    print("Processing Environment search name="+args.name)
    rs = environment_search(args.name)
    print(rs)

if args.command == 'refresh':
    print("Processing Environment refresh ID="+args.id)
    rs = environment_operation(args.id, args.command)
    print(rs)

if args.command == 'enable':
    print("Processing Environment enable ID="+args.id)
    rs = environment_operation(args.id, args.command)
    print(rs)

if args.command == 'disable':
    print("Processing Environment disable ID="+args.id)
    rs = environment_operation(args.id, args.command)
    print(rs)
