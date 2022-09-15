#
# dc_maskingjob_set
#

import argparse
from helpers import *


# Init
parser = argparse.ArgumentParser(description="Delphix DCT Masking job set operations")
subparser = parser.add_subparsers(dest='command')

parser.add_argument('--version', action='version', version='%(prog)s 1.0')

# define commands
lst = subparser.add_parser('list')
search = subparser.add_parser('search')
view = subparser.add_parser('view')

# define list parms
lst.add_argument('--format', type=str, required=False, help="Type of output",  choices=['json', 'report'])

# define view parms
view.add_argument('--id', type=str, required=True, help="Masking job set ID to be viewed")

# define search parms
search.add_argument('--filter', type=str, required=False, help="Masking job set search string")
search.add_argument('--format', type=str, required=False, help="Type of output", choices=['json', 'report'])

# force help if no parms
args = parser.parse_args(args=None if sys.argv[1:] else ['--help'])

# Start processing
dct_base_url = "/masking-job-sets"

if args.command == 'view':
    rs = dct_view_by_id(dct_base_url, args.id)
    print(rs)

if args.command == 'list':
    rs = dct_search("Masking job set List", dct_base_url, None, "No Masking job sets defined.", args.format)
    print(rs)

if args.command == 'search':
    rs = dct_search("Masking job set List", dct_base_url, args.filter, "No Masking job sets match the search criteria.",
                    args.format)
    print(rs)
