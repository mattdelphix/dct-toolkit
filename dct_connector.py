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

# Connector functions
def connector_update(base_url, conn_id, name, hostname, port, username, password):
    payload = {"name": name, "username": username, "password": password,
               "hostname": hostname, "port": port}
    resp = url_PATCH(base_url + "/" + urllib.parse.quote(conn_id), payload)
    if resp.status_code == 200:
        rsp = resp.json()
        print("Updated Connector" + " - ID=" + conn_id)
        return rsp
    else:
        dct_print_error(resp)
        sys.exit(1)


# Init
parser = argparse.ArgumentParser(description="Delphix DCT Masking connector operations")
subparser = parser.add_subparsers(dest='command')

parser.add_argument('--version', action='version', version='%(prog)s 1.0')
parser.add_argument('--config', type=str, required=False, help="Config file")
parser.add_argument('--debug', type=int, required=False, help="Debug level [0-2]",choices=[0,1,2])

# define commands
lst = subparser.add_parser('list')
tst = subparser.add_parser('test')
search = subparser.add_parser('search')
view = subparser.add_parser('view')
updt = subparser.add_parser('update')

# define list parms
lst.add_argument('--format', type=str, required=False, help="Type of output",  choices=['json', 'report','id'])

# define test parms
tst.add_argument('--id', type=str, required=True, help="Masking connector ID to be tested")
tst.add_argument('--format', type=str, required=False, help="Type of output",  choices=['json', 'report','id'])

# define view parms
view.add_argument('--id', type=str, required=True, help="Masking connector ID to be viewed")

# define search parms
search.add_argument('--filter', type=str, required=False, help="Masking connector search string")
search.add_argument('--format', type=str, required=False, help="Type of output", choices=['json', 'report','id'])

# define update parms
updt.add_argument('--id', type=str, required=True, help="Masking connector ID to be updated")
updt.add_argument('--name', type=str, required=False, help="Masking connector name to be updated")
updt.add_argument('--hostname', type=str, required=False, help="Masking connector hostname to be updated")
updt.add_argument('--port', type=str, required=False, help="Masking connector port to be updated")
updt.add_argument('--username', type=str, required=False, help="User name of the Masking connector to be updated")
updt.add_argument('--password', type=str, required=False, help="Password of the Masking connector to be updated")

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

dct_base_url = "/connectors"

if args.command == 'view':
    rs = dct_view_by_id(dct_base_url, args.id)
    dct_print_json_formatted(rs)

if args.command == 'list':
    rs = dct_search("Masking connector List", dct_base_url, None, "No Masking connectors defined.", args.format)

if args.command == 'search':
    rs = dct_search("Masking connector List", dct_base_url, args.filter, "No Masking connectors match the search criteria.",
                    args.format)

if args.command == 'test':
    rs = dct_post_by_id(dct_base_url, args.id, "/test")
    dct_print_json_formatted(rs)

if args.command == 'update':
    print("Processing Connector update ID=" + args.id)
    rs = connector_update(dct_base_url, args.id, args.name, args.hostname, args.port, args.username, args.password)
    dct_job_monitor(rs['job']['id'])