#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Copyright (c) 2022 by Delphix. All rights reserved.
#
# Author  : Matteo Ferrari, Ruben Catarrunas
# Date    : September 2022
import cfg
from helpers import *


# Account functions
def account_create(base_url, client_id, first_name, last_name, email, username, password, tags):
    if tags is None:
        payload = {"generate_api_key": 'true', "api_client_id": client_id, "first_name": first_name,
                   "last_name": last_name, "email": email, "username": username, "password": password}
    else:
        payload = {"generate_api_key": 'true', "api_client_id": client_id, "first_name": first_name,
                   "last_name": last_name, "email": email, "username": username, "password": password, "tags": tags}

    resp = url_POST(base_url, payload)
    if resp.status_code == 201:
        rsp = resp.json()
        print(f"Registered account with ID={rsp['id']}")
        return rsp
    else:
        dct_print_error(resp)
        sys.exit(1)


def account_update(base_url, account_id, client_id, first_name, last_name, email, username):
    payload = {"api_client_id": client_id, "first_name": first_name, "last_name": last_name, "email": email,
               "username": username}

    resp = url_PUT(base_url + "/" + urllib.parse.quote(account_id), payload)
    if resp.status_code == 200:
        rsp = resp.json()
        print("Updated Account" + " - ID=" + account_id)
        return rsp
    else:
        dct_print_error(resp)
        sys.exit(1)

def account_view(base_url, account_id, dct_output="json"):
    # enhanced search that filters by ID or username
    if account_id.isnumeric():
        args_filter = "id eq '" + str(account_id) + "'"
    else:
        args_filter = " username eq '" + str(account_id) + "'"
    rs = dct_search("", base_url, args_filter, "No accounts match the search criteria."),
    return rs

def password_policy_update(base_url, is_enabled, min_length, reuse_disallow_limit, digit, uppercase_letter,
                           lowercase_letter, special_character, disallow_username_as_password):
    payload = {"enabled": is_enabled, "min_length": min_length, "reuse_disallow_limit": reuse_disallow_limit,
               "digit": digit, "uppercase_letter": uppercase_letter, "lowercase_letter": lowercase_letter,
               "special_character": special_character, "disallow_username_as_password": disallow_username_as_password}

    resp = url_PATCH(base_url, payload)
    if resp.status_code == 200:
        rsp = resp.json()
        print("Password policy updated")
        return rsp
    else:
        dct_print_error(resp)
        sys.exit(1)


# Init
parser = argparse.ArgumentParser(description="Delphix DCT Account operations")
subparser = parser.add_subparsers(dest='command')

parser.add_argument('--version', action='version', version='%(prog)s Version '+cfg.version)
parser.add_argument('--config', type=str, required=False, help="Config file")
parser.add_argument('--debug', type=int, required=False, help="Debug level [0-2]",choices=[0,1,2])

# define commands
lst = subparser.add_parser('list')
create = subparser.add_parser('create')
delete = subparser.add_parser('delete')
search = subparser.add_parser('search')
view = subparser.add_parser('view')
updt = subparser.add_parser('update')
tags = subparser.add_parser('tag_list')
pwd_reset = subparser.add_parser('password_reset')
tag_create = subparser.add_parser('tag_create')
tag_delete = subparser.add_parser('tag_delete')
tag_delete_all = subparser.add_parser('tag_delete_all')
lst_pwd_policy = subparser.add_parser('list_pwd_policy')
updt_pwd_policy = subparser.add_parser('update_pwd_policy')

# define create params
create.add_argument('--client_id', type=str, required=True, help="Client_id name of the new Account")
create.add_argument('--first_name', type=str, required=False, help="First name of the new Account")
create.add_argument('--last_name', type=str, required=False, help="Last name of the new Account")
create.add_argument('--email', type=str, required=False, help="E-mail of the new Account")
create.add_argument('--username', type=str, required=True, help="Username of the new Account")
create.add_argument('--password', type=str, required=False, help="Password of the new Account")
create.add_argument('--tags', nargs='*', type=str, required=True, action=dct_parsetags,
                    help="Tags of the DSource in this format:  key=value key=value")

# define update params
updt.add_argument('--id', type=str, required=True, help="Account ID to be updated")
updt.add_argument('--client_id', type=str, required=False, help="Client_id name of the Account to be updated")
updt.add_argument('--first_name', type=str, required=False, help="First name of the Account to be updated")
updt.add_argument('--last_name', type=str, required=False, help="Last name of the Account to be updated")
updt.add_argument('--email', type=str, required=False, help="E-mail of the Account to be updated")
updt.add_argument('--username', type=str, required=False, help="Username of the Account to be updated")

# define delete params
delete.add_argument('--id', type=str, required=True, help="Account ID to be deleted")

# define view params
view.add_argument('--id', type=str, required=True, help="Account ID or Name to be viewed")

# define tag_list params
tags.add_argument('--id', type=str, required=True, help="Account ID or Name to be viewed")
tags.add_argument('--format', type=str, required=False, help="Type of output", choices=['json', 'report','id'])

# define list params
lst.add_argument('--format', type=str, required=False, help="Type of output", choices=['json', 'report','id'])

# define search params
search.add_argument('--filter', type=str, required=False, help="Account search string")
search.add_argument('--format', type=str, required=False, help="Type of output", choices=['json', 'report','id'])

# define password_reset params
pwd_reset.add_argument('--id', type=str, required=True, help="Account ID to have pwd reset")
pwd_reset.add_argument('--old_password', type=str, required=True, help="Existing Password of the Account")
pwd_reset.add_argument('--new_password', type=str, required=True, help="New Password of the Account")

# define tag_create params
tag_create.add_argument('--id', type=str, required=True, help="Account ID to add tags to")
tag_create.add_argument('--tags', nargs='*', type=str, required=True, action=dct_parsetags,
                        help="Tags of the DSource in this format:  key=value key=value")

# define tag_delete params
tag_delete.add_argument('--id', type=str, required=True, help="Account ID to delete tags from")
tag_delete.add_argument('--key', type=str, required=True, help="Tags key of existing tag")

# define tag_delete_all params
tag_delete_all.add_argument('--id', type=str, required=True, help="Account ID to delete tags from")

# define lst_pwd_policy params
lst_pwd_policy.add_argument('--format', type=str, required=False, help="Type of output", choices=['json', 'report','id'])

# define updt_pwd_policy params
updt_pwd_policy.add_argument('--enabled', type=str, required=True, help="Status of password policy",
                             choices=['true', 'false'])
updt_pwd_policy.add_argument('--min_length', type=int, required=True, help="Minimum length password should have",
                             choices=range(1, 50))
updt_pwd_policy.add_argument('--reuse_disallow_limit', type=int, required=True, choices=range(1, 50),
                             help="Times password has to be different in order to be reused")
updt_pwd_policy.add_argument('--digit', type=str, required=True, help="Has to contain at least one number",
                             choices=['true', 'false'])
updt_pwd_policy.add_argument('--uppercase_letter', type=str, required=True,
                             help="Has to contain at least one Uppercase", choices=['true', 'false'])
updt_pwd_policy.add_argument('--lowercase_letter', type=str, required=True,
                             help="Has to contain at least one Lowercase", choices=['true', 'false'])
updt_pwd_policy.add_argument('--special_character', type=str, required=True,
                             help="Has to contain at least one special character", choices=['true', 'false'])
updt_pwd_policy.add_argument('--disallow_username_as_password', type=str, required=True,
                             help="Username cannot be used as password", choices=['true', 'false'])

# force help if no params
args = parser.parse_args(args=None if sys.argv[1:] else ['--help'])

# Start processing
args = parser.parse_args()
# Read config
dct_read_config(args.config)
if args.debug:
    cfg.level = args.debug
# force help if no command
if dct_check_empty_command(args):
    parser.print_help()
    sys.exit(1)

dct_base_url = "/management/accounts"

if args.command == 'view':
    rs = account_view(dct_base_url, args.id)

if args.command == 'search':
    rs = dct_search("Account List", dct_base_url, args.filter, "No Accounts match the search criteria.", args.format)

if args.command == 'list':
    rs = dct_search("Accounts List", dct_base_url, None, "No Accounts defined.", args.format)

if args.command == 'create':
    if cfg.level > 0:
        print("Processing Accounts create")
    rs = account_create(dct_base_url, args.client_id, args.first_name, args.last_name, args.email, args.username,
                        args.password, args.tags)
    dct_print_json_formatted(rs)

if args.command == 'update':
    if cfg.level > 0:
        print("Processing Account update ID=" + args.id)
    rs = account_update(dct_base_url, args.id, args.client_id, args.first_name, args.last_name, args.email,
                        args.username)
    dct_print_json_formatted(rs)

if args.command == 'delete':
    if cfg.level > 0:
        print("Processing Account delete ID=" + args.id)
    rs = dct_delete_by_id(dct_base_url, "Deleted Account", args.id, response_code=204)

if args.command == 'password_reset':
    rs = dct_update_by_id(dct_base_url, "Password Reset for Account", args.id, {"old_password": args.old_password,
                     "new_password": args.new_password}, args.command)
    dct_print_json_formatted(rs)
    
if args.command == 'list_pwd_policy':
    if cfg.level > 0:
        print("Retrieving password policies")
    rs = url_GET(dct_base_url + "/password-policies")
    if rs.status_code == 200:
        dct_print_json_formatted(rs.json())
    else:
        dct_print_error(rs)
        sys.exit(1)

if args.command == 'update_pwd_policy':
    print("Processing password policy update")
    rs = password_policy_update(dct_base_url + "/password-policies", args.enabled, args.min_length,
                                args.reuse_disallow_limit, args.digit, args.uppercase_letter, args.lowercase_letter,
                                args.special_character, args.disallow_username_as_password)
    dct_print_json_formatted(rs)

if args.command == 'tag_list':
    rs = dct_list_by_id(dct_base_url, args.id, "/tags", args.format)
    dct_print_json_formatted(rs['tags'])

if args.command == 'tag_create':
    payload = {"tags": args.tags}
    rs = dct_post_by_id(dct_base_url, args.id, payload, "tags")
    if rs.status_code == 201:
        if cfg.level > 0:
            print("Created tags for Account - ID=" + args.id)
        rs = dct_list_by_id(dct_base_url, args.id, "/tags")
        dct_print_json_formatted(rs['tags'])
    else:
        dct_print_error(rs)
        sys.exit(1)

if args.command == 'tag_delete':
    payload = {"key": args.key}
    rs = dct_post_by_id(dct_base_url, args.id, payload, "tags/delete")
    if rs.status_code == 204:
        if cfg.level > 0:
            print("Deleted tag by key for Account - ID=" + args.id)
        rs = dct_list_by_id(dct_base_url, args.id, "/tags")
        dct_print_json_formatted(rs['tags'])
    else:
        dct_print_error(rs)
        sys.exit(1)

if args.command == 'tag_delete_all':
    rs = dct_post_by_id(dct_base_url, args.id, None, "tags/delete")
    if rs.status_code == 204:
        if cfg.level > 0:
            print("Deleted all tags for Account - ID=" + args.id)
    else:
        dct_print_error(rs)
        sys.exit(1)
