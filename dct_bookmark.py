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


# Bookmark functions
def bookmark_create(base_url, name, bookmark_id, retention, tags):
    # create VDB_ID list
    vdb_id_list = bookmark_id.split(",")
    # build payload
    payload = {"name": name, "vdb_ids": vdb_id_list, "retention": retention}
    if tags is not None:
        payload['tags'] = tags

    resp = url_POST(base_url, payload)
    if resp.status_code == 201:
        print(f"Create Bookmark with ID={name}, Retention={retention}, Tags={tags}")
        return resp.json()
    else:
        if resp.status_code == 409:
            print(f"A bookmark with the same name {name} already exists, duplicate names not allowed.")
        else:
            dct_print_error(resp)
            sys.exit(1)


# Init
parser = argparse.ArgumentParser(description="Delphix DCT Bookmark operations")
subparser = parser.add_subparsers(dest='command')

parser.add_argument('--version', action='version', version='%(prog)s Version '+cfg.version)
parser.add_argument('--config', type=str, required=False, help="Config file")
parser.add_argument('--debug', type=int, required=False, help="Debug level [0-2]",choices=[0,1,2])

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
create.add_argument('--tags', nargs='*', type=str, required=True, action=dct_parsetags,
                    help="Tags of the DSource in this format:  key=value key=value")

# define delete parms
delete.add_argument('--id', type=str, required=True, help="Bookmark ID to be deleted")

# define view parms
view.add_argument('--id', type=str, required=True, help="Bookmark ID or Name to be viewed")

# define list parms
lst.add_argument('--format', type=str, required=False, help="Type of output", choices=['json', 'report','id'])

# define search parms
search.add_argument('--filter', type=str, required=False, help="Bookmark search string")
search.add_argument('--format', type=str, required=False, help="Type of output", choices=['json', 'report','id'])

# define vdbgroup_list parms
vdbgroup_list.add_argument('--id', type=str, required=True, help="Bookmark ID for VDBGroup list")
vdbgroup_list.add_argument('--format', type=str, required=False, help="Type of output", choices=['json', 'report','id'])

# define tag_list parms
tag_list.add_argument('--id', type=str, required=True, help="Bookmark ID for tags list")
tag_list.add_argument('--format', type=str, required=False, help="Type of output", choices=['json', 'report','id'])

# define tag_create params
tag_create.add_argument('--id', type=str, required=True, help="Bookmark ID to add tags to")
tag_create.add_argument('--tags', nargs='*', type=str, required=True, action=dct_parsetags,
                        help="Tags of the DSource in this format:  key=value key=value")
# define tag_delete params
tag_delete.add_argument('--id', type=str, required=True, help="DSource ID to delete tags from")
tag_delete.add_argument('--key', type=str, required=True, help="Tags key of existing tag")

# define tag_delete_all params
tag_delete_all.add_argument('--id', type=str, required=True, help="DSource ID to delete tags from")

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

dct_base_url = "/bookmarks"

if args.command == 'view':
    rs = dct_view_by_id(dct_base_url, args.id)
    dct_print_json_formatted(rs)

if args.command == 'search':
    rs = dct_search("Bookmark List", dct_base_url, args.filter, "No Bookmarks match the search criteria.",
                    args.format)
    dct_print_json_formatted(rs)

if args.command == 'list':
    rs = dct_search("Bookmarks List", dct_base_url, None, "No Bookmarks defined.", args.format)
    dct_print_json_formatted(rs)

if args.command == 'create':
    rs = bookmark_create(dct_base_url, args.name, args.vdb_id, args.retention, args.tags)


if args.command == 'delete':
    print("Processing Bookmark delete ID=" + args.id)
    rs = dct_delete_by_id(dct_base_url, "Deleted Bookmark", args.id, 204)

if args.command == 'vdbgroup_list':
    rs = dct_list_by_id(dct_base_url, args.id, "/vdb-groups", args.format)
    dct_print_json_formatted(rs)

if args.command == 'tag_list':
    rs = dct_list_by_id(dct_base_url, args.id, "/tags", args.format)
    dct_print_json_formatted(rs['tags'])

if args.command == 'tag_create':
    payload = {"tags": args.tags}
    rs = dct_post_by_id(dct_base_url, args.id, payload, "tags", 201)
    print("Created tags for Account - ID=" + args.id)

if args.command == 'tag_delete':
    payload = {"key": args.key}
    rs = dct_post_by_id(dct_base_url, args.id, payload, "tags/delete", 204)
    print("Deleted tag by key for Account - ID=" + args.id)

if args.command == 'tag_delete_all':
    rs = dct_post_by_id(dct_base_url, args.id, None, "tags/delete", 204)
    print("Deleted all tags for Account - ID=" + args.id)
