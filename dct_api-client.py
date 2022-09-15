#
# dct_api_client
#

import argparse
from helpers import *


# Api-client functions
def api_client_create(base_url, client_id, first_name, last_name, email, username, password, tags):
    tags_dic = json.loads(tags)
    payload = {"generate_api_key": 'true', "api_client_id": client_id, "first_name": first_name, "last_name": last_name,
               "email": email,
               "username": username, "password": password, "tags": tags_dic}
    resp = url_POST(base_url, payload)
    if resp.status_code == 201:
        rsp = resp.json()
        print(f"Registered API-client with ID={rsp['id']}")
        return rsp
    else:
        print(f"ERROR: Status = {resp.status_code} - {resp.text}")
        sys.exit(1)


def api_client_update(base_url, client_id, first_name, last_name, email, username, password, tags):
    tags_dic = json.loads(tags)
    payload = {"generate_api_key": 'true', "api_client_id": client_id, "first_name": first_name, "last_name": last_name,
               "email": email,
               "username": username, "password": password, "tags": tags_dic}
    resp = url_POST(base_url, payload)
    if resp.status_code == 200:
        rsp = resp.json()
        print(f"Updated API-client with ID={rsp['id']}")
        return rsp
    else:
        print(f"ERROR: Status = {resp.status_code} - {resp.text}")
        sys.exit(1)


# Init
parser = argparse.ArgumentParser(description="Delphix DCT API-client operations")
subparser = parser.add_subparsers(dest='command')

parser.add_argument('--version', action='version', version='%(prog)s 1.0')

# define commands
lst = subparser.add_parser('list')
create = subparser.add_parser('create')
delete = subparser.add_parser('delete')
view = subparser.add_parser('view')
updt = subparser.add_parser('update')

# define create parms
create.add_argument('--client_id', type=str, required=True, help="Client_id name of the new API-clint")
create.add_argument('--first_name', type=str, required=True, help="First name of the new API-client")
create.add_argument('--last_name', type=str, required=True, help="Last name of the new API-client")
create.add_argument('--email', type=str, required=True, help="E-mail of the new API-client")
create.add_argument('--username', type=str, required=True, help="Username of the new API-client")
create.add_argument('--password', type=str, required=True, help="Password of the new API-client")
create.add_argument('--tags', type=str, required=False,
                    help="Tags of the new API-client in this format:  [{'key': 'key-1','value': 'value-1''},"
                         " {'key': 'key-2','value': 'value-2'}]")
# define update parms
updt.add_argument('--client_id', type=str, required=False, help="Client_id name of the new API-client")
updt.add_argument('--first_name', type=str, required=False, help="First name of the new API-client")
updt.add_argument('--last_name', type=str, required=False, help="Last name of the new API-client")
updt.add_argument('--email', type=str, required=False, help="E-mail of the new API-client")
updt.add_argument('--username', type=str, required=False, help="Username of the new API-client")
updt.add_argument('--password', type=str, required=False, help="Password of the new API-client")

# define delete parms
delete.add_argument('--id', type=str, required=True, help="API-client ID to be deleted")

# define view parms
view.add_argument('--id', type=str, required=True, help="API-client ID to be viewed")

# define list parms
lst.add_argument('--format', type=str, required=False, help="Type of output", choices=['json', 'report'])

# force help if no parms
args = parser.parse_args(args=None if sys.argv[1:] else ['--help'])

# Start processing
dct_base_url = "/management/api-clients"

if args.command == 'view':
    rs = dct_view_by_id(dct_base_url, args.id)
    print(rs)

if args.command == 'list':
    rs = dct_search("API-clients List", dct_base_url, None, "No API-clients defined.", args.format)
    print(rs)

if args.command == 'create':
    print("Processing API-clients create")
    rs = api_client_create(dct_base_url, args.client_id, args.first_name, args.last_name, args.email, args.username,
                           args.password, args.tags)
    print(rs)

if args.command == 'update':
    print("Processing API-client update")
    rs = api_client_update(dct_base_url, args.client_id, args.first_name, args.last_name, args.email, args.username,
                           args.password, args.tags)
    print(rs)

if args.command == 'delete':
    print("Processing API-client delete ID=" + args.id)
    rs = dct_delete_by_id(dct_base_url, "Deleted API-client", args.id)
