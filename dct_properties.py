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


# NOT OK
def update_properties_config(base_url,disable_username_password):
    payload = {"disable_username_password": disable_username_password}

    resp = url_PATCH(base_url, payload)
    if resp.status_code == 200:
        print("Properties config updated")
        print(resp.json())
    else:
        dct_print_error(resp)
        sys.exit(1)

# Init
parser = argparse.ArgumentParser(description='Delphix DCT CDBs operations')
subparser = parser.add_subparsers(dest='command')

parser.add_argument('--version', action='version', version='%(prog)s 1.0')
parser.add_argument('--config', type=str, required=False, help="Config file")
parser.add_argument('--debug', type=int, required=False, help="Debug level [0-2]",choices=[0,1,2])

# define commands
lst = subparser.add_parser('list')
update = subparser.add_parser('update')

# define list params
lst.add_argument('--format', type=str, required=False, help="Type of output", choices=['json', 'report'])

# define update params
update.add_argument('--disable_username_password', type=str, required=True, choices=['true', 'false'],
                    help="Property to define either username & password based authentication disabled or not")

# force help if no parms
args = parser.parse_args(args=None if sys.argv[1:] else ['--help'])

# Start processing
dct_read_config(args.config)
if args.debug:
    cfg.level = args.debug

# dct_base_url = "/is-saml-enabled"
dct_base_url = "/management/properties"

if args.command == 'list':
    dct_simple_list("Properties List", dct_base_url, "No Properties defined.")

if args.command == 'update':
    update_properties_config(dct_base_url, args.disable_username_password)
