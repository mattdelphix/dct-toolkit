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
user_list = subparser.add_parser('user_list')
tag_list = subparser.add_parser('tag_list')

# define list parms
lst.add_argument('--format', type=str, required=False, help="Type of output",  choices=['json', 'report'])

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
search.add_argument('--filter', type=str, required=True, help="Environment search string")
search.add_argument('--format', type=str, required=False, help="Type of output",  choices=['json', 'report'])

# define user_list parms
user_list.add_argument('--id', type=str, required=True, help="Environment ID to be viewed")
user_list.add_argument('--format', type=str, required=False, help="Type of output",  choices=['json', 'report'])

# define tag_list parms
tag_list.add_argument('--id', type=str, required=True, help="Environment ID to be viewed")
tag_list.add_argument('--format', type=str, required=False, help="Type of output",  choices=['json', 'report'])

# force help if no parms
args = parser.parse_args(args=None if sys.argv[1:] else ['--help'])


# if args.command == 'list':
#    print("Processing Environment list")
#    rs = environment_list()
#    print(rs)

if args.command == 'list':
    rs = dct_search("Environment List ", "/environments", None, "No Environments defined.", args.format)
    print(rs)

if args.command == 'view':
    rs = dct_view_by_id("/environments", args.id)
    print(rs)

if args.command == 'user_list':
    rs = dct_list_by_id("/environments", args.id, "/users", args.format)
    print(rs)

if args.command == 'tag_list':
    rs = dct_list_by_id("/environments", args.id, "/tags", args.format)
    print(rs)

if args.command == 'delete':
    print("Processing Environment delete ID="+args.id)
    rs = environment_delete(args.id)
    print(rs)

if args.command == 'search':
    rs = dct_search("Environment List ", "/environments", args.filter, "No Environments match the search criteria.",
                    args.format)
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
