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
import cfg
from helpers import *


def update_saml_config(base_url, enabled, auto_create_users, hostname, port, domains,
                       enable_ssl, truststore_filename, truststore_password, insecure_ssl, unsafe_ssl_hostname_check):
    payload = {"enabled": enabled,
               "auto_create_users": auto_create_users,
               "hostname": hostname,
               "port": port,
               "domains": domains,
               "enable_ssl": enable_ssl,
               "truststore_filename": truststore_filename,
               "truststore_password": truststore_password,
               "insecure_ssl": insecure_ssl,
               "unsafe_ssl_hostname_check": unsafe_ssl_hostname_check}
    rs = url_PUT(base_url, payload)
    if rs.status_code == 200:
        if cfg.level > 0:
            print("LDAP config updated")
        dct_print_json_formatted(rs.json())
    else:
        dct_print_error(rs)
        sys.exit(1)


# Init
parser = argparse.ArgumentParser(description='Delphix DCT CDBs operations')
subparser = parser.add_subparsers(dest='command')

parser.add_argument('--version', action='version', version='%(prog)s Version ' + cfg.version)
parser.add_argument('--config', type=str, required=False, help="Config file")
parser.add_argument('--debug', type=int, required=False, help="Debug level [0-2]", choices=[0, 1, 2])

# define commands
lst = subparser.add_parser('list')
validate = subparser.add_parser('validate')
update = subparser.add_parser('update')

# define list params
lst.add_argument('--format', type=str, required=False, help="Type of output", choices=['json', 'report', 'id'])

# define validate params
validate.add_argument('--username', type=str, required=True, help="Username to validate if LDAP is valid")
validate.add_argument('--password', type=str, required=True, help="Password to validate if LDAP is valid")

# define update params
update.add_argument('--enabled', type=str, required=False, help="Set or unset lDAP, default is true",
                    choices=['true', 'false'])
update.add_argument('--auto_create_users', type=str, required=False,
                    help="System will automatically create new Accounts for those who have logged in using "
                         "LDAP, default is true", choices=['true', 'false'])
update.add_argument('--hostname', type=str, required=False, help="The hostname of the LDAP server")
update.add_argument('--port', type=str, required=False, help="The port of the LDAP server")
update.add_argument('--domains', type=str, required=False,
                    help="DCT will try to authenticate using each Domain given in this list.")
update.add_argument('--enable_ssl', type=str, required=False, help="Enable SSL or no.", choices=['true', 'false'])
update.add_argument('--truststore_filename', type=str, required=False,
                    help="File name of a truststore which can be used to validate the TLS certificate of the "
                         "LDAP server. The truststore must be available at /etc/config/certs/<truststore_filename>")
update.add_argument('--truststore_password', type=str, required=False,
                    help="Password for reading trustStore file provided in 'truststore_filename' property")
update.add_argument('--insecure_ssl', type=str, required=False,
                    help="Allow connections to the LDAP server over LDAPS without validating the TLS certificate",
                    choices=['true', 'false'])
update.add_argument('--unsafe_ssl_hostname_check', type=str, required=False,
                    help="Ignore validation of the name associated to the TLS certificate when connecting to the LDAP "
                         "server over LDAPS Setting this value must only be done if the TLS certificate of the server "
                         "does not match the hostname, and the TLS configuration of the server cannot be fixed",
                    choices=['true', 'false'])

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

# dct_base_url = "/is-saml-enabled"
dct_base_url = "/management/ldap-config"

if args.command == 'list':
    dct_simple_list("LDAP List", dct_base_url, "No LDAP defined.", args.format)

if args.command == 'validate':
    payload = {"username": args.username, "password": args.password}
    # dct_create(dct_base_url + "/validate", payload)
    resp = url_POST(dct_base_url + "/validate", payload)
    if resp.status_code == 200:
        print("Validation successful")
    else:
        dct_print_error(resp)
        sys.exit(1)

if args.command == 'update':
    update_saml_config(dct_base_url, args.enabled, args.auto_create_users, args.hostname, args.port, args.domains,
                       args.enable_ssl, args.truststore_filename, args.truststore_password, args.insecure_ssl,
                       args.unsafe_ssl_hostname_check)
