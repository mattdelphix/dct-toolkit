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

# Init
parser = argparse.ArgumentParser(description='Delphix DCT DSource operations')
subparser = parser.add_subparsers(dest='command')

# Init
parser.add_argument('--version', action='version', version='%(prog)s 1.0')
parser.add_argument('--config', type=str, required=False, help="Config file")
parser.add_argument('--debug', type=int, required=False, help="Debug level [0-2]",choices=[0,1,2])

# define commands
lst = subparser.add_parser('list')
search = subparser.add_parser('search')
view = subparser.add_parser('view')
snapshot_list = subparser.add_parser('snapshot_list')
create_snapshot = subparser.add_parser("create_snapshot")
tag_list = subparser.add_parser('tag_list')
tag_create = subparser.add_parser('tag_create')
tag_delete = subparser.add_parser('tag_delete')
tag_delete_all = subparser.add_parser('tag_delete_all')

# define view parms
view.add_argument('--id', type=str, required=True, help="DSource ID to be viewed")

# define list parms
lst.add_argument('--format', type=str, required=False, help="Type of output", choices=['json', 'report','id'])

# define search parms
search.add_argument('--filter', type=str, required=False, help="DSource search string")
search.add_argument('--format', type=str, required=False, help="Type of output", choices=['json', 'report','id'])

# define snapshot_list parms
snapshot_list.add_argument('--id', type=str, required=True, help="DSource ID for snapshot list")
snapshot_list.add_argument('--format', type=str, required=False, help="Type of output", choices=['json', 'report','id'])

# define create_snapshot parms
create_snapshot.add_argument('--id', type=str, required=True, help="DSource ID for creating a new snapshot")

# define tag_list parms
tag_list.add_argument('--id', type=str, required=True, help="DSource ID for tags list")
tag_list.add_argument('--format', type=str, required=False, help="Type of output", choices=['json', 'report','id'])

# define tag_create params
tag_create.add_argument('--id', type=str, required=True, help="DSource ID to add tags to")
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

dct_base_url = "/dsources"

if args.command == 'list':
    rs = dct_search("DSource List ", dct_base_url, None, "No DSources defined.", args.format)

if args.command == 'view':
    rs = dct_view_by_id(dct_base_url, args.id)
    dct_print_json_formatted(rs)

if args.command == 'search':
    rs = dct_search("DSource List ", dct_base_url, args.filter, "No DSources match the search criteria.",
                    args.format)

if args.command == 'snapshot_list':
    rs = dct_list_by_id(dct_base_url, args.id, "/snapshots", args.format)
    dct_print_json_formatted(rs)

if args.command == "create_snapshot":
    rs = dct_post_by_id(dct_base_url, args.id, None, "snapshots")
    dct_job_monitor(rs['job']['id'])
    if rs.status_code == 200:
        print(rs.json())
    else:
        dct_print_error(rs)
        sys.exit(1)

if args.command == 'tag_list':
    rs = dct_list_by_id(dct_base_url, args.id, "/tags", args.format)
    dct_print_json_formatted(rs)

if args.command == 'tag_create':
    payload = {"tags": json.loads(args.tags)}
    rs = dct_post_by_id(dct_base_url, args.id, payload, "tags")
    if rs.status_code == 201:
        print("Create tags for dSource - ID=" + args.id)
    else:
        dct_print_error(rs)
        sys.exit(1)

if args.command == 'tag_delete':
    payload = {"key": args.key}
    rs = dct_post_by_id(dct_base_url, args.id, payload, "tags/delete")
    if rs.status_code == 204:
        print("Delete tag for DSourceID - ID=" + args.id)
    else:
        dct_print_error(rs)
        sys.exit(1)

if args.command == 'tag_delete_all':
    rs = dct_post_by_id(dct_base_url, args.id, None, "tags/delete")
    if rs.status_code == 204:
        print("Deleted all tags for DSource - ID=" + args.id)
    else:
        dct_print_error(rs)
        sys.exit(1)
