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
import time
from helpers import *

# TODO job cancel not implemented

# Job functions

# Init
parser = argparse.ArgumentParser(description="Delphix DCT Job operations")
subparser = parser.add_subparsers(dest='command')

parser.add_argument('--version', action='version', version='%(prog)s 1.0')
parser.add_argument('--config', type=str, required=False, help="Config file")

# define commands

view = subparser.add_parser('view')
monitor = subparser.add_parser('monitor')
cancel = subparser.add_parser('cancel')
search = subparser.add_parser('search')
lst = subparser.add_parser('list')


# define view parms
view.add_argument('--id', type=str, required=True, help="job ID to be viewed")

# define list parms
lst.add_argument('--format', type=str, required=False, help="Type of output",  choices=['json', 'report'])

# define monitor parms
monitor.add_argument('--id', type=str, required=True, help="job ID to be monitored")

# define search parms
search.add_argument('--filter', type=str, required=False, help="Job search string")
search.add_argument('--format', type=str, required=False, help="Type of output",  choices=['json', 'report'])

# force help if no parms
args = parser.parse_args(args=None if sys.argv[1:] else ['--help'])


# Start processing
dct_read_config(args.config)

dct_base_url = "/jobs"

if args.command == 'monitor':
    print("Monitor Job ID=" + args.id)
    rs = dct_job_monitor(args.id)
    print(rs)

if args.command == 'view':
    rs = dct_view_by_id(dct_base_url, args.id)
    print(rs)

if args.command == 'cancel':
    print("Cancel Job ID=" + args.id)
    rs = job_cancel_by_id(args.id)
    print(rs)

if args.command == 'search':
    rs = dct_search("Job List ", dct_base_url, args.filter, "No Jobs match the search criteria.",
                    args.format)
    print(rs)

if args.command == 'list':
    rs = dct_search("Job List ", dct_base_url, None, "No Jobs defined.", args.format)
    print(rs)
