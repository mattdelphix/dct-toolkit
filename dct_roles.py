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
# Date    : October 2022


from helpers import *

def connectivity_check (base_url, id, host, port):
    payload = {"engine_id": id, "host": host, "port": port}

    resp = url_POST(base_url + "/check", payload)
    if resp.status_code == 200:
        rsp = resp.json()
        #print("Updated Account" + " - ID=" + vdb_id)
        return rsp
    else:
        dct_print_error(resp)
        sys.exit(1)

# Init
parser = argparse.ArgumentParser(description="Delphix DCT Roles")
subparser = parser.add_subparsers(dest='command')

parser.add_argument('--version', action='version', version='%(prog)s 1.0')
parser.add_argument('--config', type=str, required=False, help="Config file")
parser.add_argument('--debug', type=int, required=False, help="Debug level [0-2]",choices=[0,1,2])

# define commands
lst = subparser.add_parser('list')
view = subparser.add_parser('view')

# define list parms
lst.add_argument('--format', type=str, required=False, help="Type of output", choices=['json', 'report'])

# define view parms
view.add_argument('--id', type=str, required=True, help="Bookmark ID to be viewed")

# force help if no parms
args = parser.parse_args(args=None if sys.argv[1:] else ['--help'])

# Start processing
dct_read_config(args.config)
if args.debug:
    cfg.level = args.debug

dct_base_url = "/roles"

if args.command == 'list':
    rs = dct_search("Bookmarks List", dct_base_url, None, "No Bookmarks defined.", args.format)
    dct_print_json(rs)

if args.command == 'view':
    rs = dct_view_by_id(dct_base_url, args.id)
    dct_print_json(rs)

