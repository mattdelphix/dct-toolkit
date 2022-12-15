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

# Init
parser = argparse.ArgumentParser(description='Delphix DCT VCDBs operations')
subparser = parser.add_subparsers(dest='command')

parser.add_argument('--version', action='version', version='%(prog)s 1.0')
parser.add_argument('--config', type=str, required=False, help="Config file")

# define commands

lst = subparser.add_parser('list')
search = subparser.add_parser('search')
view = subparser.add_parser('view')

# define view parms
view.add_argument('--id', type=str, required=True, help="VCDB to be viewed")

# define list parms
lst.add_argument('--format', type=str, required=False, help="Type of output",  choices=['json', 'report'])

# define search parms
search.add_argument('--filter', type=str, required=False, help="VCDB search string")
search.add_argument('--format', type=str, required=False, help="Type of output",  choices=['json', 'report'])
parser.add_argument('--debug', type=int, required=False, help="Debug level [0-2]",choices=[0,1,2])

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

dct_base_url = "/vcdbs"

if args.command == 'list':
    rs = dct_search("VCDBs List ", dct_base_url, None, "No VCDBs defined.", args.format)
    dct_print_json(rs)

if args.command == 'view':
    rs = dct_view_by_id(dct_base_url, args.id)
    dct_print_json(rs)

if args.command == 'search':
    rs = dct_search("VCDBs List ", dct_base_url, args.filter, "No VCDBs match the search criteria.",
                    args.format)
    dct_print_json(rs)
