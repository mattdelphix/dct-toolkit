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


import argparse
from helpers import *


# Bookmark functions
def bookmark_create(base_url, name, bookmark_id, retention, tags):
    # create VDB_ID list
    vdb_id_list = bookmark_id.split(",")
    # build payload
    payload = {"name": name, "vdb_ids": vdb_id_list, "retention": retention}
    if tags is not None:
        tags_dic = json.loads(tags)
        payload['tags'] = tags_dic
    resp = url_POST(base_url, payload)
    if resp.status_code == 201:
        bookm = resp.json()
        print(f"Create Bookmark with ID={name}, Retention={retention}, Tags={tags}")
        return bookm
    else:
        print(f"ERROR: Status = {resp.status_code} - {resp.text}")
        sys.exit(1)


# Init
parser = argparse.ArgumentParser(description="Delphix DCT Bookmark operations")
subparser = parser.add_subparsers(dest='command')

parser.add_argument('--version', action='version', version='%(prog)s 1.0')
parser.add_argument('--config', type=str, required=False, help="Config file")

# define commands

lst = subparser.add_parser('list')
create = subparser.add_parser('create')
delete = subparser.add_parser('delete')
search = subparser.add_parser('search')
view = subparser.add_parser('view')
vdbgroup_list = subparser.add_parser('vdbgroup_list')
tag_list = subparser.add_parser('tag_list')
tag_create = subparser.add_parser('tag_create')
tag_delete = subparser.add_parser('tag_delete')
tag_delete_all = subparser.add_parser('tag_delete_all')

# define create parms
create.add_argument('--name', type=str, required=True, help="Name of the new Bookmark")
create.add_argument('--vdb_id', type=str, required=True, help="List of VDB IDs separated by commas")
create.add_argument('--retention', type=int, required=False, help="Bookmark retention period in days", default=365)
create.add_argument('--tags', type=str, required=False,
                    help="Tags of the new Account in this format:  [{'key': 'key-1','value': 'value-1'},"
                         " {'key': 'key-2','value': 'value-2'}]")

# define delete parms
delete.add_argument('--id', type=str, required=True, help="Bookmark ID to be deleted")

# define view parms
view.add_argument('--id', type=str, required=True, help="Bookmark ID to be viewed")

# define list parms
lst.add_argument('--format', type=str, required=False, help="Type of output", choices=['json', 'report'])

# define search parms
search.add_argument('--filter', type=str, required=False, help="Bookmark search string")
search.add_argument('--format', type=str, required=False, help="Type of output", choices=['json', 'report'])

# define vdbgroup_list parms
vdbgroup_list.add_argument('--id', type=str, required=True, help="Bookmark ID for VDBGroup list")
vdbgroup_list.add_argument('--format', type=str, required=False, help="Type of output", choices=['json', 'report'])

# define tag_list parms
tag_list.add_argument('--id', type=str, required=True, help="Bookmark ID for tags list")
tag_list.add_argument('--format', type=str, required=False, help="Type of output", choices=['json', 'report'])

# define tag_create params
tag_create.add_argument('--id', type=str, required=True, help="Bookmark ID to add tags to")
tag_create.add_argument('--tags', type=str, required=True,
                        help="Tags of the Bookmark in this format:  [{'key': 'key-1','value': 'value-1'},"
                             " {'key': 'key-2','value': 'value-2'}]")
# define tag_delete params
tag_delete.add_argument('--id', type=str, required=True, help="DSource ID to delete tags from")
tag_delete.add_argument('--key', type=str, required=True, help="Tags key of existing tag")

# define tag_delete_all params
tag_delete_all.add_argument('--id', type=str, required=True, help="DSource ID to delete tags from")

# force help if no parms
args = parser.parse_args(args=None if sys.argv[1:] else ['--help'])

# Start processing
dct_read_config(args.config)

dct_base_url = "/bookmarks"

if args.command == 'view':
    rs = dct_view_by_id(dct_base_url, args.id)
    print(rs)

if args.command == 'search':
    rs = dct_search("Bookmark List", dct_base_url, args.filter, "No Bookmarks match the search criteria.",
                    args.format)
    print(rs)

if args.command == 'list':
    rs = dct_search("Bookmarks List", dct_base_url, None, "No Bookmarks defined.", args.format)
    print(rs)

if args.command == 'create':
    rs = bookmark_create(dct_base_url, args.name, args.vdb_id, args.retention, args.tags)
    dct_job_monitor(rs['job']['id'])

if args.command == 'delete':
    print("Processing Bookmark delete ID=" + args.id)
    rs = dct_delete_by_id(dct_base_url, "Deleted Bookmark", args.id)

if args.command == 'vdbgroup_list':
    rs = dct_list_by_id(dct_base_url, args.id, "/vdb-groups", args.format)
    print(rs)

if args.command == 'tag_list':
    rs = dct_list_by_id(dct_base_url, args.id, "/tags", args.format)
    print(rs)

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