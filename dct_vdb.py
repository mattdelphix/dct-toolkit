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

#TODO need to clarify how to use refresh_by_timestamp

import argparse

from helpers import *


# VDB functions
def vdb_operation(base_url, vdb_id, ops):
    ops = ops.lower()
    if not any(x in ops for x in ["enable", "disable", "stop", "start","snapshot"]):
        print("Error: Wrong operation on VDB: " + ops)
        sys.exit(1)
    payload = ""
    if ops == "enable":
        payload = {"attempt_start": "true"}
    if ops == "disable":
        payload = {"attempt_cleanup": "true"}
    if ops == "snapshot":
        ops = "snapshots"
    resp = url_POST(base_url + "/" + urllib.parse.quote(vdb_id) + "/" + ops, payload)
    if resp.status_code == 200:
        return json.loads(resp.text)
    else:
        print(f"ERROR: Status = {resp.status_code}")
        print(f"{resp.text}")
        sys.exit(1)

def vdb_refresh(base_url, vdb_id, ops, pit_id):
    ops = ops.lower()
    if not any(x in ops for x in ["refresh_by_snapshot", "refresh_from_bookmark"]):
        print("Error: Wrong refresh type on VDB: " + ops)
        sys.exit(1)
    payload = ""
    if ops == "refresh_by_snapshot":
        payload = {"snapshot_id": pit_id}
    if ops == "refresh_from_bookmark":
        payload = {"bookmark_id": pit_id}
    resp = url_POST(base_url + "/" + urllib.parse.quote(vdb_id) + "/" + ops, payload)
    if resp.status_code == 200:
        return json.loads(resp.text)
    else:
        print(f"ERROR: Status = {resp.status_code}")
        print(f"{resp.text}")
        sys.exit(1)


def vdb_rollback(base_url, vdb_id, ops, pit_id):
    ops = ops.lower()
    if not any(x in ops for x in ["rollback_by_snapshot", "rollback_from_bookmark"]):
        print("Error: Wrong rollback type on VDB: " + ops)
        sys.exit(1)
    payload = ""
    if ops == "rollback_by_snapshot":
        payload = {"snapshot_id": pit_id}
    if ops == "rollback_from_bookmark":
        payload = {"bookmark_id": pit_id}

    resp = url_POST(base_url + "/" + urllib.parse.quote(vdb_id) + "/" + ops, payload)
    if resp.status_code == 200:
        return json.loads(resp.text)
    else:
        print(f"ERROR: Status = {resp.status_code}")
        print(f"{resp.text}")
        sys.exit(1)


def vdb_update(base_url, vdb_id, name, db_username, db_password, validate_db_credentials, auto_restart,
               environment_user_id, template_id, listener_ids, new_dbid, cdc_on_provision, pre_script, post_script,
               hooks):
    payload = {"name": name, "db_username": db_username, "db_password": db_password,
               "validate_db_credentials": validate_db_credentials, "auto_restart": auto_restart,
               "environment_user_id": environment_user_id, "template_id": template_id, "listener_ids": listener_ids,
               "new_dbid": new_dbid, "cdc_on_provision": cdc_on_provision, "pre_script": pre_script,
               "post_script": post_script, "hooks": hooks}

    resp = url_PATCH(base_url + "/" + urllib.parse.quote(vdb_id), payload)
    if resp.status_code == 200:
        rsp = resp.json()
        print("Updated Account" + " - ID=" + vdb_id)
        return rsp
    else:
        print(f"ERROR: Status = {resp.status_code} - {resp.text}")
        sys.exit(1)


# Init
parser = argparse.ArgumentParser(description='Delphix DCT VDB operations')
subparser = parser.add_subparsers(dest='command')

parser.add_argument('--version', action='version', version='%(prog)s 1.0')
parser.add_argument('--config', type=str, required=False, help="Config file")

# define commands
lst = subparser.add_parser('list')
create = subparser.add_parser('create')
search = subparser.add_parser('search')
delete = subparser.add_parser('delete')
view = subparser.add_parser('view')
disable = subparser.add_parser('disable')
enable = subparser.add_parser('enable')
stop = subparser.add_parser('stop')
start = subparser.add_parser('start')
tag_list = subparser.add_parser('tag_list')
snapshot_list = subparser.add_parser('snapshot_list')
refr_by_snap = subparser.add_parser('refresh_by_snapshot')
refr_by_book = subparser.add_parser('refresh_by_bookmark')
roll_by_snap = subparser.add_parser('rollback_by_snapshot')
roll_by_book = subparser.add_parser('rollback_by_bookmark')
snapshot = subparser.add_parser('snapshot')
create_snapshot = subparser.add_parser("create_snapshot")
tag_create = subparser.add_parser('tag_create')
tag_delete = subparser.add_parser('tag_delete')
tag_delete_all = subparser.add_parser('tag_delete_all')
updt = subparser.add_parser('update')

# define view parms
view.add_argument('--id', type=str, required=True, help="VDB ID to be viewed")

# define list parms

# define enable parms
roll_by_snap.add_argument('--id', type=str, required=True, help="VDB ID to be rolled back with a snap")
roll_by_snap.add_argument('--snap_id', type=str, required=True, help="Snapshot ID to be used for rollback")

roll_by_book.add_argument('--id', type=str, required=True, help="VDB ID to be rolled back with a bookmark")
roll_by_book.add_argument('--book_id', type=str, required=True, help="Bookmark ID to be used for rollback")

refr_by_snap.add_argument('--id', type=str, required=True, help="VDB ID to be refreshed with a snap")
refr_by_snap.add_argument('--snap_id', type=str, required=True, help="Snapshot ID to be used for refresh")

refr_by_book.add_argument('--id', type=str, required=True, help="VDB ID to be refreshed with a bookmark")
refr_by_book.add_argument('--book_id', type=str, required=True, help="Bookmark ID to be used for refresh")

lst.add_argument('--format', type=str, required=False, help="Type of output", choices=['json', 'report'])

# define enable parms
enable.add_argument('--id', type=str, required=True, help="VDB ID to be enabled")

# define disable parms
disable.add_argument('--id', type=str, required=True, help="VDB ID to be disabled")

# define stop parms
stop.add_argument('--id', type=str, required=True, help="VDB ID to be stopped")

# define start parms
start.add_argument('--id', type=str, required=True, help="VDB ID to be started")

# define snapshot parms
snapshot.add_argument('--id', type=str, required=True, help="VDB ID to be snapshot'd")

# define delete parms
delete.add_argument('--id', type=str, required=True, help="VDB ID to be deleted")

# define search parms
search.add_argument('--filter', type=str, required=False, help="VDB search string")
search.add_argument('--format', type=str, required=False, help="Type of output", choices=['json', 'report'])

# define tag_list parms
tag_list.add_argument('--id', type=str, required=True, help="VDB ID for tags list")
tag_list.add_argument('--format', type=str, required=False, help="Type of output", choices=['json', 'report'])

# define snapshot_list parms
snapshot_list.add_argument('--id', type=str, required=True, help="DSource ID for snapshot list")
snapshot_list.add_argument('--format', type=str, required=False, help="Type of output", choices=['json', 'report'])

# define tag_list parms
create_snapshot.add_argument('--id', type=str, required=True, help="DSource ID for creating a new snapshot")

# define tag_create params
tag_create.add_argument('--id', type=str, required=True, help="DSource ID to add tags to")
tag_create.add_argument('--tags', type=str, required=True,
                        help="Tags of the DSource in this format:  [{'key': 'key-1','value': 'value-1'},"
                             " {'key': 'key-2','value': 'value-2'}]")
# define tag_delete params
tag_delete.add_argument('--id', type=str, required=True, help="DSource ID to delete tags from")
tag_delete.add_argument('--key', type=str, required=True, help="Tags key of existing tag")

# define tag_delete_all params
tag_delete_all.add_argument('--id', type=str, required=True, help="DSource ID to delete tags from")

# define update params
updt.add_argument('--id', type=str, required=True, help="VDB ID to be updated")
updt.add_argument('--name', type=str, required=True, help="VDB name to be updated")
updt.add_argument('--db_username', type=str, required=False, help="User name of the VDB to be updated")
updt.add_argument('--db_password', type=str, required=False, help="Password of the user name to be updated")
updt.add_argument('--validate_db_credentials', type=str, required=False, help="Whether db_username and db_password "
                                                                              "must be validated")
updt.add_argument('--auto_restart', type=str, required=False, help="Whether to enable VDB restart")
updt.add_argument('--environment_user_id', type=str, required=False, help="The environment user ID to use to connect "
                                                                          "to the target environment.")
updt.add_argument('--template_id', type=str, required=False, help="The ID of the target VDB Template (Oracle Only)")
updt.add_argument('--listener_ids', type=str, required=False, help="The listener IDs for this provision operation ("
                                                                   "Oracle Only) example: List [ 'listener-123', "
                                                                   "'listener-456' ]")
updt.add_argument('--new_dbid', type=str, required=False, help="Whether to enable new DBID for Oracle")
updt.add_argument('--cdc_on_provision', type=str, required=False, help="Whether to enable CDC on provision for MSSql")
updt.add_argument('--pre_script', type=str, required=False, help="Pre script for MSSql")
updt.add_argument('--post_script', type=str, required=False, help="Post script for MSSql")
updt.add_argument('--hooks', type=str, required=False, help="VDB operation hooks")

# force help if no parms
args = parser.parse_args(args=None if sys.argv[1:] else ['--help'])

# Start processing
dct_read_config(args.config)

dct_base_url = "/vdbs"

if args.command == 'list':
    rs = dct_search("VDB List ", dct_base_url, None, "No VDBs defined.", args.format)
    print(rs)

if args.command == 'view':
    rs = dct_view_by_id(dct_base_url, args.id)
    print(rs)

if args.command == 'delete':
    print("Processing VDB delete ID=" + args.id)
    rs = dct_delete_by_id(dct_base_url, "Deleted VDB", args.id)

if args.command == 'search':
    rs = dct_search("VDB List ", dct_base_url, args.filter, "No VDBs match the search criteria.",
                    args.format)
    print(rs)

if args.command == 'enable':
    print("Processing VDB enable ID=" + args.id)
    rs = vdb_operation(dct_base_url, args.id, args.command)
    dct_job_monitor(rs['job']['id'])

if args.command == 'disable':
    print("Processing VDB disable ID=" + args.id)
    rs = vdb_operation(dct_base_url, args.id, args.command)
    dct_job_monitor(rs['job']['id'])

if args.command == 'stop':
    print("Processing VDB stop ID=" + args.id)
    rs = vdb_operation(dct_base_url, args.id, args.command)
    dct_job_monitor(rs['job']['id'])

if args.command == 'start':
    print("Processing VDB start ID=" + args.id)
    rs = vdb_operation(dct_base_url, args.id, args.command)
    dct_job_monitor(rs['job']['id'])

if args.command == 'snapshot':
    print("Processing VDB snapshot ID=" + args.id)
    rs = vdb_operation(dct_base_url, args.id, args.command)
    dct_job_monitor(rs['job']['id'])

if args.command == 'tag_list':
    rs = dct_list_by_id(dct_base_url, args.id, "/tags", args.format)
    print(rs)

if args.command == 'snapshot_list':
    rs = dct_list_by_id(dct_base_url, args.id, "/snapshots", args.format)
    print(rs)

if args.command == "create_snapshot":
    rs = dct_post_by_id(dct_base_url, args.id, None, "snapshots")
    if rs.status_code == 200:
        print(rs.json())
    else:
        print(f"ERROR: Status = {rs.status_code} - {rs.text}")
        sys.exit(1)

if args.command == 'tag_create':
    payload = {"tags": json.loads(args.tags)}
    rs = dct_post_by_id(dct_base_url, args.id, payload, "tags")
    if rs.status_code == 201:
        print("Create tags for dSource - ID=" + args.id)
    else:
        print(f"ERROR: Status = {rs.status_code} - {rs.text}")
        sys.exit(1)

if args.command == 'tag_delete':
    payload = {"key": args.key}
    rs = dct_post_by_id(dct_base_url, args.id, payload, "tags/delete")
    if rs.status_code == 204:
        print("Delete tag for DSourceID - ID=" + args.id)
    else:
        print(f"ERROR: Status = {rs.status_code} - {rs.text}")
        sys.exit(1)

if args.command == 'tag_delete_all':
    rs = dct_post_by_id(dct_base_url, args.id, None, "tags/delete")
    if rs.status_code == 204:
        print("Deleted all tags for DSource - ID=" + args.id)
    else:
        print(f"ERROR: Status = {rs.status_code} - {rs.text}")
        sys.exit(1)

if args.command == 'update':
    print("Processing VDB update ID=" + args.id)
    rs = vdb_update(dct_base_url, args.id, args.name, args.db_username, args.db_password, args.validate_db_credentials,
                    args.auto_restart, args.environment_user_id, args.template_id, args.listener_ids,
                    args.new_dbid, args.cdc_on_provision, args.pre_script, args.post_script, args.hooks)
    print(rs)

if args.command == 'refresh_by_snapshot':
    print("Processing VDB refresh ID=" + args.id + " with spapshot_ID=" + args.snap_id)
    rs = vdb_refresh(dct_base_url, args.id, args.command, args.snap_id)
    dct_job_monitor(rs['job']['id'])

if args.command == 'rollback_by_snapshot':
    print("Processing VDB rollback ID=" + args.id + " with spapshot_ID=" + args.snap_id)
    rs = vdb_rollback(dct_base_url, args.id, args.command, args.snap_id)
    dct_job_monitor(rs['job']['id'])
