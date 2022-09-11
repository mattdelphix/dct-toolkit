#
# dct_engine
#

import argparse
from helpers import *

# Engine functions
def engine_register(base_url, name, hostname, user, password, insecure_ssl, unsafe_ssl):
    # TODO add hashicorp, trustore and tags
    payload = {"name": name, "hostname": hostname, "username": user, "password": password, "insecure_ssl": insecure_ssl,
               "unsafe_ssl_hostname_check": unsafe_ssl}
    resp = url_POST(base_url, payload)
    if resp.status_code == 201:
        print(f"Registered engine with ID={resp['id']}")
        return resp.json()
    else:
        print(f"ERROR: Status = {resp.status_code} - {resp.text}")
        sys.exit(1)

# Init
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

# define list parms
lst.add_argument('--format', type=str, required=False, help="Type of output",  choices=['json', 'report'])

# define delete parms
delete.add_argument('--id', type=str, required=True, help="engine UUID to be deleted")

# define search parms
search.add_argument('--filter', type=str, required=False, help="Engine search string")
search.add_argument('--format', type=str, required=False, help="Type of output",  choices=['json', 'report'])

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


# Start processing
dct_base_url = "/management/engines"

if args.command == 'list':
    rs = dct_search("Engine List", dct_base_url, None, "No Engines defined.", args.format)
    print(rs)

if args.command == 'view':
    rs = dct_view_by_id(dct_base_url, args.id)
    print(rs)

if args.command == 'delete':
    print("Processing Engine delete ID=" + args.id)
    rs = dct_delete_by_id(dct_base_url, "Deleted Engine", args.id)

if args.command == 'search':
    rs = dct_search("Engine List", dct_base_url, args.filter, "No Engines match the search criteria.",
                    args.format)
    print(rs)

if args.command == 'register':
    print("Processing Engine register ")
    rs = engine_register(dct_base_url, args.name, args.hostname, args.user, args.password, args.insecure_ssl,
                         args.unsafe_ssl_hostname_check)
    print(rs)
