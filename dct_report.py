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


from datetime import datetime
from helpers import *

# TODO add sort and limit to all reports as parameter

# Report functions
def report_api_usage(begin, end):
    date_begin = urllib.parse.quote(begin)
    date_end = urllib.parse.quote(end)
    resp = url_GET("/reporting/api-usage-report?start_date=" + date_begin + "&end_date=" + date_end)
    if resp.status_code == 200:
        report_data = resp.json()['items']
        if report_data:
            tabular_report(f"DELPHIX Data Control Tower - API USAGE REPORT\nInterval: {begin} to {end}", report_data)
        else:
            print(f"\nNo API Usage Report for this interval - {begin} to {end}")
            return
    else:
        print(f"ERROR: Status = {resp.status_code} - {resp.text}")
        sys.exit(1)


def report_product_info():
    resp = url_GET("/reporting/product_info")
    if resp.status_code == 200:
        tabular_report("DELPHIX Data Control Tower - PRODUCT INFO", resp.json())
    else:
        print(f"ERROR: Status = {resp.status_code} - {resp.text}")
        sys.exit(1)


def report_vdb_inventory(report_filter):
    display_filter = ""
    if report_filter is not None:
        payload = {"filter_expression": report_filter}
        display_filter = "SEARCH: "+report_filter
        resp = url_POST("/reporting/vdb-inventory-report/search", payload)
    else:
        resp = url_GET("/reporting/vdb-inventory-report")
    if resp.status_code == 200:
        report_data = resp.json()['items']
        if report_data:
            tabular_report("DELPHIX Data Control Tower - DSource Usage Report " + display_filter, report_data)
            return report_data
        else:
            print(f"\nNo DSources match search criteria.")
            return
    else:
        print(f"ERROR: Status = {resp.status_code} - {resp.text}")
        sys.exit(1)


def report_dsource_usage(report_filter):
    display_filter = ""
    if report_filter is not None:
        payload = {"filter_expression": report_filter}
        display_filter = "SEARCH: "+report_filter
        resp = url_POST("/reporting/dsource-usage-report/search", payload)
    else:
        resp = url_GET("/reporting/dsource-usage-report")
    if resp.status_code == 200:
        report_data = resp.json()['items']
        if report_data:
            tabular_report("DELPHIX Data Control Tower - DSource Usage Report " + display_filter, report_data)
            return report_data
        else:
            print(f"\nNo DSources match search criteria.")
            return
    else:
        print(f"ERROR: Status = {resp.status_code} - {resp.text}")
        sys.exit(1)


def report_storage_summary(report_filter):
    display_filter = ""
    if report_filter is not None:
        payload = {"filter_expression": report_filter}
        display_filter = "SEARCH: "+report_filter
        resp = url_POST("/reporting/virtualization-storage-summary-report/search", payload)
    else:
        resp = url_GET("/reporting/virtualization-storage-summary-report")
    if resp.status_code == 200:
        report_data = resp.json()['items']
        if report_data:
            tabular_report("DELPHIX Data Control Tower - Storage summary Report " + display_filter, report_data)
            return report_data
        else:
            print(f"\nNo Delphix Engines match search criteria.")
            return
    else:
        print(f"ERROR: Status = {resp.status_code} - {resp.text}")
        sys.exit(1)

# Init
parser = argparse.ArgumentParser(description = "Delphix DCT Reports")
subparser = parser.add_subparsers(dest='command')

parser.add_argument('--version', action='version', version='%(prog)s 1.0')
parser.add_argument('--config', type=str, required=False, help="Config file")
parser.add_argument('--debug', type=int, required=False, help="Debug level [0-2]",choices=[0,1,2])

# define commands

api_usage = subparser.add_parser('api_usage')
dsource_usage = subparser.add_parser('dsource_usage')
vdb_inventory = subparser.add_parser('vdb_inventory')
storage_summary = subparser.add_parser('storage_summary')
product_info = subparser.add_parser('product_info')

# Get current date time in ISO FORMAT
#TODO to be implemented logic to set current time as API end timestamp
end_time = datetime.now().isoformat()

# define api_usage parms
api_usage.add_argument('--begin', type=str, required=False, help="begin timestamp for report", default='2020-01-01T15:00:00-00:00')
api_usage.add_argument('--end', type=str, required=False, help="end timestamp for report", default='2099-01-01T15:00:00-00:00')

# define vdb_inventory parms
vdb_inventory.add_argument('--filter', type=str, required=False, help="VDB search string")

# define storage_summary parms
storage_summary.add_argument('--filter', type=str, required=False, help="Storage Summary search string")

# define storage_summary parms
dsource_usage.add_argument('--filter', type=str, required=False, help="DSource Usage search string")

# force help if no parms
args = parser.parse_args(args=None if sys.argv[1:] else ['--help'])

# Start processing
dct_read_config(args.config)
if args.debug:
    cfg.level = args.debug

if args.command == 'api_usage':
    rs = report_api_usage(args.begin, args.end)

if args.command == 'vdb_inventory':
    rs = report_vdb_inventory(args.filter)

if args.command == 'dsource_usage':
    rs = report_dsource_usage(args.filter)

if args.command == 'storage_summary':
    rs = report_storage_summary(args.filter)

if args.command == 'product_info':
    rs = report_product_info()


