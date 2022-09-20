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

# Init
parser = argparse.ArgumentParser(description='Delphix DCT DSource operations')
subparser = parser.add_subparsers(dest='command')

# Init
parser.add_argument('--version', action='version', version='%(prog)s 1.0')

# define commands
lst = subparser.add_parser('list')
search = subparser.add_parser('search')
view = subparser.add_parser('view')
snapshot_list = subparser.add_parser('snapshot_list')
tag_list = subparser.add_parser('tag_list')

# define view parms
view.add_argument('--id', type=str, required=True, help="DSource ID to be viewed")

# define list parms
lst.add_argument('--format', type=str, required=False, help="Type of output",  choices=['json', 'report'])

# define search parms
search.add_argument('--filter', type=str, required=False, help="DSource search string")
search.add_argument('--format', type=str, required=False, help="Type of output",  choices=['json', 'report'])

# define snapshot_list parms
snapshot_list.add_argument('--id', type=str, required=True, help="DSource ID for snapshot list")
snapshot_list.add_argument('--format', type=str, required=False, help="Type of output",  choices=['json', 'report'])

# define tag_list parms
tag_list.add_argument('--id', type=str, required=True, help="DSource ID for tags list")
tag_list.add_argument('--format', type=str, required=False, help="Type of output",  choices=['json', 'report'])

# force help if no parms
args = parser.parse_args(args=None if sys.argv[1:] else ['--help'])

# Start processing
dct_base_url = "/dsources"

if args.command == 'list':
    rs = dct_search("DSource List ", dct_base_url, None, "No DSources defined.", args.format)
    print(rs)

if args.command == 'view':
    rs = dct_view_by_id(dct_base_url, args.id)
    print(rs)

if args.command == 'search':
    rs = dct_search("DSource List ", dct_base_url, args.filter, "No DSources match the search criteria.",
                    args.format)
    print(rs)

if args.command == 'snapshot_list':
    rs = dct_list_by_id(dct_base_url, args.id, "/snapshots", args.format)
    print(rs)

if args.command == 'tag_list':
    rs = dct_list_by_id(dct_base_url, args.id, "/tags", args.format)
    print(rs)
