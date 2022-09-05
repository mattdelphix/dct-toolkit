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

# define search parms
search.add_argument('--name', type=str, required=True, help="DSource search string")

# define snapshot_list parms
snapshot_list.add_argument('--id', type=str, required=True, help="DSource ID for snapshot list")

# define tags_view parms
tags_view.add_argument('--id', type=str, required=True, help="DSource ID for tags list")

# force help if no parms
args = parser.parse_args(args=None if sys.argv[1:] else ['--help'])

if args.command == 'list':
    print("Processing DSource list")
    rs = dsource_list()
    print(rs)

if args.command == 'view':
    print("Processing DSource view ID="+args.id)
    rs = dsource_by_id(args.id)
    print(rs)

if args.command == 'search':
    print("Processing DSource search name="+args.name)
    rs = dsource_search(args.name)
    print(rs)

if args.command == 'snapshot_list':
    print("Processing Snapshot list for DSource ID="+args.id)
    rs = dsource_snapshot_list(args.id)
    print(rs)

if args.command == 'tags_view':
    print("Processing Tags view for DSource ID="+args.id)
    rs = dsource_tags_view(args.id)
    print(rs)
