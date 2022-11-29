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
def update_smtp_config(base_url, enabled, server, port, authentication_enabled, tls_enabled, username, password,
                       from_address, send_timeout):
    payload = {"enabled": enabled,
               "server": server,
               "port": port,
               "authentication_enabled:": authentication_enabled,
               "tls_enabled": tls_enabled,
               "username": username,
               "password": password,
               "from_address:": from_address,
               "send_timeout": send_timeout}

    resp = url_PATCH(base_url, payload)
    if resp.status_code == 200:
        rsp = resp.json()
        print("SAML config updated")
        return rsp
    else:
        print(f"ERROR: Status = {resp.status_code} - {resp.text}")
        sys.exit(1)


# Init
parser = argparse.ArgumentParser(description='Delphix DCT CDBs operations')
subparser = parser.add_subparsers(dest='command')

parser.add_argument('--version', action='version', version='%(prog)s 1.0')
parser.add_argument('--config', type=str, required=False, help="Config file")

# define commands
validate = subparser.add_parser('validate')
lst = subparser.add_parser('list')
update = subparser.add_parser('update')

# define check params
validate.add_argument('--address', type=str, required=True, help="Address of Smtp server to validate")

# define list params
lst.add_argument('--format', type=str, required=False, help="Type of output", choices=['json', 'report'])

# define update params
update.add_argument('--enabled', type=str, required=False, help="Set or unset LDAP, default is false",
                    choices=['true', 'false'])
update.add_argument('--server', type=str, required=False, help="IP address or hostname of SMTP relay server.")
update.add_argument('--port', type=str, required=False, help="Port number to use.")
update.add_argument('--authentication_enabled', type=str, required=False,
                    help="True if username/password authentication should be used", choices=['true', 'false'])
update.add_argument('--tls_enabled', type=str, required=False,
                    help="True if TLS (transport layer security) should be used.", choices=['true', 'false'])
update.add_argument('--username', type=str, required=False,
                    help="If authentication is enabled, username to use when authenticating to the server.")
update.add_argument('--password', type=str, required=False,
                    help="If authentication is enabled, password to use when authenticating to the server.")
update.add_argument('--from_address', type=str, required=False,
                    help="From address to use when sending mail. If unspecified, 'noreply@delphix.com' is used.")
update.add_argument('--send_timeout', type=str, required=False,
                    help="Maximum timeout to wait, in seconds, when sending mail.")

# force help if no parms
args = parser.parse_args(args=None if sys.argv[1:] else ['--help'])

# Start processing
dct_read_config(args.config)

# dct_base_url = "/is-saml-enabled"
dct_base_url = "/management/smtp"

if args.command == 'validate':
    payload = {"to_address": args.address}
    resp = dct_create(dct_base_url + "/validate", payload)
    print(resp)

if args.command == 'list':
    resp = dct_search("Saml List", dct_base_url, None, "No SAML defined.", args.format)
    print(resp)

if args.command == 'update':
    update_smtp_config(dct_base_url, args.enabled, args.server, args.port, args.authentication_enabled, args.tls_enabled
                       , args.username, args.password, args.from_address, args.send_timeout)
