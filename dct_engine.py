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

# TODO add engine update logic

# Engine functions
def virt_engine_register(base_url, name, hostname, user, password, insecure_ssl, unsafe_ssl):
    # TODO add hashicorp, trustore and tags
    payload = {"name": name, "hostname": hostname, "username": user, "password": password, "insecure_ssl": insecure_ssl,
               "unsafe_ssl_hostname_check": unsafe_ssl}
    resp = url_POST(base_url, payload)
    if resp.status_code == 201:
        rsp = resp.json()
        if cfg.level == 1:
            print(f"Registered Virtualization Engine with ID={rsp['id']}")
        return rsp
    else:
        dct_print_error(resp)
        sys.exit(1)


def mask_engine_register(base_url, name, hostname, mask_user, mask_password, insecure_ssl, unsafe_ssl):
    # TODO add hashicorp, trustore and tags
    payload = {"name": name, "hostname": hostname, "masking_username": mask_user, "masking_password": mask_password,
               "insecure_ssl": insecure_ssl,
               "unsafe_ssl_hostname_check": unsafe_ssl}
    resp = url_POST(base_url, payload)
    if resp.status_code == 201:
        rsp = resp.json()
        if cfg.level == 1:
            print(f"Registered Masking Engine with ID={rsp['id']}")
        return rsp
    else:
        dct_print_error(resp)
        sys.exit(1)

def virt_engine_update(base_url, engine_id, name, hostname, user, password, insecure_ssl, unsafe_ssl):
    # TODO add hashicorp, trustore and tags
    payload = {"name": name, "hostname": hostname, "username": user, "password": password,
               "insecure_ssl": insecure_ssl,
               "unsafe_ssl_hostname_check": unsafe_ssl}
    rs = dct_put_update_by_id(base_url, "Update Engine ", engine_id, payload)
    dct_print_json_formatted(rs)

def mask_engine_update(base_url, engine_id, name, hostname, mask_user, mask_password, insecure_ssl, unsafe_ssl):
    # TODO add hashicorp, trustore and tags
    payload = {"name": name, "hostname": hostname, "masking_username": mask_user, "masking_password": mask_password,
               "insecure_ssl": insecure_ssl,
               "unsafe_ssl_hostname_check": unsafe_ssl}
    rs = dct_put_update_by_id(base_url, "Update Engine ", engine_id, payload)
    dct_print_json_formatted(rs)

# Init
parser = argparse.ArgumentParser(description="Delphix DCT Engine operations")
subparser = parser.add_subparsers(dest='command')

parser.add_argument('--version', action='version', version='%(prog)s 1.0')
parser.add_argument('--config', type=str, required=False, help="Config file")
parser.add_argument('--debug', type=int, required=False, help="Debug level [0-2]",choices=[0,1,2])

# define commands

lst = subparser.add_parser('list')
search = subparser.add_parser('search')
delete = subparser.add_parser('delete')
register_mask = subparser.add_parser('register_mask')
register_virt = subparser.add_parser('register_virt')
update_mask = subparser.add_parser('update_mask')
update_virt = subparser.add_parser('update_virt')
view = subparser.add_parser('view')
tag_list = subparser.add_parser('tag_list')
tag_create = subparser.add_parser('tag_create')
tag_delete = subparser.add_parser('tag_delete')
tag_delete_all = subparser.add_parser('tag_delete_all')

# define view parms
view.add_argument('--id', type=str, required=True, help="engine UUID or Name to be viewed")

# define list parms
lst.add_argument('--format', type=str, required=False, help="Type of output", choices=['json', 'report','id'])

# define delete parms
delete.add_argument('--id', type=str, required=True, help="engine UUID to be deleted")

# define search parms
search.add_argument('--filter', type=str, required=False, help="Engine search string")
search.add_argument('--format', type=str, required=False, help="Type of output", choices=['json', 'report','id'])

# define register_virt parms
register_virt.add_argument('--name', type=str, required=True, help="Name used to refer to the engine in DCT")
register_virt.add_argument('--hostname', type=str, required=True, help="hostname or ip address")
register_virt.add_argument('--user', type=str, required=True, help="admin user")
register_virt.add_argument('--password', type=str, required=True, help="admin password")
register_virt.add_argument('--insecure_ssl', type=str, required=False, help="is SSL secure?", default=True)
register_virt.add_argument('--unsafe_ssl_hostname_check', required=False, type=str, help="check SSL connection",
                           default=True)

# define register_mask parms
register_mask.add_argument('--name', type=str, required=True, help="Name used to refer to the engine in DCT")
register_mask.add_argument('--hostname', type=str, required=True, help="hostname or ip address")
register_mask.add_argument('--user', type=str, required=True, help="masking admin user")
register_mask.add_argument('--password', type=str, required=True, help="masking admin password")
register_mask.add_argument('--insecure_ssl', type=str, required=False, help="is SSL secure?", default=True)
register_mask.add_argument('--unsafe_ssl_hostname_check', required=False, type=str, help="check SSL connection",
                           default=True)

# define update_virt parms
update_virt.add_argument('--id', type=str, required=True, help="virtualization engine UUID to be updated")
update_virt.add_argument('--name', type=str, required=False, help="name used to refer to the engine in DCT")
update_virt.add_argument('--hostname', type=str, required=False, help="hostname or ip address")
update_virt.add_argument('--user', type=str, required=False, help="admin user")
update_virt.add_argument('--password', type=str, required=False, help="admin password")
update_virt.add_argument('--insecure_ssl', type=str, required=False, help="is SSL secure?", default=True)
update_virt.add_argument('--unsafe_ssl_hostname_check', required=False, type=str, help="check SSL connection",
                           default=True)

# define update_mask parms
update_mask.add_argument('--id', type=str, required=True, help="masking engine UUID to be updated")
update_mask.add_argument('--name', type=str, required=False, help="name used to refer to the engine in DCT")
update_mask.add_argument('--hostname', type=str, required=False, help="hostname or ip address")
update_mask.add_argument('--user', type=str, required=False, help="masking admin user")
update_mask.add_argument('--password', type=str, required=True, help="masking admin password")
update_mask.add_argument('--insecure_ssl', type=str, required=False, help="is SSL secure?", default=True)
update_mask.add_argument('--unsafe_ssl_hostname_check', required=False, type=str, help="check SSL connection",
                           default=True)

# define tag_list parms
tag_list.add_argument('--id', type=str, required=True, help="Engine ID for tags list")
tag_list.add_argument('--format', type=str, required=False, help="Type of output", choices=['json', 'report','id'])

# define tag_create params
tag_create.add_argument('--id', type=str, required=True, help="Engine ID to add tags to")
tag_create.add_argument('--tags', nargs='*', type=str, required=True, action=dct_parsetags,
                        help="Tags of the Engine in this format:  key=value key=value")
# define tag_delete params
tag_delete.add_argument('--id', type=str, required=True, help="Engine ID to delete tags from")
tag_delete.add_argument('--key', type=str, required=True, help="Tags key of existing tag")

# define tag_delete_all params
tag_delete_all.add_argument('--id', type=str, required=True, help="Engine ID to delete tags from")

# force help if no parms
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

dct_base_url = "/management/engines"

if args.command == 'list':
    rs = dct_search("Engine List", dct_base_url, None, "No Engines defined.", args.format)

if args.command == 'view':
    rs = dct_view_by_id(dct_base_url, args.id)
    dct_print_json_formatted(rs)

if args.command == 'delete':
    if cfg.level == 1:
        print("Processing Engine delete ID=" + args.id)
    rs = dct_delete_by_id(dct_base_url, "Deleted Engine", args.id)

if args.command == 'search':
    rs = dct_search("Engine List", dct_base_url, args.filter, "No Engines match the search criteria.",
                    args.format)

if args.command == 'register_virt':
    if cfg.level == 1:
        print("Registering Virtualization Engine " + args.hostname)
    rs = virt_engine_register(dct_base_url, args.name, args.hostname, args.user, args.password, args.insecure_ssl,
                              args.unsafe_ssl_hostname_check)
    dct_print_json_formatted(rs)

if args.command == 'register_mask':
    if cfg.level == 1:
        print("Registering Masking Engine " + args.hostname)
    rs = mask_engine_register(dct_base_url, args.name, args.hostname, args.user, args.password, args.insecure_ssl,
                              args.unsafe_ssl_hostname_check)
    dct_print_json_formatted(rs)

if args.command == 'tag_list':
    rs = dct_list_by_id(dct_base_url, args.id, "/tags", args.format)
    dct_print_json_formatted(rs['tags'])

if args.command == 'tag_create':
    payload = {"tags": args.tags}
    rs = dct_post_by_id(dct_base_url, args.id, payload, "tags")
    if rs.status_code == 201:
        if cfg.level == 1:
            print("Created tags for Engine - ID=" + args.id)
        rs = dct_list_by_id(dct_base_url, args.id, "/tags")
        dct_print_json_formatted(rs['tags'])
    else:
        dct_print_error(rs)
        sys.exit(1)

if args.command == 'tag_delete':
    payload = {"key": args.key}
    rs = dct_post_by_id(dct_base_url, args.id, payload, "tags/delete")
    if rs.status_code == 204:
        if cfg.level == 1:
            print("Deleted tag by key for Engine - ID=" + args.id)
        rs = dct_list_by_id(dct_base_url, args.id, "/tags")
        dct_print_json_formatted(rs['tags'])
    else:
        dct_print_error(rs)
        sys.exit(1)

if args.command == 'tag_delete_all':
    rs = dct_post_by_id(dct_base_url, args.id, None, "tags/delete")
    if rs.status_code == 204:
        if cfg.level == 1:
            print("Deleted all tags for Engine - ID=" + args.id)
    else:
        dct_print_error(rs)
        sys.exit(1)

if args.command == 'update_virt':
    if cfg.level == 1:
        print("Updating Virtualization Engine " + args.hostname)
    curr = dct_view_by_id(dct_base_url, args.id)
    if curr['type'] != "VIRTUALIZATION":
        print(f"Engine with ID = "+ args.id + " is not a Masking engine.")
        sys.exit(1)
    if args.name:
        curr['name'] = args.name
    if args.hostname:
        curr['hostname'] = args.hostname
    if args.user:
        curr['username'] = args.user
    if args.password:
        curr['password'] = args.password
    if args.insecure_ssl:
        curr['insecure_ssl'] = args.insecure_ssl
    if args.unsafe_ssl_hostname_check:
        curr['unsafe_ssl_hostname_check'] = args.insecure_ssl
    rs = mask_engine_update(dct_base_url, args.id, curr['name'], curr['hostname'], curr['username'], curr['password'], curr['insecure_ssl'],
                              curr['unsafe_ssl_hostname_check'])
    dct_print_json_formatted(rs)

if args.command == 'update_mask':
    if cfg.level == 1:
        print("Updating Masking Engine " + args.hostname)
    curr = dct_view_by_id(dct_base_url, args.id)
    if curr['type'] != "MASKING":
        print(f"Engine with ID = "+ args.id + " is not a Masking engine.")
        sys.exit(1)
    if args.name:
        curr['name'] = args.name
    if args.hostname:
        curr['hostname'] = args.hostname
    if args.user:
        curr['masking_username'] = args.user
    if args.password:
        curr['masking_password'] = args.password
    if args.insecure_ssl:
        curr['insecure_ssl'] = args.insecure_ssl
    if args.unsafe_ssl_hostname_check:
        curr['unsafe_ssl_hostname_check'] = args.insecure_ssl
    rs = mask_engine_update(dct_base_url, args.id, curr['name'], curr['hostname'], curr['username'], curr['password'], curr['insecure_ssl'],
                              curr['unsafe_ssl_hostname_check'])
    dct_print_json_formatted(rs)
