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


# VDBGroup functions
def vdbgroup_create(base_url, name, vdbg_id):
    # create VDB_ID list
    vdb_id_list = vdbg_id.split(",")
    # build payload
    payload = {"name": name, "vdb_ids": vdb_id_list}
    resp = dct_create(base_url, payload)
    dct_job_monitor(resp['job']['id'])


def vdbgroup_refresh(base_url, vdbgroup_id, vdbgroup_name, bookmark_id):
    if vdbgroup_id:
        input_param = vdbgroup_id
    if vdbgroup_name:
        input_param = vdbgroup_name
    payload = {"bookmark_id": bookmark_id}
    resp = dct_create(base_url + "/" + urllib.parse.quote(input_param) + "/refresh", payload)
    dct_job_monitor(resp['job']['id'])

def vdbgroup_update(base_url, vdbgroup_id, vdbgroup_name, vdb_list):
    # create VDB_ID list
    vdb_id_list = vdb_list.split(",")
    if vdbgroup_id:
        # build payload
        input_param = vdbgroup_id
        payload = {"id": vdbgroup_id, "vdb_ids": vdb_id_list}
    if vdbgroup_name:
        input_param = vdbgroup_name
        # build payload
        payload = {"name": vdbgroup_name, "vdb_ids": vdb_id_list}

    resp = url_PATCH(base_url + "/" + urllib.parse.quote(input_param), payload)
    dct_job_monitor(resp['job']['id'])
    if resp.status_code == 200:
        print("Updated VDBGroup: " + resp.text)
    else:
        print(f"ERROR: Status = {resp.status_code} - {resp.text}")
        sys.exit(1)


def vdbgroup_provision_from_bookmark(base_url, input_param, vdbgroup_name, bookmark_id, vdb_id, dataset_group=""):
    # create VDB_ID list
    vdb_id_list = vdb_id.split(",")
    build_params: str = ""
    payload: str = ""
    for index, item in enumerate(vdb_id_list):
        if index != len(vdb_id_list) - 1:
            build_params += "\"" + item + "\"" + ": {\"auto_select_repository\": true"
            if dataset_group is not None:
                build_params += ",\"target_group_id\": \"" + dataset_group + "\""
            build_params += "},"
        else:
            build_params += "\"" + item + "\"" + ": {\"auto_select_repository\": true"
            if dataset_group is not None:
                build_params += ",\"target_group_id\": \"" + dataset_group + "\""
            build_params += "}"

    payload = '{ "name": "' + vdbgroup_name + '", "bookmark_id": "' + bookmark_id + '", "provision_parameters": {' + \
              build_params + '}}'
    print(payload)
    resp = dct_create(base_url + "/" + urllib.parse.quote(input_param), json.loads(payload))
    dct_job_monitor(resp['job']['id'])



# Init
parser = argparse.ArgumentParser(description="Delphix DCT VDBgroup operations")
subparser = parser.add_subparsers(dest='command')

parser.add_argument('--version', action='version', version='%(prog)s 1.0')
parser.add_argument('--config', type=str, required=False, help="Config file")
parser.add_argument('--debug', type=int, required=False, help="Debug level [0-2]",choices=[0,1,2])

# define commands

lst = subparser.add_parser('list')
search = subparser.add_parser('search')
delete = subparser.add_parser('delete')
create = subparser.add_parser('create')
view = subparser.add_parser('view')
bookmarks = subparser.add_parser('bookmarks')
refresh = subparser.add_parser('refresh')
rollback = subparser.add_parser('rollback')
update = subparser.add_parser('update')
provision_from_bookmark = subparser.add_parser('provision_from_bookmark')

# define view parms
view.add_argument('--id', type=str, required=True, help="VDBGroup full name or ID to be viewed")

# define list parms
lst.add_argument('--format', type=str, required=False, help="Type of output", choices=['json', 'report'])

# define delete parms
delete.add_argument('--id', type=str, required=True, help="VDBgroup to be deleted")

# define search parms
search.add_argument('--filter', type=str, required=False, help="VDBgroup search string")
search.add_argument('--format', type=str, required=False, help="Type of output", choices=['json', 'report'])

# define create parms
create.add_argument('--name', type=str, required=True, help="Name of the new VDBgroup")
create.add_argument('--vdb_id', type=str, required=True, help="List of VDB IDs separated by commas")

# define view parms
bookmarks.add_argument('--id', type=str, required=True, help="VDBGroup full name or ID to be viewed")
bookmarks.add_argument('--format', type=str, required=False, help="Type of output", choices=['json', 'report'])

# refresh view parms
refresh.add_argument('--bookmark_id', type=str, help="ID of the bookmark to be refreshed")
refresh = refresh.add_mutually_exclusive_group(required=True)
refresh.add_argument('--name', type=str, help="Name of the VDBGroup to refresh ")
refresh.add_argument('--id', type=str, help="ID of the VDBGroup to be refreshed")

# rollback view parms
rollback.add_argument('--bookmark_id', type=str, required=True, help="ID of the bookmark to be rollback")
rollback = rollback.add_mutually_exclusive_group(required=True)
rollback.add_argument('--name', type=str, help="Name of the VDBGroup to rollback ")
rollback.add_argument('--id', type=str, help="ID of the VDBGroup to be rollback")

# update create parms
update.add_argument('--vdb_id', type=str, required=True, help="List of VDB IDs separated by commas")
update = update.add_mutually_exclusive_group(required=True)
update.add_argument('--name', type=str, help="Name of the VDBgroup to update")
update.add_argument('--id', type=str, help="ID of the VDBGroup to be refreshed")

# provision from bookmark
provision_from_bookmark.add_argument('--vdbgroup_name', type=str, required=True, help="VDB Group name")
provision_from_bookmark.add_argument('--bookmark_id', type=str, required=True, help="Bookmark_Id to provision from")
provision_from_bookmark.add_argument('--vdb_id', type=str, required=True, help="List of VDB IDs separated by commas")
provision_from_bookmark.add_argument('--dataset_group', type=str, required=False, help="Target Group where the VDBs "
                                                                                       "will be created")
# provision_from_bookmark.add_argument('--dataset_group', type=str, required=True, help="DataSet group for the VBDs to be created on")

# force help if no parms
args = parser.parse_args(args=None if sys.argv[1:] else ['--help'])

# Start processing
dct_read_config(args.config)
if args.debug:
    cfg.level = args.debug

dct_base_url = "/vdb-groups"

if args.command == 'list':
    rs = dct_search("VDBGroup List ", dct_base_url, None, "No VDBGroups defined.", args.format)
    print(rs)

if args.command == 'view':
    rs = dct_view_by_id(dct_base_url, args.id)
    print(rs)

if args.command == 'delete':
    print("Processing VDBGroup delete ID=" + args.id)
    rs = dct_delete_by_id(dct_base_url, "Deleted VDBGroup", args.id)
    print(rs)

if args.command == 'search':
    rs = dct_search("VDBGroups List ", dct_base_url, args.filter, "No VDBGroups match the search criteria.",
                    args.format)
    print(rs)

if args.command == 'create':
    print("Processing VDBGroup create ")
    vdbgroup_create(dct_base_url, args.name, args.vdb_id)

if args.command == 'bookmarks':
    rs = dct_list_by_id(dct_base_url, args.id, "/bookmarks", args.format)
    print(rs)

if args.command == 'refresh':
    print("Processing VDBGroup refresh ")
    vdbgroup_refresh(dct_base_url, args.id, args.name, args.bookmark_id)

if args.command == 'rollback':
    print("Processing VDBGroup rollback ")
    vdbgroup_refresh(dct_base_url, args.id, args.name, args.bookmark_id)

if args.command == 'update':
    print("Processing VDBGroup update ")
    vdbgroup_update(dct_base_url, args.id, args.name, args.vdb_id)

if args.command == "provision_from_bookmark":
    print("Attempting to Provisioning VDB Group")
    vdbgroup_provision_from_bookmark(dct_base_url, args.command, args.vdbgroup_name, args.bookmark_id, args.vdb_id,
                                     args.dataset_group)
