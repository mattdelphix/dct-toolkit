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
parser.add_argument('--debug', type=int, required=False, help="Debug level [0-2]",choices=[0,1,2])

# define commands

lst = subparser.add_parser('list')
search = subparser.add_parser('search')
delete = subparser.add_parser('delete')
register_mask = subparser.add_parser('register_mask')
register_virt = subparser.add_parser('register_virt')
view = subparser.add_parser('view')

# define view parms
view.add_argument('--id', type=str, required=True, help="engine UUID to be viewed")

# define list parms
lst.add_argument('--format', type=str, required=False, help="Type of output", choices=['json', 'report'])

# define delete parms
delete.add_argument('--id', type=str, required=True, help="engine UUID to be deleted")

# define search parms
search.add_argument('--filter', type=str, required=False, help="Engine search string")
search.add_argument('--format', type=str, required=False, help="Type of output", choices=['json', 'report'])

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

# force help if no parms
args = parser.parse_args(args=None if sys.argv[1:] else ['--help'])

# Start processing
dct_read_config(args.config)
if args.debug:
    cfg.level = args.debug

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
