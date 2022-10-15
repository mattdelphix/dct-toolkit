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


from helpers import *


# TODO Environment delete to be tested
# TODO add job monitoring where needed

# Environment functions
def environment_operation(base_url, env_id, ops):
    ops = ops.lower()
    if not any(x in ops for x in ["enable", "disable", "refresh"]):
        print("Wrong operation on Environment: " + ops)
        sys.exit(1)
    resp = url_POST(base_url + "/" + urllib.parse.quote(env_id) + "/" + ops, "")
    if resp.status_code == 200:
        return json.loads(resp.text)
    else:
        print(f"ERROR: Status = {resp.status_code} - {resp.text}")
        sys.exit(1)


# Init
parser = argparse.ArgumentParser(description='Delphix DCT Environment operations')
subparser = parser.add_subparsers(dest='command')

parser.add_argument('--version', action='version', version='%(prog)s 1.0')
parser.add_argument('--config', type=str, required=False, help="Config file")

# define commands

lst = subparser.add_parser('list')
search = subparser.add_parser('search')
view = subparser.add_parser('view')
delete = subparser.add_parser('delete')
disable = subparser.add_parser('disable')
enable = subparser.add_parser('enable')
refresh = subparser.add_parser('refresh')

tag_list = subparser.add_parser('tag_list')
tag_create = subparser.add_parser('tag_create')
tag_delete = subparser.add_parser('tag_delete')
tag_delete_all = subparser.add_parser('tag_delete_all')

user_list = subparser.add_parser('user_list')
user_create = subparser.add_parser('user_create')
user_create_pubkey = subparser.add_parser('user_create_pubkey')
user_create_kerb = subparser.add_parser('user_create_kerb')
user_create_cyark = subparser.add_parser('user_create_cyark')
user_create_hcorp = subparser.add_parser('user_create_hcorp')

# define list parms
lst.add_argument('--format', type=str, required=False, help="Type of output", choices=['json', 'report'])

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
search.add_argument('--format', type=str, required=False, help="Type of output", choices=['json', 'report'])

# define user_list parms
user_list.add_argument('--id', type=str, required=True, help="Environment ID with users to be listed")
user_list.add_argument('--format', type=str, required=False, help="Type of output", choices=['json', 'report'])

# define tag_list parms
tag_list.add_argument('--id', type=str, required=True, help="Environment ID to be viewed")
tag_list.add_argument('--format', type=str, required=False, help="Type of output", choices=['json', 'report'])

# define tag_create params
tag_create.add_argument('--id', type=str, required=True, help="Environment ID to add tags to")
tag_create.add_argument('--tags', nargs='*', type=str, required=True, action=dct_parsetags,
                        help="Tags of the DSource in this format:  key=value key=value")
tag_delete.add_argument('--id', type=str, required=True, help="Environment ID to delete tags from")
tag_delete.add_argument('--key', type=str, required=True, help="Tags key of existing tag")

# define tag_delete_all params
tag_delete_all.add_argument('--id', type=str, required=True, help="Environment ID to delete tags from")

# define user_create parms
user_create.add_argument('--id', type=str, required=True, help="Environment ID to be updated")
user_create.add_argument('--username', type=str, required=True, help="Username to be added")
user_create.add_argument('--password', type=str, required=True, help="Password for the user")

# define user_create_pubkey parms
user_create_pubkey.add_argument('--id', type=str, required=True, help="Environment ID to be updated")
user_create_pubkey.add_argument('--username', type=str, required=True, help="Username to be added")

# define user_create_kerb parms
user_create_kerb.add_argument('--id', type=str, required=True, help="Environment ID to be updated")

# define user_create_cyark parms
user_create_cyark.add_argument('--id', type=str, required=True, help="Environment ID to be updated")
user_create_cyark.add_argument('--vault', type=str, required=True, help="Vault to be added")
user_create_cyark.add_argument('--username', type=str, required=True, help="Username to be added")

# define user_create_hcorp parms
user_create_hcorp.add_argument('--id', type=str, required=True, help="Environment ID to be updated")
user_create_hcorp.add_argument('--vault', type=str, required=True, help="Hashicorp Vault to be added")
user_create_hcorp.add_argument('--vault_username', type=str, required=True, help="Hashicorp Vault Username to be added")
user_create_hcorp.add_argument('--vault_engine', type=str, required=True, help="Hashicorp Vault engine to be added")
user_create_hcorp.add_argument('--vault_secret_path', type=str, required=True,
                               help="Hashicorp Vault Secret Path to be added")
user_create_hcorp.add_argument('--vault_user_key', type=str, required=True, help="Hashicorp Vault engine to be added")
user_create_hcorp.add_argument('--vault_secret_key', type=str, required=True,
                               help="Hashicorp Vault Secret key to be added")

# force help if no parms
args = parser.parse_args(args=None if sys.argv[1:] else ['--help'])

# Start processing
dct_read_config(args.config)

dct_base_url = "/environments"

if args.command == 'list':
    rs = dct_search("Environment List", dct_base_url, None, "No Environments defined.", args.format)
    print(rs)

if args.command == 'view':
    rs = dct_view_by_id(dct_base_url, args.id)
    print(rs)

if args.command == 'user_create':
    payload = {"username": args.username, "password": args.password}
    rs = dct_post_by_id(dct_base_url, args.id, payload, "users")
    if rs.status_code == 204:
        print("Created '" + args.username + "' for Environment - ID=" + args.id)
    else:
        print(f"ERROR: Status = {rs.status_code} - {rs.text}")
        sys.exit(1)

if args.command == 'user_create_pubkey':
    payload = {"use_engine_public_key": "true", "username": args.username}
    rs = dct_post_by_id(dct_base_url, args.id, payload, "users")
    if rs.status_code == 204:
        print("Set '" + args.username + "' for Environment - ID=" + args.id)
    else:
        print(f"ERROR: Status = {rs.status_code} - {rs.text}")
        sys.exit(1)

if args.command == 'user_create_kerb':
    payload = {"use_kerberos_authentication": "true"}
    rs = dct_post_by_id(dct_base_url, args.id, payload, "users")
    if rs.status_code == 204:
        print("Set Kerberos for Environment - ID=" + args.id)
    else:
        print(f"ERROR: Status = {rs.status_code} - {rs.text}")
        sys.exit(1)

if args.command == 'user_create_cyark':
    payload = {"vault": args.vault, "vault_username": args.username,
               "cyberark_vault_query_string": "Safe=Test;Folder=Test;Object=Test"}
    rs = dct_post_by_id(dct_base_url, args.id, payload, "users")
    if rs.status_code == 204:
        print("Set CyberArk '" + args.username + "' for Environment - ID=" + args.id)
    else:
        print(f"ERROR: Status = {rs.status_code} - {rs.text}")
        sys.exit(1)

if args.command == 'user_create_hcorp':
    payload = {"vault": args.vault, "vault_username": args.username, "hashicorp_vault_engine": args.vault_engine,
               "hashicorp_vault_secret_path": args.vault_secret_path,
               "hashicorp_vault_username_key": args.vault_user_key, "hashicorp_vault_secret_key": args.vault_secret_key}
    rs = dct_post_by_id(dct_base_url, args.id, payload, "users")
    if rs.status_code == 204:
        print("Set CyberArk '" + args.username + "' for Environment - ID=" + args.id)
    else:
        print(f"ERROR: Status = {rs.status_code} - {rs.text}")
        sys.exit(1)

if args.command == 'tag_list':
    rs = dct_list_by_id(dct_base_url, args.id, "/tags", args.format)
    print(rs)

if args.command == 'user_list':
    rs = dct_list_by_id(dct_base_url, args.id, "/users", args.format)
    print(rs)

if args.command == 'search':
    rs = dct_search("Environment List", dct_base_url, args.filter, "No Environments match the search criteria.",
                    args.format)
    print(rs)

if args.command == 'refresh':
    print("Processing Environment refresh ID=" + args.id)
    rs = environment_operation(dct_base_url, args.id, args.command)
    dct_job_monitor(rs['job']['id'])

if args.command == 'enable':
    print("Processing Environment enable ID=" + args.id)
    rs = environment_operation(dct_base_url, args.id, args.command)
    dct_job_monitor(rs['job']['id'])

if args.command == 'disable':
    print("Processing Environment disable ID=" + args.id)
    rs = environment_operation(dct_base_url, args.id, args.command)
    dct_job_monitor(rs['job']['id'])

if args.command == 'delete':
    print("Processing Environment delete ID=" + args.id)
    rs = dct_delete_by_id(dct_base_url, "Deleted Environment", args.id)

if args.command == 'tag_create':
    payload = {"tags": args.tags}
    # payload = {"tags": json.loads(args.tags)}
    rs = dct_post_by_id(dct_base_url, args.id, payload, "tags")
    if rs.status_code == 201:
        print("Created tags for Environment - ID=" + args.id)
    else:
        print(f"ERROR: Status = {rs.status_code} - {rs.text}")
        sys.exit(1)

if args.command == 'tag_delete':
    payload = {"key": args.key}
    rs = dct_post_by_id(dct_base_url, args.id, payload, "tags/delete")
    if rs.status_code == 204:
        print("Deleted tag '" + args.key + "' for Environment - ID=" + args.id)
    else:
        print(f"ERROR: Status = {rs.status_code} - {rs.text}")
        sys.exit(1)

if args.command == 'tag_delete_all':
    rs = dct_post_by_id(dct_base_url, args.id, None, "tags/delete")
    if rs.status_code == 204:
        print("Deleted all tags for Environment - ID=" + args.id)
    else:
        print(f"ERROR: Status = {rs.status_code} - {rs.text}")
        sys.exit(1)
