#
# dc_maskingjob_set
#

import argparse
from helpers import *

# Init
parser = argparse.ArgumentParser(description="Delphix DCT Masking job set operations")
subparser = parser.add_subparsers(dest='command')

parser.add_argument('--version', action='version', version='%(prog)s 1.0')
parser.add_argument('--config', type=str, required=False, help="Config file")

# define commands
lst = subparser.add_parser('list')
search = subparser.add_parser('search')
view = subparser.add_parser('view')
tag_list = subparser.add_parser('tag_list')
tag_delete = subparser.add_parser('tag_delete')
tag_delete_all = subparser.add_parser('tag_delete_all')
connector_list = subparser.add_parser('connector_list')

# define list parms
lst.add_argument('--format', type=str, required=False, help="Type of output", choices=['json', 'report'])

# define view parms
view.add_argument('--id', type=str, required=True, help="Masking job set ID to be viewed")

# define search parms
search.add_argument('--filter', type=str, required=False, help="Masking Job Set search string")
search.add_argument('--format', type=str, required=False, help="Type of output", choices=['json', 'report'])

# define tag_list parms
tag_list.add_argument('--id', type=str, required=True, help="Masking Job Set ID for tags list")
tag_list.add_argument('--format', type=str, required=False, help="Type of output", choices=['json', 'report'])

# define tag_delete params
tag_delete.add_argument('--id', type=str, required=True, help="Masking Job Set ID to delete tags from")
tag_delete.add_argument('--key', type=str, required=True, help="Tags key of existing tag")

# define tag_delete_all params
tag_delete_all.add_argument('--id', type=str, required=True, help="Account ID to delete tags from")

# define connector_list parms
connector_list.add_argument('--id', type=str, required=True, help="Masking Job Set ID to be viewed")
connector_list.add_argument('--format', type=str, required=False, help="Type of output",  choices=['json', 'report'])

# force help if no parms
args = parser.parse_args(args=None if sys.argv[1:] else ['--help'])

# Start processing
dct_read_config(args.config)

dct_base_url = "/masking-job-sets"

if args.command == 'view':
    rs = dct_view_by_id(dct_base_url, args.id)
    print(rs)

if args.command == 'list':
    rs = dct_search("Masking job set List", dct_base_url, None, "No Masking Job Sets defined.", args.format)
    print(rs)

if args.command == 'search':
    rs = dct_search("Masking job set List", dct_base_url, args.filter, "No Masking Job Sets match the search criteria.",
                    args.format)
    print(rs)

if args.command == 'tag_list':
    rs = dct_list_by_id(dct_base_url, args.id, "/tags", args.format)
    print(rs)

if args.command == 'tag_delete':
    payload = {"key": args.key}
    rs = dct_post_by_id(dct_base_url, args.id, payload, "tags/delete")
    if rs.status_code == 204:
        print("Delete tag for Masking Job Set - ID=" + args.id)
    else:
        print(f"ERROR: Status = {rs.status_code} - {rs.text}")
        sys.exit(1)

if args.command == 'tag_delete_all':
    rs = dct_post_by_id(dct_base_url, args.id, None, "tags/delete")
    if rs.status_code == 204:
        print("Deleted all tags for Masking Job Set - ID=" + args.id)
    else:
        print(f"ERROR: Status = {rs.status_code} - {rs.text}")
        sys.exit(1)

if args.command == 'connector_list':
    rs = dct_list_by_id(dct_base_url, args.id, "/users", args.format)
    print(rs)