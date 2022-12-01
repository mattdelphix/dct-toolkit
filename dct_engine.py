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


# Engine functions
def virt_engine_register(base_url, name, hostname, user, password, insecure_ssl, unsafe_ssl):
    # TODO add hashicorp, trustore and tags
    payload = {"name": name, "hostname": hostname, "username": user, "password": password, "insecure_ssl": insecure_ssl,
               "unsafe_ssl_hostname_check": unsafe_ssl}
    resp = url_POST(base_url, payload)
    if resp.status_code == 201:
        rsp = resp.json()
        print(f"Registered Virtualization Engine with ID={rsp['id']}")
        return rsp
    else:
        print(f"ERROR: Status = {resp.status_code} - {resp.text}")
        sys.exit(1)


def mask_engine_register(base_url, name, hostname, mask_user, mask_password, insecure_ssl, unsafe_ssl):
    # TODO add hashicorp, trustore and tags
    payload = {"name": name, "hostname": hostname, "masking_username": mask_user, "masking_password": mask_password,
               "insecure_ssl": insecure_ssl,
               "unsafe_ssl_hostname_check": unsafe_ssl}
    resp = url_POST(base_url, payload)
    if resp.status_code == 201:
        rsp = resp.json()
        print(f"Registered Masking Engine with ID={rsp['id']}")
        return rsp
    else:
        print(f"ERROR: Status = {resp.status_code} - {resp.text}")
        sys.exit(1)


# Init
parser = argparse.ArgumentParser(description="Delphix DCT Engine operations")
subparser = parser.add_subparsers(dest='command')

parser.add_argument('--version', action='version', version='%(prog)s 1.0')
parser.add_argument('--config', type=str, required=False, help="Config file")

# define commands

lst = subparser.add_parser('list')
search = subparser.add_parser('search')
delete = subparser.add_parser('delete')
register_mask = subparser.add_parser('register_mask')
register_virt = subparser.add_parser('register_virt')
view = subparser.add_parser('view')
tag_create = subparser.add_parser('tag_create')
tag_delete = subparser.add_parser('tag_delete')
tag_delete_all = subparser.add_parser('tag_delete_all')

# define view parms
view.add_argument('--id', type=str, required=True, help="Engine UUID to be viewed")

# define list parms
lst.add_argument('--format', type=str, required=False, help="Type of output", choices=['json', 'report'])

# define delete parms
delete.add_argument('--id', type=str, required=True, help="Engine UUID to be deleted")

# define search parms
search.add_argument('--filter', type=str, required=False, help="Engine search string")
search.add_argument('--format', type=str, required=False, help="Type of output", choices=['json', 'report'])

# define register_virt parms
register_virt.add_argument('--name', type=str, required=True, help="Name used to refer to the engine in DCT")
register_virt.add_argument('--hostname', type=str, required=True, help="Hostname or ip address")
register_virt.add_argument('--user', type=str, required=True, help="Admin user")
register_virt.add_argument('--password', type=str, required=True, help="Admin password")
register_virt.add_argument('--insecure_ssl', type=str, required=False, help="Is SSL secure?", default=True)
register_virt.add_argument('--unsafe_ssl_hostname_check', required=False, type=str, help="Check SSL connection",
                           default=True)

# define register_mask parms
register_mask.add_argument('--name', type=str, required=True, help="Name used to refer to the engine in DCT")
register_mask.add_argument('--hostname', type=str, required=True, help="hostname or ip address")
register_mask.add_argument('--user', type=str, required=True, help="masking admin user")
register_mask.add_argument('--password', type=str, required=True, help="masking admin password")
register_mask.add_argument('--insecure_ssl', type=str, required=False, help="is SSL secure?", default=True)
register_mask.add_argument('--unsafe_ssl_hostname_check', required=False, type=str, help="check SSL connection",
                           default=True)

# define tag_create params
tag_create.add_argument('--id', type=str, required=True, help="Engine UUID to add tags to")
tag_create.add_argument('--tags', nargs='*', type=str, required=True, action=dct_parsetags,
                        help="Tags of the Engine in this format:  key=value key=value")
# define tag_delete params
tag_delete.add_argument('--id', type=str, required=True, help="Engine UUID to delete tags from")
tag_delete.add_argument('--key', type=str, required=True, help="Tags key of existing tag")

# define tag_delete_all params
tag_delete_all.add_argument('--id', type=str, required=True, help="Engine UUID to delete tags from")

# force help if no parms
args = parser.parse_args(args=None if sys.argv[1:] else ['--help'])

# Start processing
dct_read_config(args.config)

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

if args.command == 'register_virt':
    print("Registering Virtualization Engine " + args.hostname)
    rs = virt_engine_register(dct_base_url, args.name, args.hostname, args.user, args.password, args.insecure_ssl,
                              args.unsafe_ssl_hostname_check)
    print(rs)

if args.command == 'register_mask':
    print("Registering Masking Engine " + args.hostname)
    rs = mask_engine_register(dct_base_url, args.name, args.hostname, args.user, args.password, args.insecure_ssl,
                              args.unsafe_ssl_hostname_check)
    print(rs)

if args.command == 'tag_create':
    payload = {"tags": args.tags}
    rs = dct_post_by_id(dct_base_url, args.id, payload, "tags")
    if rs.status_code == 201:
        print("Create tags for dSource - ID=" + args.id)
    else:
        print(f"ERROR: Status = {rs.status_code} - {rs.text}")
        sys.exit(1)

if args.command == 'tag_delete':
    payload = {"key": args.key}
    rs = dct_post_by_id(dct_base_url, args.id, payload, "tags/delete")
    if rs.status_code == 204:
        print("Delete tag for DSourceID - ID=" + args.id)
    else:
        print(f"ERROR: Status = {rs.status_code} - {rs.text}")
        sys.exit(1)

if args.command == 'tag_delete_all':
    rs = dct_post_by_id(dct_base_url, args.id, None, "tags/delete")
    if rs.status_code == 204:
        print("Deleted all tags for DSource - ID=" + args.id)
    else:
        print(f"ERROR: Status = {rs.status_code} - {rs.text}")
        sys.exit(1)
