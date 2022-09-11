#
# dt_source
#

import argparse
from helpers import *

# Init
parser = argparse.ArgumentParser(description='Delphix DCT Source operations')
subparser = parser.add_subparsers(dest='command')

parser.add_argument('--version', action='version', version='%(prog)s 1.0')

# define commands

lst = subparser.add_parser('list')
search = subparser.add_parser('search')
view = subparser.add_parser('view')

# define view parms
view.add_argument('--id', type=str, required=True, help="Source to be viewed")

# define list parms
lst.add_argument('--format', type=str, required=False, help="Type of output",  choices=['json', 'report'])

# define search parms
search.add_argument('--filter', type=str, required=False, help="Source search string")
search.add_argument('--format', type=str, required=False, help="Type of output",  choices=['json', 'report'])

# force help if no parms
args = parser.parse_args(args=None if sys.argv[1:] else ['--help'])

# Start processing
dct_base_url = "/sources"

if args.command == 'list':
    rs = dct_search("Source List ", dct_base_url, None, "No Sources defined.", args.format)
    print(rs)

if args.command == 'view':
    rs = dct_view_by_id(dct_base_url, args.id)
    print(rs)

if args.command == 'search':
    rs = dct_search("Source List ", dct_base_url, args.filter, "No Sources match the search criteria.",
                    args.format)
    print(rs)
