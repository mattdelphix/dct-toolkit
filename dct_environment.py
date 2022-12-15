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

# TODO Environment delete to be tested

# Environment functions
def environment_operation(base_url, env_id, ops):
    ops = ops.lower()
    if not any(x in ops for x in ["enable", "disable", "refresh"]):
        print("Wrong operation on Environment: " + ops)
        sys.exit(1)
    resp = url_POST(base_url + "/" + urllib.parse.quote(env_id) + "/" + ops, "")
    if resp.status_code == 200:
        return json.loads(resp.text)
    else:
        dct_print_error(resp)
        sys.exit(1)


# Init
parser = argparse.ArgumentParser(description='Delphix DCT Environment operations')
subparser = parser.add_subparsers(dest='command')

parser.add_argument('--version', action='version', version='%(prog)s 1.0')
parser.add_argument('--config', type=str, required=False, help="Config file")
parser.add_argument('--debug', type=int, required=False, help="Debug level [0-2]",choices=[0,1,2])

# define commands

# environment base commands
lst = subparser.add_parser('list')
search = subparser.add_parser('search')
view = subparser.add_parser('view')
delete = subparser.add_parser('delete')
disable = subparser.add_parser('disable')
enable = subparser.add_parser('enable')
refresh = subparser.add_parser('refresh')
# create environment commands
create_unix = subparser.add_parser('create_unix')
create_unix_cls = subparser.add_parser('create_unix_cls')
create_win_src = subparser.add_parser('create_win_src')
create_win_tgt = subparser.add_parser('create_win_tgt')
create_win_src_cls = subparser.add_parser('create_win_src_cls')
create_win_tgt_cls = subparser.add_parser('create_win_tgt_cls')
# update environment commands
update = subparser.add_parser('update_unix')
# tag command
tag_list = subparser.add_parser('tag_list')
tag_create = subparser.add_parser('tag_create')
tag_delete = subparser.add_parser('tag_delete')
tag_delete_all = subparser.add_parser('tag_delete_all')
# user command
user_list = subparser.add_parser('user_list')
user_create = subparser.add_parser('user_create')
user_create_pubkey = subparser.add_parser('user_create_pubkey')
user_create_kerb = subparser.add_parser('user_create_kerb')
user_create_cyark = subparser.add_parser('user_create_cyark')
user_create_hcorp = subparser.add_parser('user_create_hcorp')
user_update = subparser.add_parser('user_update')
user_update_pubkey = subparser.add_parser('user_update_pubkey')
user_update_kerb = subparser.add_parser('user_update_kerb')
user_update_cyark = subparser.add_parser('user_update_cyark')
user_update_hcorp = subparser.add_parser('user_update_hcorp')
user_delete = subparser.add_parser('user_delete')
user_setprimary = subparser.add_parser('user_setprimary')
# host command
host_delete = subparser.add_parser('host_delete')
host_create = subparser.add_parser('host_create')


# define list parms
lst.add_argument('--format', type=str, required=False, help="Type of output", choices=['json', 'report'])

# define view parms
view.add_argument('--id', type=str, required=True, help="Environment ID to be viewed")

# define enable parms
enable.add_argument('--id', type=str, required=True, help="Environment ID to be enabled")

# define disable parms
disable.add_argument('--id', type=str, required=True, help="Environment ID to be disabled")

# define refresh parms
refresh.add_argument('--id', type=str, required=True, help="Environment ID to be refreshed")

# define delete parms
delete.add_argument('--id', type=str, required=True, help="Environment ID to be deleted")

# define search parms
search.add_argument('--filter', type=str, required=True, help="Environment search string")
search.add_argument('--format', type=str, required=False, help="Type of output", choices=['json', 'report'])

# define user_list parms
user_list.add_argument('--id', type=str, required=True, help="Environment ID with users to be listed")
user_list.add_argument('--format', type=str, required=False, help="Type of output", choices=['json', 'report'])

# define tag_list parms
tag_list.add_argument('--id', type=str, required=True, help="Environment ID to be viewed")
tag_list.add_argument('--format', type=str, required=False, help="Type of output", choices=['json', 'report'])

# define tag_create params
tag_create.add_argument('--id', type=str, required=True, help="Environment ID to add tags to")
tag_create.add_argument('--tags', nargs='*', type=str, required=True, action=dct_parsetags,
                        help="Tags of the Environment in this format:  key=value key=value")
tag_delete.add_argument('--id', type=str, required=True, help="Environment ID to delete tags from")
tag_delete.add_argument('--key', type=str, required=True, help="Tags key of existing tag")

# define tag_delete_all params
tag_delete_all.add_argument('--id', type=str, required=True, help="Environment ID to delete tags from")

# define user_create parms
user_create.add_argument('--id', type=str, required=True, help="Environment ID to be updated")
user_create.add_argument('--username', type=str, required=True, help="Username to be added")
user_create.add_argument('--password', type=str, required=True, help="Password for the user")

# define user_create_pubkey parms
user_create_pubkey.add_argument('--id', type=str, required=True, help="Environment ID to be updated")
user_create_pubkey.add_argument('--username', type=str, required=True, help="Username to be added")

# define user_create_kerb parms
user_create_kerb.add_argument('--id', type=str, required=True, help="Environment ID to be updated")

# define user_create_cyark parms
user_create_cyark.add_argument('--id', type=str, required=True, help="Environment ID to be updated")
user_create_cyark.add_argument('--vault', type=str, required=True, help="Vault to be added")
user_create_cyark.add_argument('--username', type=str, required=True, help="Username to be added")

# define user_create_hcorp parms
user_create_hcorp.add_argument('--id', type=str, required=True, help="Environment ID to be updated")
user_create_hcorp.add_argument('--vault', type=str, required=True, help="Hashicorp Vault to be added")
user_create_hcorp.add_argument('--vault_username', type=str, required=True, help="Hashicorp Vault Username to be added")
user_create_hcorp.add_argument('--vault_engine', type=str, required=True, help="Hashicorp Vault engine to be added")
user_create_hcorp.add_argument('--vault_secret_path', type=str, required=True,
                               help="Hashicorp Vault Secret Path to be added")
user_create_hcorp.add_argument('--vault_user_key', type=str, required=True, help="Hashicorp Vault engine to be added")
user_create_hcorp.add_argument('--vault_secret_key', type=str, required=True,
                               help="Hashicorp Vault Secret key to be added")

# define user_update parms
user_update.add_argument('--id', type=str, required=True, help="Environment ID to be updated")
user_update.add_argument('--user_ref_id', type=str, required=True, help="User ref ID to update in environment")
user_update.add_argument('--username', type=str, required=True, help="Username to be added")
user_update.add_argument('--password', type=str, required=True, help="Password for the user")

# define user_update_pubkey parms
user_update_pubkey.add_argument('--id', type=str, required=True, help="Environment ID to be updated")
user_update_pubkey.add_argument('--user_ref_id', type=str, required=True, help="User ref ID to update in environment")
user_update_pubkey.add_argument('--username', type=str, required=True, help="Username to be added")

# define user_update_kerb parms
user_update_kerb.add_argument('--id', type=str, required=True, help="Environment ID to be updated")
user_update_kerb.add_argument('--user_ref_id', type=str, required=True, help="User ref ID to update in environment")

# define user_update_cyark parms
user_update_cyark.add_argument('--id', type=str, required=True, help="Environment ID to be updated")
user_update_cyark.add_argument('--user_ref_id', type=str, required=True, help="User ref ID to update in environment")
user_update_cyark.add_argument('--vault', type=str, required=True, help="Vault to be added")
user_update_cyark.add_argument('--username', type=str, required=True, help="Username to be added")

# define user_update_hcorp parms
user_update_hcorp.add_argument('--id', type=str, required=True, help="Environment ID to be updated")
user_update_hcorp.add_argument('--user_ref_id', type=str, required=True, help="User ref ID to update in environment")
user_update_hcorp.add_argument('--vault', type=str, required=True, help="Hashicorp Vault to be added")
user_update_hcorp.add_argument('--vault_username', type=str, required=True, help="Hashicorp Vault Username to be added")
user_update_hcorp.add_argument('--vault_engine', type=str, required=True, help="Hashicorp Vault engine to be added")
user_update_hcorp.add_argument('--vault_secret_path', type=str, required=True,
                               help="Hashicorp Vault Secret Path to be added")
user_update_hcorp.add_argument('--vault_user_key', type=str, required=True, help="Hashicorp Vault engine to be added")
user_update_hcorp.add_argument('--vault_secret_key', type=str, required=True,
                               help="Hashicorp Vault Secret key to be added")

# define user_delete params
user_delete.add_argument('--id', type=str, required=True, help="Environment ID to delete user from")
user_delete.add_argument('--user_ref_id', type=str, required=True, help="User ref ID to delete from environment")

# define user_setprimary parms
user_setprimary.add_argument('--id', type=str, required=True, help="Environment ID to be updated")
user_setprimary.add_argument('--user_ref_id', type=str, required=True,
                             help="User ref ID to be set primary in environment")

# define create_unix.parms
create_unix.add_argument('--name', type=str, required=True, help="Name of the environment")
create_unix.add_argument('--engine', type=str, required=True, help="ID of the engine")
create_unix.add_argument('--hostname', type=str, required=True, help="Hostname of the environment")
create_unix.add_argument('--port', type=str, required=False, help="SSH port of the environment", default='22')
create_unix.add_argument('--toolkit', type=str, required=True, help="Toolkit path of the environment")
create_unix.add_argument('--username', type=str, required=False, help="Username for the environment")
create_unix.add_argument('--password', type=str, required=False, help="Password for the user")
#--
create_unix.add_argument('--vault', type=str, required=False, help="Name of Cyberark or Hashicorp Vault")
create_unix.add_argument('--hcorp_engine', type=str, required=False, help="Hashicorp Vault engine")
create_unix.add_argument('--hcorp_secret_path', type=str, required=False,
                         help="Hashicorp Vault Secret path")
create_unix.add_argument('--hcorp_username', type=str, required=False, help="Hashicorp Vault Username")
create_unix.add_argument('--hcorp_secret_key', type=str, required=False,
                         help="Hashicorp Vault Secret key")
create_unix.add_argument('--cyark_query', type=str, required=False, help="Cyberark Vault Query String")
create_unix.add_argument('--kerberos', type=str, required=False, help="Kerberos Authentication",
                         choices=('True', 'False'), default='False')
create_unix.add_argument('--public_key', type=str, required=False, help="Use public key", choices=('True', 'False'),
                         default='False')
create_unix.add_argument('--nfs_addresses', type=str, required=False, help="NFS addresses for the environment separated by commas")
#--
create_unix.add_argument('--ase_username', type=str, required=False, help="ASE DB Username")
create_unix.add_argument('--ase_password', type=str, required=False, help="ASEW DB Password")
create_unix.add_argument('--ase_vault', type=str, required=False, help="ASE Name of Cyberark or Hashicorp Vault")
create_unix.add_argument('--ase_hcorp_engine', type=str, required=False, help="ASE Hashicorp Vault engine")
create_unix.add_argument('--ase_hcorp_secret_path', type=str, required=False,
                         help="ASE Hashicorp Vault Secret path")
create_unix.add_argument('--ase_hcorp_username', type=str, required=False, help="ASE Hashicorp Vault Username")
create_unix.add_argument('--ase_hcorp_secret_key', type=str, required=False,
                         help="ASE Hashicorp Vault Secret key")
create_unix.add_argument('--ase_cyark_query', type=str, required=False, help="ASE Cyberark Vault Query String")
create_unix.add_argument('--ase_kerberos', type=str, required=False, help="ASE Kerberos Authentication",
                         choices=('True', 'False'), default='False')
#--
create_unix.add_argument('--java', type=str, required=False, help="Java home")
create_unix.add_argument('--dsp_k_path', type=str, required=False, help="DSP Keystore path")
create_unix.add_argument('--dsp_k_password', type=str, required=False, help="DSP Keystore password")
create_unix.add_argument('--dsp_k_alias', type=str, required=False, help="DSP Keystore alias")
create_unix.add_argument('--dsp_t_path', type=str, required=False, help="DSP Truststore path")
create_unix.add_argument('--dsp_t_password', type=str, required=False, help="DSP Truststore password")
#--
create_unix.add_argument('--description', type=str, required=True, help="Description of the environment")
create_unix.add_argument('--tags', nargs='*', type=str, required=False, action=dct_parsetags,
                         help="Tags of the Environment in this format:  key=value key=value")

# define create_unix_cls.parms
create_unix_cls.add_argument('--name', type=str, required=True, help="Name of the environment")
create_unix_cls.add_argument('--engine', type=str, required=True, help="ID of the engine")
create_unix_cls.add_argument('--cluster_home', type=str, required=True, help="Cluster Home")
create_unix_cls.add_argument('--hostname', type=str, required=True, help="Hostname of the environment")
create_unix_cls.add_argument('--port', type=str, required=False, help="SSH port of the environment", default='22')
create_unix_cls.add_argument('--toolkit', type=str, required=True, help="Toolkit path of the environment")
create_unix_cls.add_argument('--username', type=str, required=False, help="Username for the environment")
create_unix_cls.add_argument('--password', type=str, required=False, help="Password for the user")
#--
create_unix_cls.add_argument('--vault', type=str, required=False, help="Name of Cyberark or Hashicorp Vault")
create_unix_cls.add_argument('--hcorp_engine', type=str, required=False, help="Hashicorp Vault engine")
create_unix_cls.add_argument('--hcorp_secret_path', type=str, required=False,
                         help="Hashicorp Vault Secret path")
create_unix_cls.add_argument('--hcorp_username', type=str, required=False, help="Hashicorp Vault Username")
create_unix_cls.add_argument('--hcorp_secret_key', type=str, required=False,
                         help="Hashicorp Vault Secret key")
create_unix_cls.add_argument('--cyark_query', type=str, required=False, help="Cyberark Vault Query String")
create_unix_cls.add_argument('--kerberos', type=str, required=False, help="Kerberos Authentication",
                         choices=('True', 'False'), default='False')
create_unix_cls.add_argument('--public_key', type=str, required=False, help="Use public key", choices=('True', 'False'),
                         default='False')
create_unix_cls.add_argument('--nfs_addresses', type=str, required=False, help="NFS addresses for the environment separated by commas")
#--
create_unix_cls.add_argument('--java', type=str, required=False, help="Java home")
create_unix_cls.add_argument('--dsp_k_path', type=str, required=False, help="DSP Keystore path")
create_unix_cls.add_argument('--dsp_k_password', type=str, required=False, help="DSP Keystore password")
create_unix_cls.add_argument('--dsp_k_alias', type=str, required=False, help="DSP Keystore alias")
create_unix_cls.add_argument('--dsp_t_path', type=str, required=False, help="DSP Truststore path")
create_unix_cls.add_argument('--dsp_t_password', type=str, required=False, help="DSP Truststore password")
#--
create_unix_cls.add_argument('--description', type=str, required=True, help="Description of the environment")
create_unix_cls.add_argument('--tags', nargs='*', type=str, required=False, action=dct_parsetags,
                         help="Tags of the Environment in this format:  key=value key=value")

# define create_win_src parms
create_win_src.add_argument('--name', type=str, required=True, help="Name of the environment")
create_win_src.add_argument('--engine', type=str, required=True, help="ID of the engine")
create_win_src.add_argument('--hostname', type=str, required=True, help="Hostname of the environment")
create_win_src.add_argument('--staging', type=str, required=True, help="ID of the staging environment")
create_win_src.add_argument('--username', type=str, required=False, help="Username for the environment")
create_win_src.add_argument('--password', type=str, required=False, help="Password for the user")
create_win_src.add_argument('--vault', type=str, required=False, help="Name of Cyberark or Hashicorp Vault")
create_win_src.add_argument('--hcorp_engine', type=str, required=False, help="Hashicorp Vault engine")
create_win_src.add_argument('--hcorp_secret_path', type=str, required=False,
                         help="Hashicorp Vault Secret path")
create_win_src.add_argument('--hcorp_username', type=str, required=False, help="Hashicorp Vault Username")
create_win_src.add_argument('--hcorp_secret_key', type=str, required=False,
                         help="Hashicorp Vault Secret key")
create_win_src.add_argument('--cyark_query', type=str, required=False, help="Cyberark Vault Query String")
create_win_src.add_argument('--description', type=str, required=True, help="Description of the environment")
create_win_src.add_argument('--tags', nargs='*', type=str, required=False, action=dct_parsetags,
                            help="Tags of the Environment in this format:  key=value key=value")

# define create_win_tgt parms
create_win_tgt.add_argument('--name', type=str, required=True, help="Name of the environment")
create_win_tgt.add_argument('--engine', type=str, required=True, help="ID of the engine")
create_win_tgt.add_argument('--hostname', type=str, required=True, help="Hostname of the environment")
create_win_tgt.add_argument('--connport', type=str, required=False, help="Connection port - default 9100", default="9100")
create_win_tgt.add_argument('--connauthkey', type=str, required=False, help="Connection auth key")
create_win_tgt.add_argument('--username', type=str, required=False, help="Username for the environment")
create_win_tgt.add_argument('--password', type=str, required=False, help="Password for the user")
#--
create_win_tgt.add_argument('--vault', type=str, required=False, help="Name of Cyberark or Hashicorp Vault")
create_win_tgt.add_argument('--hcorp_engine', type=str, required=False, help="Hashicorp Vault engine")
create_win_tgt.add_argument('--hcorp_secret_path', type=str, required=False,
                         help="Hashicorp Vault Secret path")
create_win_tgt.add_argument('--hcorp_username', type=str, required=False, help="Hashicorp Vault Username")
create_win_tgt.add_argument('--hcorp_secret_key', type=str, required=False,
                         help="Hashicorp Vault Secret key")
create_win_tgt.add_argument('--cyark_query', type=str, required=False, help="Cyberark Vault Query String")
create_win_tgt.add_argument('--java', type=str, required=False, help="Java home")
create_win_tgt.add_argument('--dsp_k_path', type=str, required=False, help="DSP Keystore path")
create_win_tgt.add_argument('--dsp_k_password', type=str, required=False, help="DSP Keystore password")
create_win_tgt.add_argument('--dsp_k_alias', type=str, required=False, help="DSP Keystore alias")
create_win_tgt.add_argument('--dsp_t_path', type=str, required=False, help="DSP Truststore path")
create_win_tgt.add_argument('--dsp_t_password', type=str, required=False, help="DSP Truststore password")
#--
create_win_tgt.add_argument('--description', type=str, required=True, help="Description of the environment")
create_win_tgt.add_argument('--tags', nargs='*', type=str, required=False, action=dct_parsetags,
                            help="Tags of the Environment in this format:  key=value key=value")

# define create_win_src_cls parms
create_win_src_cls.add_argument('--name', type=str, required=True, help="Name of the environment")
create_win_src_cls.add_argument('--engine', type=str, required=True, help="ID of the engine")
create_win_src_cls.add_argument('--hostname', type=str, required=True, help="Hostname of the environment")
create_win_src_cls.add_argument('--staging', type=str, required=True, help="ID of the staging environment")
create_win_src_cls.add_argument('--username', type=str, required=False, help="Username for the environment")
create_win_src_cls.add_argument('--password', type=str, required=False, help="Password for the user")
create_win_src_cls.add_argument('--vault', type=str, required=False, help="Name of Cyberark or Hashicorp Vault")
create_win_src_cls.add_argument('--hcorp_engine', type=str, required=False, help="Hashicorp Vault engine")
create_win_src_cls.add_argument('--hcorp_secret_path', type=str, required=False,
                         help="Hashicorp Vault Secret path")
create_win_src_cls.add_argument('--hcorp_username', type=str, required=False, help="Hashicorp Vault Username")
create_win_src_cls.add_argument('--hcorp_secret_key', type=str, required=False,
                         help="Hashicorp Vault Secret key")
create_win_src_cls.add_argument('--cyark_query', type=str, required=False, help="Cyberark Vault Query String")
create_win_src_cls.add_argument('--description', type=str, required=True, help="Description of the environment")
create_win_src_cls.add_argument('--tags', nargs='*', type=str, required=False, action=dct_parsetags,
                            help="Tags of the Environment in this format:  key=value key=value")

# define create_win_tgt_cls parms
create_win_tgt_cls.add_argument('--name', type=str, required=True, help="Name of the environment")
create_win_tgt_cls.add_argument('--engine', type=str, required=True, help="ID of the engine")
create_win_tgt_cls.add_argument('--hostname', type=str, required=True, help="Hostname of the environment")
create_win_tgt_cls.add_argument('--staging', type=str, required=True, help="ID of the staging environment")
create_win_tgt_cls.add_argument('--username', type=str, required=False, help="Username for the environment")
create_win_tgt_cls.add_argument('--password', type=str, required=False, help="Password for the user")
#--
create_win_tgt_cls.add_argument('--vault', type=str, required=False, help="Name of Cyberark or Hashicorp Vault")
create_win_tgt_cls.add_argument('--hcorp_engine', type=str, required=False, help="Hashicorp Vault engine")
create_win_tgt_cls.add_argument('--hcorp_secret_path', type=str, required=False,
                         help="Hashicorp Vault Secret path")
create_win_tgt_cls.add_argument('--hcorp_username', type=str, required=False, help="Hashicorp Vault Username")
create_win_tgt_cls.add_argument('--hcorp_secret_key', type=str, required=False,
                         help="Hashicorp Vault Secret key")
create_win_tgt_cls.add_argument('--cyark_query', type=str, required=False, help="Cyberark Vault Query String")
create_win_tgt_cls.add_argument('--description', type=str, required=True, help="Description of the environment")
create_win_tgt_cls.add_argument('--tags', nargs='*', type=str, required=False, action=dct_parsetags,
                            help="Tags of the Environment in this format:  key=value key=value")

# define host_delete parms
host_delete.add_argument('--id', type=str, required=True, help="Environment ID where host is to be deleted")
host_delete.add_argument('--hostid', type=str, required=True, help="Host ID to be deleted")

# define host_create.parms
host_create.add_argument('--name', type=str, required=True, help="Name of the environment")
host_create.add_argument('--address', type=str, required=True, help="Host IP address or hostname")
host_create.add_argument('--nfs_addresses', type=str, required=False, help="NFS addresses for the environment separated by commas")
host_create.add_argument('--port', type=str, required=False, help="SSH port of the environment", default='22')
host_create.add_argument('--privilege', type=str, required=False, help="Privilege elevation profile reference")
host_create.add_argument('--dsp_k_alias', type=str, required=False, help="DSP Keystore alias")
host_create.add_argument('--dsp_k_password', type=str, required=False, help="DSP Keystore password")
host_create.add_argument('--dsp_k_path', type=str, required=False, help="DSP Keystore path")
host_create.add_argument('--dsp_t_password', type=str, required=False, help="DSP Truststore password")
host_create.add_argument('--dsp_t_path', type=str, required=False, help="DSP Truststore path")
host_create.add_argument('--java', type=str, required=False, help="Java home")
host_create.add_argument('--toolkit', type=str, required=False, help="Toolkit path of the environment")
host_create.add_argument('--ora_jdbc_pwd', type=str, required=False, help="Oracle jdbc keystore password")
host_create.add_argument('--ora_tde_path', type=str, required=False, help="Oracle tde keystores root path")
# ssh verif
host_create.add_argument('--ssh_name', type=str, required=False, help="Ssh verification name")
host_create.add_argument('--ssh_type', type=str, required=False, help="Ssh verification type")
host_create.add_argument('--ssh_rawkey', type=str, required=False, help="Ssh verification raw key")
host_create.add_argument('--ssh_fp_type', type=str, required=False, help="Ssh verification fingeprint type")
host_create.add_argument('--ssh_fp', type=str, required=False, help="Ssh verification fingeprint type")

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

dct_base_url = "/environments"

if args.command == 'list':
    rs = dct_search("Environment List", dct_base_url, None, "No Environments defined.", args.format)
    dct_print_json(rs)

if args.command == 'view':
    rs = dct_view_by_id(dct_base_url, args.id)
    dct_print_json(rs)

if args.command == 'user_create':
    payload = {"username": args.username, "password": args.password}
    rs = dct_post_by_id(dct_base_url, args.id, payload, "users")
    if rs.status_code == 204:
        print("Created '" + args.username + "' for Environment - ID=" + args.id)
    else:
        dct_print_error(rs)
        sys.exit(1)


if args.command == 'user_create_pubkey':
    payload = {"use_engine_public_key": "true", "username": args.username}
    rs = dct_post_by_id(dct_base_url, args.id, payload, "users")
    if rs.status_code == 204:
        print("Set '" + args.username + "' for Environment - ID=" + args.id)
    else:
        dct_print_error(rs)
        sys.exit(1)


if args.command == 'user_create_kerb':
    payload = {"use_kerberos_authentication": "true"}
    rs = dct_post_by_id(dct_base_url, args.id, payload, "users")
    if rs.status_code == 204:
        print("Set Kerberos for Environment - ID=" + args.id)
    else:
        dct_print_error(rs)
        sys.exit(1)


if args.command == 'user_create_cyark':
    payload = {"vault": args.vault, "vault_username": args.username,
               "cyberark_vault_query_string": "Safe=Test;Folder=Test;Object=Test"}
    rs = dct_post_by_id(dct_base_url, args.id, payload, "users")
    if rs.status_code == 204:
        print("Set CyberArk '" + args.username + "' for Environment - ID=" + args.id)
    else:
        dct_print_error(rs)
        sys.exit(1)


if args.command == 'user_create_hcorp':
    payload = {"vault": args.vault, "vault_username": args.username, "hashicorp_vault_engine": args.vault_engine,
               "hashicorp_vault_secret_path": args.vault_secret_path,
               "hashicorp_vault_username_key": args.vault_user_key, "hashicorp_vault_secret_key": args.vault_secret_key}
    rs = dct_post_by_id(dct_base_url, args.id, payload, "users")
    if rs.status_code == 204:
        print("Set Hashicorp '" + args.username + "' for Environment - ID=" + args.id)
    else:
        dct_print_error(rs)
        sys.exit(1)


if args.command == 'user_update':
    payload = {"username": args.username, "password": args.password}
    rs = dct_update_ref_by_id(dct_base_url, args.id, payload, "users", args.user_ref_id)
    if rs.status_code == 204:
        print("Updated user '" + args.user_ref_id + "' for Environment - ID=" + args.id)
    else:
        dct_print_error(rs)
        sys.exit(1)


if args.command == 'user_update_pubkey':
    payload = {"use_engine_public_key": "true", "username": args.username}
    rs = dct_update_ref_by_id(dct_base_url, args.id, payload, "users", args.user_ref_id)
    if rs.status_code == 204:
        print("Updated user '" + args.user_ref_id + "' for Environment - ID=" + args.id)
    else:
        dct_print_error(rs)
        sys.exit(1)


if args.command == 'user_update_kerb':
    payload = {"use_kerberos_authentication": "true"}
    rs = dct_update_ref_by_id(dct_base_url, args.id, payload, "users", args.user_ref_id)
    if rs.status_code == 204:
        print("Updated Kerberos for Environment - ID=" + args.id)
    else:
        dct_print_error(rs)
        sys.exit(1)


if args.command == 'user_update_cyark':
    payload = {"vault": args.vault, "vault_username": args.username,
               "cyberark_vault_query_string": "Safe=Test;Folder=Test;Object=Test"}
    rs = dct_update_ref_by_id(dct_base_url, args.id, payload, "users", args.user_ref_id)
    if rs.status_code == 204:
        print("Updated CyberArk '" + args.user_ref_id + "' for Environment - ID=" + args.id)
    else:
        dct_print_error(rs)
        sys.exit(1)


if args.command == 'user_update_hcorp':
    payload = {"vault": args.vault, "vault_username": args.username, "hashicorp_vault_engine": args.vault_engine,
               "hashicorp_vault_secret_path": args.vault_secret_path,
               "hashicorp_vault_username_key": args.vault_user_key, "hashicorp_vault_secret_key": args.vault_secret_key}
    rs = dct_update_ref_by_id(dct_base_url, args.id, payload, "users", args.user_ref_id)
    if rs.status_code == 204:
        print("Updated Hashicorp '" + args.user_ref_id + "' for Environment - ID=" + args.id)
    else:
        dct_print_error(rs)
        sys.exit(1)


if args.command == 'tag_list':
    rs = dct_list_by_id(dct_base_url, args.id, "/tags", args.format)
    dct_print_json(rs)

if args.command == 'user_list':
    rs = dct_list_by_id(dct_base_url, args.id, "/users", args.format)
    dct_print_json(rs)

if args.command == 'search':
    rs = dct_search("Environment List", dct_base_url, args.filter, "No Environments match the search criteria.",
                    args.format)
    dct_print_json(rs)

if args.command == 'refresh':
    print("Processing Environment refresh ID=" + args.id)
    rs = environment_operation(dct_base_url, args.id, args.command)
    dct_job_monitor(rs['job']['id'])

if args.command == 'enable':
    print("Processing Environment enable ID=" + args.id)
    rs = environment_operation(dct_base_url, args.id, args.command)
    dct_job_monitor(rs['job']['id'])

if args.command == 'disable':
    print("Processing Environment disable ID=" + args.id)
    rs = environment_operation(dct_base_url, args.id, args.command)
    dct_job_monitor(rs['job']['id'])

if args.command == 'delete':
    print("Processing Environment delete ID=" + args.id)
    rs = dct_delete_by_id(dct_base_url, "Deleted Environment", args.id)
    dct_job_monitor(rs['job']['id'])

if args.command == 'tag_create':
    payload = {"tags": args.tags}
    rs = dct_post_by_id(dct_base_url, args.id, payload, "tags")
    if rs.status_code == 201:
        print("Created tags for Environment - ID=" + args.id)
    else:
        dct_print_error(rs)
        sys.exit(1)


if args.command == 'tag_delete':
    payload = {"key": args.key}
    rs = dct_post_by_id(dct_base_url, args.id, payload, "tags/delete")
    if rs.status_code == 204:
        print("Deleted tag '" + args.key + "' for Environment - ID=" + args.id)
    else:
        dct_print_error(rs)
        sys.exit(1)


if args.command == 'tag_delete_all':
    rs = dct_post_by_id(dct_base_url, args.id, None, "tags/delete")
    if rs.status_code == 204:
        print("Deleted all tags for Environment - ID=" + args.id)
    else:
        dct_print_error(rs)
        sys.exit(1)


if args.command == 'user_delete':
    print("Processing user'" + args.user_ref_id + "' delete for Environment ID=" + args.id)
    rs = dct_delete_ref_by_id(dct_base_url, "Deleted Environment", args.id, "users", args.user_ref_id)
    dct_job_monitor(rs['job']['id'])

if args.command == 'user_setprimary':
    print("Setting primary user'" + args.user_ref_id + "' delete for Environment ID=" + args.id)
    rs = dct_update_ref_by_id(dct_base_url, "Set Primary user", args.id, "users", args.user_ref_id)
    dct_job_monitor(rs['job']['id'])

if args.command == 'create_unix':
    # build list of NFS addresses
    nfs_list = args.nfs_addresses.split(",")
    payload = {
        "name": args.name,
        "engine_id": args.engine,
        "os_name": "UNIX",
        "hostname": args.hostname,
        "ssh_port": args.port,
        "toolkit_path": args.toolkit,
        "username": args.username,
        "password": args.password,
        "vault": args.vault,
        "hashicorp_vault_engine": args.hcorp_engine,
        "hashicorp_vault_secret_path": args.hcorp_path,
        "hashicorp_vault_username_key": args.hcorp_username,
        "hashicorp_vault_secret_key": args.hcorp_secret_key,
        "cyberark_vault_query_string": args.cyark_query,
        "use_kerberos_authentication": args.kerberos,
        "use_engine_public_key": args.public_key,
        "nfs_addresses": nfs_list,
        "ase_db_username": args.ase_username,
        "ase_db_password": args.ase_password,
        "ase_db_vault": args.ase_vault,
        "ase_db_hashicorp_vault_engine": args.ase_hcorp_engine,
        "ase_db_hashicorp_vault_secret_path": args.ase_hcorp_path,
        "ase_db_hashicorp_vault_username_key": args.ase_hcorp_username,
        "ase_db_hashicorp_vault_secret_key": args.ase_hcorp_secret_key,
        "ase_db_cyberark_vault_query_string": args.ase_cyark_query,
        "ase_db_use_kerberos_authentication": args.ase_kerberos,
        "java_home": args.java,
        "dsp_keystore_path": args.dsp_k_path,
        "dsp_keystore_password": args.dsp_k_password,
        "dsp_keystore_alias": args.dsp_k_alias,
        "dsp_truststore_path": args.dsp_t_path,
        "dsp_truststore_password": args.dsp_t_password,
        "description": args.description,
        "tags": args.tags
    }
    rs = dct_create(dct_base_url, payload)
    dct_job_monitor(rs['job']['id'])

if args.command == 'create_unix_cls':
    # build list of NFS addresses
    nfs_list = args.nfs_addresses.split(",")
    payload = {
        "name": args.name,
        "engine_id": args.engine,
        "os_name": "UNIX",
        "is_cluster": True,
        "cluster_home": args.cluster_home,
        "hostname": args.hostname,
        "ssh_port": args.port,
        "toolkit_path": args.toolkit,
        "username": args.username,
        "password": args.password,
        "vault": args.vault,
        "hashicorp_vault_engine": args.hcorp_engine,
        "hashicorp_vault_secret_path": args.hcorp_path,
        "hashicorp_vault_username_key": args.hcorp_username,
        "hashicorp_vault_secret_key": args.hcorp_secret_key,
        "cyberark_vault_query_string": args.cyark_query,
        "use_kerberos_authentication": args.kerberos,
        "use_engine_public_key": args.public_key,
        "nfs_addresses": nfs_list,
        "java_home": args.java,
        "dsp_keystore_path": args.dsp_k_path,
        "dsp_keystore_password": args.dsp_k_password,
        "dsp_keystore_alias": args.dsp_k_alias,
        "dsp_truststore_path": args.dsp_t_path,
        "dsp_truststore_password": args.dsp_t_password,
        "description": args.description,
        "tags": args.tags
    }
    rs = dct_create(dct_base_url, payload)
    dct_job_monitor(rs['job']['id'])

if args.command == 'create_win_src':
    payload = {
        "name": args.name,
        "engine_id": args.engine,
        "os_name": "WINDOWS",
        "hostname": args.hostname,
        "staging_environment": args.staging,
        "username": args.username,
        "password": args.password,
        "vault": args.vault,
        "hashicorp_vault_engine": args.hcorp_engine,
        "hashicorp_vault_secret_path": args.hcorp_path,
        "hashicorp_vault_username_key": args.hcorp_username,
        "hashicorp_vault_secret_key": args.hcorp_secret_key,
        "cyberark_vault_query_string": args.cyark_query,
        "description": args.description,
        "tags": args.tags
    }
    rs = dct_create(dct_base_url, payload)
    dct_job_monitor(rs['job']['id'])

if args.command == 'create_win_tgt':
    payload = {
        "name": args.name,
        "engine_id": args.engine,
        "os_name": "WINDOWS",
        "hostname": args.hostname,
        "connector_port": args.connport,
        "connector_authentication_key": args.connauthkey,
        "username": args.username,
        "password": args.password,
        "vault": args.vault,
        "hashicorp_vault_engine": args.hcorp_engine,
        "hashicorp_vault_secret_path": args.hcorp_path,
        "hashicorp_vault_username_key": args.hcorp_username,
        "hashicorp_vault_secret_key": args.hcorp_secret_key,
        "cyberark_vault_query_string": args.cyark_query,
        "java_home": args.java,
        "dsp_keystore_path": args.dsp_k_path,
        "dsp_keystore_password": args.dsp_k_password,
        "dsp_keystore_alias": args.dsp_k_alias,
        "dsp_truststore_path": args.dsp_t_path,
        "dsp_truststore_password": args.dsp_t_password,
        "description": args.description,
        "tags": args.tags
    }
    rs = dct_create(dct_base_url, payload)
    dct_job_monitor(rs['job']['id'])

if args.command == 'create_win_src_cls':
    payload = {
        "name": args.name,
        "engine_id": args.engine,
        "os_name": "WINDOWS",
        "is_cluster": True,
        "hostname": args.hostname,
        "staging_environment": args.staging_env,
        "username": args.username,
        "password": args.password,
        "vault": args.vault,
        "hashicorp_vault_engine": args.hcorp_engine,
        "hashicorp_vault_secret_path": args.hcorp_path,
        "hashicorp_vault_username_key": args.hcorp_username,
        "hashicorp_vault_secret_key": args.hcorp_secret_key,
        "cyberark_vault_query_string": args.cyark_query,
        "is_target": False,
        "description": args.description,
        "tags": args.tags
    }
    rs = dct_create(dct_base_url, payload)
    dct_job_monitor(rs['job']['id'])

if args.command == 'create_win_tgt_cls':
    payload = {
        "name": args.name,
        "engine_id": args.engine,
        "os_name": "WINDOWS",
        "is_cluster": True,
        "hostname": args.hostname,
        "staging_environment": args.staging_env,
        "username": args.username,
        "password": args.password,
        "vault": args.vault,
        "hashicorp_vault_engine": args.hcorp_engine,
        "hashicorp_vault_secret_path": args.hcorp_path,
        "hashicorp_vault_username_key": args.hcorp_username,
        "hashicorp_vault_secret_key": args.hcorp_secret_key,
        "cyberark_vault_query_string": args.cyark_query,
        "is_target": True,
        "description": args.description,
        "tags": args.tags
    }
    rs = dct_create(dct_base_url, payload)
    dct_job_monitor(rs['job']['id'])

if args.command == 'host_create':
    # build list of NFS addresses
    nfs_list = args.nfs_addresses.split(",")
    payload = {
        "name": args.name,
        "nfs_addresses": nfs_list,
        "ssh_port": args.port,
        "privilege_elevation_profile_reference": args.privilege,
        "java_home": args.java,
        "dsp_keystore_alias": args.dsp_k_alias,
        "dsp_keystore_password": args.dsp_k_password,
        "dsp_keystore_path": args.dsp_k_path,
        "dsp_truststore_password": args.dsp_t_password,
        "dsp_truststore_path": args.dsp_t_path,
        "toolkit_path": args.toolkit,
        "oracle_jdbc_keystore_password": args.ora_jdbc_pwd,
        "oracle_tde_keystores_root_path": args.ora_tde_path,
        "ssh_verification_strategy": {
            "name": args.ssh_name,
            "key_type": args.ssh_type,
            "raw_key": args.ssh_rawkey,
            "fingerprint_type": args.ssh_fp_type,
            "fingerprint": args.ssh_fp
        },
        "virtual_ips": [
            {
                "ip": args.vip_address,
                "domain_name": args.vip_domain
            }
        ]
    }
    rs = dct_create(dct_base_url, payload)
    dct_job_monitor(rs['job']['id'])

if args.command == 'host_delete':
    rs = dct_delete_ref_by_id(dct_base_url, "Delete host", args.id, "hosts", args.hostid)
    if rs.status_code == 202:
        print("Deleted host '" + args.hostid + "' for Environment - ID=" + args.id)
    else:
        dct_print_error(rs)
        sys.exit(1)
