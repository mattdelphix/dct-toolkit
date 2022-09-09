import argparse
from dsources import *

# TODO test snapshot list
# TODO test dsource_tags_view when no tags are present. report is produced

parser = argparse.ArgumentParser(description='Delphix DCT DSource operations')
subparser = parser.add_subparsers(dest='command')

parser.add_argument('--version', action='version', version='%(prog)s 1.0')

# define commands

lst = subparser.add_parser('list')
search = subparser.add_parser('search')
view = subparser.add_parser('view')
snapshot_list = subparser.add_parser('snapshot_list')
tags_view = subparser.add_parser('tags_view')

# define view parms
view.add_argument('--id', type=str, required=True, help="DSource ID to be viewed")

# define list parms
lst.add_argument('--format', type=str, required=False, help="Type of output",  choices=['json', 'report'])

# define search parms
search.add_argument('--filter', type=str, required=False, help="DSource search string")
search.add_argument('--format', type=str, required=False, help="Type of output",  choices=['json', 'report'])

# define snapshot_list parms
snapshot_list.add_argument('--id', type=str, required=True, help="DSource ID for snapshot list")

# define tags_view parms
tags_view.add_argument('--id', type=str, required=True, help="DSource ID for tags list")

# force help if no parms
args = parser.parse_args(args=None if sys.argv[1:] else ['--help'])

if args.command == 'list':
    rs = dct_search("DSource List ", "/dsources", None, "No DSources defined.", args.format)
    print(rs)

if args.command == 'view':
    rs = dct_view_by_id("/dsources", args.id)
    print(rs)

if args.command == 'search':
    rs = dct_search("DSource List ", "/dsources", args.filter, "No DSources match the search criteria.",
                    args.format)
    print(rs)


if args.command == 'snapshot_list':
    print("Processing Snapshot list for DSource ID="+args.id)
    rs = dsource_snapshot_list(args.id)
    print(rs)

if args.command == 'tags_view':
    print("Processing Tags view for DSource ID="+args.id)
    rs = dsource_tags_view(args.id)
    print(rs)
