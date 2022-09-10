#
# dc_account
#

import argparse
from helpers import *


# Account functions
def account_create(base_url, client_id, first_name, last_name, email, username, password, tags):
    tags_dic = json.loads(tags)
    payload = {"generate_api_key": 'true', "api_client_id": client_id, "first_name": first_name, "last_name": last_name,
               "email": email,
               "username": username, "password": password, "tags": tags_dic}
    resp = url_POST(base_url, payload)
    if resp.status_code == 201:
        rsp = resp.json()
        print(f"Registered account with ID={rsp['id']}")
        return rsp
    else:
        print(f"ERROR: Status = {resp.status_code} - {resp.text}")
        sys.exit(1)


# Init
parser = argparse.ArgumentParser(description="Delphix DCT Account operations")
subparser = parser.add_subparsers(dest='command')

parser.add_argument('--version', action='version', version='%(prog)s 1.0')

# define commands
lst = subparser.add_parser('list')
create = subparser.add_parser('create')
delete = subparser.add_parser('delete')
search = subparser.add_parser('search')
view = subparser.add_parser('view')

# define create parms
create.add_argument('--client_id', type=str, required=True, help="Client_id name of the new Account")
create.add_argument('--first_name', type=str, required=True, help="First name of the new Account")
create.add_argument('--last_name', type=str, required=True, help="Last name of the new Account")
create.add_argument('--email', type=str, required=True, help="E-mail of the new Account")
create.add_argument('--username', type=str, required=True, help="Username of the new Account")
create.add_argument('--password', type=str, required=True, help="Password of the new Account")
create.add_argument('--tags', type=str, required=False,
                    help="Tags of the new Account in this format:  [{'key': 'key-1','value': 'value-1''},"
                         " {'key': 'key-2','value': 'value-2'}]")

# define delete parms
delete.add_argument('--id', type=str, required=True, help="Account ID to be deleted")

# define view parms
view.add_argument('--id', type=str, required=True, help="Account ID to be viewed")

# define list parms
lst.add_argument('--format', type=str, required=False, help="Type of output", choices=['json', 'report'])

# define search parms
search.add_argument('--filter', type=str, required=False, help="Account search string")
search.add_argument('--format', type=str, required=False, help="Type of output", choices=['json', 'report'])

# force help if no parms
args = parser.parse_args(args=None if sys.argv[1:] else ['--help'])

# Start processing
dct_base_url = "/management/accounts"

if args.command == 'view':
    rs = dct_view_by_id(dct_base_url, args.id)
    print(rs)

if args.command == 'search':
    rs = dct_search("Account List", dct_base_url, args.filter, "No Accounts match the search criteria.",
                    args.format)
    print(rs)

if args.command == 'list':
    rs = dct_search("Accounts List", dct_base_url, None, "No Accounts defined.", args.format)
    print(rs)

if args.command == 'create':
    print("Processing Accounts create")
    rs = account_create(dct_base_url, args.client_id, args.first_name, args.last_name, args.email, args.username,
                        args.password, args.tags)
    print(rs)

if args.command == 'delete':
    print("Processing Account delete ID=" + args.id)
    rs = dct_delete_by_id(dct_base_url, "Deleted Account", args.id)
