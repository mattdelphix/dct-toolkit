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


# VDB functions

# Init
parser = argparse.ArgumentParser(description='Delphix DCT VDB provisioning by snapshot')
subparser = parser.add_subparsers(dest='command')

parser.add_argument('--version', action='version', version='%(prog)s 1.0')
parser.add_argument('--config', type=str, required=False, help="Config file")
parser.add_argument('--debug', type=int, required=False, help="Debug level [0-2]",choices=[0,1,2])

# define commands
vdb_oracle = subparser.add_parser('oracle')
vdb_file = subparser.add_parser('file')

# define vdb_file parms
vdb_file.add_argument('--snapshot_id', type=str, required=True, help="Snapshot ID to be used for VDB provisioning")
vdb_file.add_argument('--engine', type=str, required=True, help="Engine ID to be used for VDB provisioning")
vdb_file.add_argument('--source', type=str, required=True, help="Source data ID to be used for VDB provisioning")
vdb_file.add_argument('--target_group', type=str, required=True, help="Target group ID to be used for VDB provisioning")
vdb_file.add_argument('--name', type=str, required=True, help="Name of the VDB to be provisioned")
vdb_file.add_argument('--os_username', type=str, required=True, help="OS user")
vdb_file.add_argument('--os_password', type=str, required=True, help="OS password")
vdb_file.add_argument('--environment_id', type=str, required=True, help="Environment ID for the VDB")
vdb_file.add_argument('--environment_user_id', type=str, required=True, help="Environment User Name")
vdb_file.add_argument('--auto_select_repository', required=False, help="Choose repository automatically", action="store_true")
vdb_file.add_argument('--vdb_restart', required=False, help="VDB will be restarted automatically?", action="store_true")
vdb_file.add_argument('--mount_point', type=str, required=True, help="Mount point to be created on target host")
# Policies
vdb_file.add_argument('--snapshot_policy_id', type=str, required=False, help="Snapshot policy ID to be used for VDB provisioning")
vdb_file.add_argument('--retention_policy_id', type=str, required=False, help="Retention policy ID to be used for VDB provisioning")

# Hooks
vdb_file.add_argument('--pre_refresh_name', type=str, required=False, help="Pre-refresh hook name", default="pre_refresh_command")
vdb_file.add_argument('--pre_refresh_command', type=str, required=False, help="Pre-refresh hook command")
vdb_file.add_argument('--pre_refresh_shell', type=str, required=False, help="Pre-refresh hook shell")

vdb_file.add_argument('--post_refresh_name', type=str, required=False, help="Post-refresh hook name", default="post_refresh_command")
vdb_file.add_argument('--post_refresh_command', type=str, required=False, help="Post-refresh hook command")
vdb_file.add_argument('--post_refresh_shell', type=str, required=False, help="Post-refresh hook shell")

vdb_file.add_argument('--pre_rollback_name', type=str, required=False, help="Pre-rollback hook name", default="pre_rollback_command")
vdb_file.add_argument('--pre_rollback_command', type=str, required=False, help="Pre-rollback hook command")
vdb_file.add_argument('--pre_rollback_shell', type=str, required=False, help="Pre-rollback hook shell")

vdb_file.add_argument('--post_rollback_name', type=str, required=False, help="Post-rollback hook name", default="post_rollback_command")
vdb_file.add_argument('--post_rollback_command', type=str, required=False, help="Post-rollback hook command")
vdb_file.add_argument('--post_rollback_shell', type=str, required=False, help="Post-rollback hook shell")

vdb_file.add_argument('--configure_clone_name', type=str, required=False, help="Configure_clone hook name", default="configure_clone_command")
vdb_file.add_argument('--configure_clone_command', type=str, required=False, help="Configure_clone hook command")
vdb_file.add_argument('--configure_clone_shell', type=str, required=False, help="Configure_clone hook shell")

vdb_file.add_argument('--pre_snapshot_name', type=str, required=False, help="Pre-snapshot hook name", default="pre_snapshot_command")
vdb_file.add_argument('--pre_snapshot_command', type=str, required=False, help="Pre-snapshot hook command")
vdb_file.add_argument('--pre_snapshot_shell', type=str, required=False, help="Pre-snapshot hook shell")

vdb_file.add_argument('--post_snapshot_name', type=str, required=False, help="Post-snapshot hook name", default="post_snapshot_command")
vdb_file.add_argument('--post_snapshot_command', type=str, required=False, help="Post-snapshot hook command")
vdb_file.add_argument('--post_snapshot_shell', type=str, required=False, help="Post-snapshot hook shell")

vdb_file.add_argument('--pre_start_name', type=str, required=False, help="Pre-start hook name", default="pre_start_command")
vdb_file.add_argument('--pre_start_command', type=str, required=False, help="Pre-start hook command")
vdb_file.add_argument('--pre_start_shell', type=str, required=False, help="Pre-start hook shell")

vdb_file.add_argument('--post_start_name', type=str, required=False, help="Post-start hook name", default="post_start_command")
vdb_file.add_argument('--post_start_command', type=str, required=False, help="Post-start hook command")
vdb_file.add_argument('--post_start_shell', type=str, required=False, help="Post-start hook shell")

vdb_file.add_argument('--pre_stop_name', type=str, required=False, help="Pre-stop hook name", default="pre_stop_command")
vdb_file.add_argument('--pre_stop_command', type=str, required=False, help="Pre-stop hook command")
vdb_file.add_argument('--pre_stop_shell', type=str, required=False, help="Pre-stop hook shell")

vdb_file.add_argument('--post_stop_name', type=str, required=False, help="Post-stop hook name", default="post_stop_command")
vdb_file.add_argument('--post_stop_command', type=str, required=False, help="Post-stop hook command")
vdb_file.add_argument('--post_stop_shell', type=str, required=False, help="Post-stop hook shell")

vdb_file.add_argument('--tags', nargs='*', type=str, required=False, action=dct_parsetags,
                        help="Tags of the VDB in this format:  key=value key=value")

# define vdb_oracle parms
vdb_oracle.add_argument('--snapshot_id', type=str, required=True, help="Snapshot ID to be used for VDB provisioning")
vdb_oracle.add_argument('--engine', type=str, required=True, help="Engine ID to be used for VDB provisioning")
vdb_oracle.add_argument('--source', type=str, required=True, help="Source data ID to be used for VDB provisioning")
vdb_oracle.add_argument('--target_group', type=str, required=True, help="Target group ID to be used for VDB provisioning")
vdb_oracle.add_argument('--name', type=str, required=True, help="Name of the VDB to be provisioned")
vdb_oracle.add_argument('--database_name', type=str, required=True, help="Name of the Oracle DB to be provisioned")
vdb_oracle.add_argument('--os_username', type=str, required=True, help="OS user")
vdb_oracle.add_argument('--os_password', type=str, required=True, help="OS password")
vdb_oracle.add_argument('--environment_id', type=str, required=True, help="Environment ID for the VDB")
vdb_oracle.add_argument('--environment_user_id', type=str, required=True, help="Environment User Name")
vdb_oracle.add_argument('--auto_select_repository', required=True, help="Choose repository automatically", action="store_true")
vdb_oracle.add_argument('--cluster_node_ids', type=str, required=True, help="Cluster nodes ids")
vdb_oracle.add_argument('--vdb_restart', required=True, help="VDB will be restarted automatically?", action="store_true")
vdb_oracle.add_argument('--template_id', type=str, required=True, help="Template ID to be used for VDB provisioning")
vdb_oracle.add_argument('--aux_template_id', type=str, required=True, help="Aux Template ID to be used for VDB provisioning")
vdb_oracle.add_argument('--mount_point', type=str, required=True, help="Mount point to be created on target host")
# Policies
vdb_oracle.add_argument('--snapshot_policy_id', type=str, required=True, help="Snapshot policy ID to be used for VDB provisioning")
vdb_oracle.add_argument('--retention_policy_id', type=str, required=True, help="Retention policy ID to be used for VDB provisioning")

# Hooks
vdb_oracle.add_argument('--pre_refresh_name', type=str, required=False, help="Pre-refresh hook name", default="pre_refresh_command")
vdb_oracle.add_argument('--pre_refresh_command', type=str, required=False, help="Pre-refresh hook command")
vdb_oracle.add_argument('--pre_refresh_shell', type=str, required=False, help="Pre-refresh hook shell")

vdb_oracle.add_argument('--post_refresh_name', type=str, required=False, help="Post-refresh hook name", default="post_refresh_command")
vdb_oracle.add_argument('--post_refresh_command', type=str, required=False, help="Post-refresh hook command")
vdb_oracle.add_argument('--post_refresh_shell', type=str, required=False, help="Post-refresh hook shell")

vdb_oracle.add_argument('--pre_rollback_name', type=str, required=False, help="Pre-rollback hook name", default="pre_rollback_command")
vdb_oracle.add_argument('--pre_rollback_command', type=str, required=False, help="Pre-rollback hook command")
vdb_oracle.add_argument('--pre_rollback_shell', type=str, required=False, help="Pre-rollback hook shell")

vdb_oracle.add_argument('--post_rollback_name', type=str, required=False, help="Post-rollback hook name", default="post_rollback_command")
vdb_oracle.add_argument('--post_rollback_command', type=str, required=False, help="Post-rollback hook command")
vdb_oracle.add_argument('--post_rollback_shell', type=str, required=False, help="Post-rollback hook shell")

vdb_oracle.add_argument('--configure_clone_name', type=str, required=False, help="Configure_clone hook name", default="configure_clone_command")
vdb_oracle.add_argument('--configure_clone_command', type=str, required=False, help="Configure_clone hook command")
vdb_oracle.add_argument('--configure_clone_shell', type=str, required=False, help="Configure_clone hook shell")

vdb_oracle.add_argument('--pre_snapshot_name', type=str, required=False, help="Pre-snapshot hook name", default="pre_snapshot_command")
vdb_oracle.add_argument('--pre_snapshot_command', type=str, required=False, help="Pre-snapshot hook command")
vdb_oracle.add_argument('--pre_snapshot_shell', type=str, required=False, help="Pre-snapshot hook shell")

vdb_oracle.add_argument('--post_snapshot_name', type=str, required=False, help="Post-snapshot hook name", default="post_snapshot_command")
vdb_oracle.add_argument('--post_snapshot_command', type=str, required=False, help="Post-snapshot hook command")
vdb_oracle.add_argument('--post_snapshot_shell', type=str, required=False, help="Post-snapshot hook shell")

vdb_oracle.add_argument('--pre_start_name', type=str, required=False, help="Pre-start hook name", default="pre_start_command")
vdb_oracle.add_argument('--pre_start_command', type=str, required=False, help="Pre-start hook command")
vdb_oracle.add_argument('--pre_start_shell', type=str, required=False, help="Pre-start hook shell")

vdb_oracle.add_argument('--post_start_name', type=str, required=False, help="Post-start hook name", default="post_start_command")
vdb_oracle.add_argument('--post_start_command', type=str, required=False, help="Post-start hook command")
vdb_oracle.add_argument('--post_start_shell', type=str, required=False, help="Post-start hook shell")

vdb_oracle.add_argument('--pre_stop_name', type=str, required=False, help="Pre-stop hook name", default="pre_stop_command")
vdb_oracle.add_argument('--pre_stop_command', type=str, required=False, help="Pre-stop hook command")
vdb_oracle.add_argument('--pre_stop_shell', type=str, required=False, help="Pre-stop hook shell")

vdb_oracle.add_argument('--post_stop_name', type=str, required=False, help="Post-stop hook name", default="post_stop_command")
vdb_oracle.add_argument('--post_stop_command', type=str, required=False, help="Post-stop hook command")
vdb_oracle.add_argument('--post_stop_shell', type=str, required=False, help="Post-stop hook shell")

# Oracle parms
vdb_oracle.add_argument('--instance_name', type=str, required=True, help="Oracle instance name ID to be used for VDB provisioning")
vdb_oracle.add_argument('--unique_name', type=str, required=True, help="Oracle unique name to be used for VDB provisioning")
vdb_oracle.add_argument('--open_reset_logs', required=False, help="Oracle reset logs?", action="store_true")
vdb_oracle.add_argument('--online_log_size', type=str, required=True, help="Oracle online log size in GB to be used for VDB provisioning")
vdb_oracle.add_argument('--online_log_groups', type=str, required=True, help="Oracle online log groups to be used for VDB provisioning")
vdb_oracle.add_argument('--archive_log', required=False, help="Oracle reset logs?", action="store_true")
vdb_oracle.add_argument('--new_dbid', required=False, help="Oracle new dbid?", action="store_true")
vdb_oracle.add_argument('--file_mapping_rules', type=str, required=False, help="Oracle file mapping rules")
vdb_oracle.add_argument('--custom_env_vars', type=str, required=False, help="Custom environment variables")

vdb_oracle.add_argument('--tags', nargs='*', type=str, required=True, action=dct_parsetags,
                        help="Tags of the VDB in this format:  key=value key=value")


# define new_by_bookmark parms
#new_by_book.add_argument('--book_id', type=str, required=True, help="Bookmark ID to be used for provisioning")
#new_by_book.add_argument('--tags', nargs='*', type=str, required=True, action=dct_parsetags,
#                        help="Tags of the VDB in this format:  key=value key=value")

# define new_by_timestamp parms
#new_by_timestamp.add_argument('--timestamp', type=str, required=True, help="Timestamp ID to be used for rollback")
#new_by_timestamp.add_argument('--tags', nargs='*', type=str, required=True, action=dct_parsetags,
#                        help="Tags of the VDB in this format:  key=value key=value")


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

dct_base_url = "/vdbs/provision_by_snapshot"


if cfg.level == 1:
    print("Provisioning VDB by Snapshot")

if args.command == 'file':
    # mandatory fields
    payload = {"snapshot_id": args.snapshot_id,
               "mount_point": args.mount_point,
               "engine": args.engine,
               "source_id": args.source,
               "target_group_id": args.target_group,
               "name": args.name,
               "os_username": args.os_username,
               "os_password": args.os_password,
               "environment_id": args.environment_id,
               "environment_user_id": args.environment_user_id
               }

if args.vdb_restart:
    payload['vdb_restart'] = True
else:
    payload['vdb_restart'] = False

if args.auto_select_repository:
    payload['auto_select_repository'] = True

if args.snapshot_policy_id:
    payload['snapshot_policy_id'] = args.snapshot_policy_id

if args.retention_policy_id:
    payload['snapshot_retention_id'] = args.retention_policy_id


if args.pre_refresh_command:
    payload['pre_refresh_name'] = args.pre_refresh_command
    payload['pre_refresh_command'] = args.pre_refresh_command
    payload['pre_refresh_shell'] = args.pre_refresh_shell

if args.post_refresh_command:
    payload['pre_refresh_name'] = args.post_refresh_name
    payload['pre_refresh_command'] = args.post_refresh_command
    payload['pre_refresh_shell'] = args.post_refresh_shell

if args.pre_rollback_command:
    payload['pre_rollback_name'] = args.pre_rollback_name
    payload['pre_rollback_command'] = args.pre_rollback_command
    payload['pre_rollback_shell'] = args.pre_rollback_shell

if args.post_rollback_command:
    payload['pre_rollback_name'] = args.post_rollback_name
    payload['pre_rollback_command'] = args.post_rollback_command
    payload['pre_rollback_shell'] = args.post_rollbck_shell

if args.configure_clone_command:
    payload['configure_clone_name'] = args.configure_clone_name
    payload['configure_clone_command'] = args.configure_clone_command
    payload['configure_clone_shell'] = args.configure_clone_shell

if args.pre_snapshot_command:
    payload['pre_snapshot_name'] = args.pre_snapshot_name
    payload['pre_snapshot_command'] = args.pre_snapshot_command
    payload['pre_snapshot_shell'] = args.pre_snapshot_shell

if args.post_snapshot_command:
    payload['pre_snapshot_name'] = args.post_snapshot_name
    payload['pre_snapshot_command'] = args.post_snapshot_command
    payload['pre_snapshot_shell'] = args.post_rollbck_shell

if args.pre_start_command:
    payload['pre_start_name'] = args.pre_start_name
    payload['pre_start_command'] = args.pre_start_command
    payload['pre_start_shell'] = args.pre_start_shell

if args.post_start_command:
    payload['pre_start_name'] = args.post_start_name
    payload['pre_start_command'] = args.post_start_command
    payload['pre_start_shell'] = args.post_rollbck_shell

if args.pre_stop_command:
    payload['pre_stop_name'] = args.pre_stop_name
    payload['pre_stop_command'] = args.pre_stop_command
    payload['pre_stop_shell'] = args.pre_stop_shell

if args.post_stop_command:
    payload['pre_stop_name'] = args.post_stop_name
    payload['pre_stop_command'] = args.post_stop_command
    payload['pre_stop_shell'] = args.post_rollbck_shell

if args.tags:
    payload['tags'] = json.loads(args.tags)

dct_print_json_formatted(payload)
#sys.exit(0)
resp = url_POST(dct_base_url, payload)
if resp.status_code == 200:
    dct_job_monitor(resp['job']['id'])
else:
    dct_print_error(resp)
    sys.exit(1)
