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

# TODO job cancel not implemented

# Init
parser = argparse.ArgumentParser(description="Delphix DCT Snapshot operations")
subparser = parser.add_subparsers(dest='command')

parser.add_argument('--version', action='version', version='%(prog)s 1.0')

# define commands
view = subparser.add_parser('view')


# define view parms
view.add_argument('--id', type=str, required=True, help="job ID to be viewed")

# force help if no parms
args = parser.parse_args(args=None if sys.argv[1:] else ['--help'])


# Start processing
dct_base_url = "/snapshots"

if args.command == 'view':
    rs = dct_view_by_id(dct_base_url, args.id)
    print(rs)
