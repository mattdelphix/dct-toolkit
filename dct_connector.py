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
parser = argparse.ArgumentParser(description="Delphix DCT Masking connector operations")
subparser = parser.add_subparsers(dest='command')

parser.add_argument('--version', action='version', version='%(prog)s 1.0')

# define commands
lst = subparser.add_parser('list')
tst = subparser.add_parser('test')
search = subparser.add_parser('search')
view = subparser.add_parser('view')

# define list parms
lst.add_argument('--format', type=str, required=False, help="Type of output",  choices=['json', 'report'])

# define test parms
tst.add_argument('--id', type=str, required=True, help="Masking connector ID to be tested")
tst.add_argument('--format', type=str, required=False, help="Type of output",  choices=['json', 'report'])

# define view parms
view.add_argument('--id', type=str, required=True, help="Masking connector ID to be viewed")

# define search parms
search.add_argument('--filter', type=str, required=False, help="Masking connector search string")
search.add_argument('--format', type=str, required=False, help="Type of output", choices=['json', 'report'])

# force help if no parms
args = parser.parse_args(args=None if sys.argv[1:] else ['--help'])

# Start processing
dct_base_url = "/connectors"

if args.command == 'view':
    rs = dct_view_by_id(dct_base_url, args.id)
    print(rs)

if args.command == 'list':
    rs = dct_search("Masking connector List", dct_base_url, None, "No Masking connectors defined.", args.format)
    print(rs)

if args.command == 'search':
    rs = dct_search("Masking connector List", dct_base_url, args.filter, "No Masking connectors match the search criteria.",
                    args.format)
    print(rs)

if args.command == 'test':
    rs = dct_act_by_id(dct_base_url, args.id, "/test")
    print(rs)
