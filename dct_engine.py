import argparse
from engines import *

# TODO search should provide a generic filter as dct_report

parser = argparse.ArgumentParser(description="Delphix DCT Engine operations")
subparser = parser.add_subparsers(dest='command')

parser.add_argument('--version', action='version', version='%(prog)s 1.0')

# define commands

lst = subparser.add_parser('list')
search = subparser.add_parser('search')
delete = subparser.add_parser('delete')
register = subparser.add_parser('register')
view = subparser.add_parser('view')

# define view parms
view.add_argument('--id', type=str, required=True, help="engine UUID to be viewed")

# define delete parms
delete.add_argument('--id', type=str, required=True, help="engine UUID to be deleted")

# define search parms
search.add_argument('--name', type=str, required=True, help="engine UUID search string")

# define register parms
register.add_argument('--name', type=str, required=True, help="Name used to refer to the engine in DCT")
register.add_argument('--hostname', type=str, required=True, help="hostname or ip address")
register.add_argument('--user', type=str, required=True, help="admin user")
register.add_argument('--password', type=str, required=True, help="admin password")
register.add_argument('--insecure_ssl', type=str, required=False, help="is SSL secure?", default=True)
register.add_argument('--unsafe_ssl_hostname_check', required=False, type=str, help="check SSL connection",
                      default=True)

# force help if no parms
args = parser.parse_args(args=None if sys.argv[1:] else ['--help'])

if args.command == 'list':
    print("Processing Engine list")
    rs = engine_list()
    print(rs)

if args.command == 'view':
    rs = engine_by_id(args.id)
    print(rs)

if args.command == 'delete':
    print("Processing Engine delete ID=" + args.id)
    rs = engine_delete(args.id)
    print(rs)

if args.command == 'search':
    print("Processing Engine search name=" + args.name)
    rs = engine_search(args.name)
    print(rs)

if args.command == 'register':
    print("Processing Engine register ")
    rs = engine_register(args.name, args.hostname, args.user, args.password, args.insecure_ssl,
                         args.unsafe_ssl_hostname_check)
    print(rs)
