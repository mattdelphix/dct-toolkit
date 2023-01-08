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


def update_saml_config(base_url, enabled, auto_create_users, metadata_url, metadata, entity_id, response_skew,
                       group_attr, first_name_attr,last_name_attr):
    payload = {"enabled": enabled,
               "auto_create_users": auto_create_users,
               "metadata_url": metadata_url,
               "metadata:": metadata,
               "entity_id": entity_id,
               "response_skew": response_skew,
               "group_attr": group_attr,
               "first_name_attr:": first_name_attr,
               "last_name_attr": last_name_attr}

    resp = url_PATCH(base_url, payload)
    if resp.status_code == 200:
        print("SAML config updated")
        print(resp.json())
        return
    else:
        dct_print_error(resp)
        sys.exit(1)


# Init
parser = argparse.ArgumentParser(description='Delphix DCT CDBs operations')
subparser = parser.add_subparsers(dest='command')

parser.add_argument('--version', action='version', version='%(prog)s Version '+cfg.version)
parser.add_argument('--config', type=str, required=False, help="Config file")
parser.add_argument('--debug', type=int, required=False, help="Debug level [0-2]",choices=[0,1,2])

# define commands
check = subparser.add_parser('is_enabled')
lst = subparser.add_parser('list')
update = subparser.add_parser('update')

# define check params
check.add_argument('--format', type=str, required=False, help="Type of output", choices=['json', 'report','id'])

# define list params
lst.add_argument('--format', type=str, required=False, help="Type of output", choices=['json', 'report','id'])

# define update params
update.add_argument('--enabled', type=str, required=False, help="Set or unset SAML, default is false",
                    choices=['true', 'false'])
update.add_argument('--auto_create_users', type=str, required=False,
                             help="System will automatically create new Accounts for those who have logged in using "
                                  "SAML", choices=['true', 'false'])
update.add_argument('--metadata_url', type=str, required=False,
                             help="IdP metadata URL for this service provider")
update.add_argument('--metadata', type=str, required=False,
                             help="IdP metadata for this service provider.This is mutually exclusive to other field "
                                  "'metadata_url'")
update.add_argument('--entity_id', type=str, required=False,
                             help="Unique identifier of this instance as a SAML/SSO service provider.")
update.add_argument('--response_skew', type=str, required=False,
                             help="Maximum time difference allowed between a SAML response and the DCT's current "
                                  "time, in seconds. If not set, it defaults to 120 seconds")
update.add_argument('--group_attr', type=str, required=False,
                             help="Group mapped attribute on SAML to create account tags in DCT")
update.add_argument('--first_name_attr', type=str, required=False,
                             help="First name attribute mapped on SAML used for mapping on DCT account")
update.add_argument('--last_name_attr', type=str, required=False,
                             help="Last name attribute mapped on SAML used for mapping on DCT account")

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

dct_base_url = "/management/saml-config"

if args.command == 'is_enabled':
    resp = url_GET("/is-saml-enabled")
    print(resp)
    if resp.status_code == 200:
        print("SAML is enabled")
        # return json.dumps(resp.json(), indent=4)
    if resp.status_code == 400:
        print("SAML is NOT enabled")
    else:
        dct_print_error(resp)
        sys.exit(1)

if args.command == 'list':
    dct_simple_list("SAML List", dct_base_url, "No SAML defined.")

if args.command == 'update':
    update_saml_config(dct_base_url, args.enabled, args.auto_create_users, args.metadata_url, args.metadata,
                       args.entity_id, args.response_skew, args.group_attr, args.first_name_attr, args.last_name_attr)
