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
parser = argparse.ArgumentParser(description='Delphix DCT Management Vault operations')
subparser = parser.add_subparsers(dest='command')

parser.add_argument('--version', action='version', version='%(prog)s Version '+cfg.version)
parser.add_argument('--config', type=str, required=False, help="Config file")
parser.add_argument('--debug', type=int, required=False, help="Debug level [0-2]",choices=[0,1,2])

# define commands

lst = subparser.add_parser('list')
#create = subparser.add_parser('create')
view = subparser.add_parser('view')
delete  = subparser.add_parser('delete')

# define view parms
view.add_argument('--id', type=str, required=True, help="Hashicorp Vault to be viewed")

# define list parms
lst.add_argument('--format', type=str, required=False, help="Type of output",  choices=['json', 'report','id'])

# define search parms
#create.add_argument('--filter', type=str, required=False, help="Hashicorp Vault search string")
#create.add_argument('--format', type=str, required=False, help="Type of output",  choices=['json', 'report','id'])

# define delete parms
delete.add_argument('--id', type=str, required=True, help="Hashicorp Vault to be deleted")

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

dct_base_url = "/management/vaults/hashicorp"

if args.command == 'list':
    dct_search("Hashicorp Vault List ", dct_base_url, None, "No Hashicorp Vault defined.", args.format)

if args.command == 'view':
    rs = dct_view_by_id(dct_base_url, args.id)
    dct_print_json_formatted(rs)

if args.command == 'delete':
    dct_delete_by_id(dct_base_url, "Hashicorp Vault ID deleted ", args.id, 204)
