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
parser = argparse.ArgumentParser(description="Delphix DCT connectivity test")
subparser = parser.add_subparsers(dest='command')

parser.add_argument('--version', action='version', version='%(prog)s 1.0')
parser.add_argument('--config', type=str, required=False, help="Config file")
parser.add_argument('--debug', type=int, required=False, help="Debug level [0-2]",choices=[0,1,2])

# define commands
check = subparser.add_parser('check')


# define check parms
check.add_argument('--id', type=str, required=True, help="Engine ID to test connectivity with")
check.add_argument('--host', type=str, required=True, help="Host or IP of Engine to be tested")
check.add_argument('--port', type=str, required=False, help="Port of Engine to be tested")
check.add_argument('--format', type=str, required=False, help="Type of output",  choices=['json', 'report'])

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

dct_base_url = "/connectivity"

if args.command == 'check':
    if args.port is None:
        args.port = 22
    rs = connectivity_check(dct_base_url, args.id, args.host, args.port)
    dct_print_json(rs)

