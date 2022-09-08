import argparse
from sources import *

# TODO search should provide a generic filter as dct_report

parser = argparse.ArgumentParser(description='Delphix DCT Source operations')
subparser = parser.add_subparsers(dest='command')

parser.add_argument('--version', action='version', version='%(prog)s 1.0')

# define commands

lst = subparser.add_parser('list')
search = subparser.add_parser('search')
view = subparser.add_parser('view')

# define view parms
view.add_argument('--id', type=str, required=True, help="Source to be viewed")

# define search parms
search.add_argument('--name', type=str, required=True, help="Source search string")

# force help if no parms
args = parser.parse_args(args=None if sys.argv[1:] else ['--help'])

if args.command == 'list':
    print("Processing Source list")
    rs = source_list()
    print(rs)

if args.command == 'view':
    rs = source_by_id(args.id)
    print(rs)

if args.command == 'search':
    print("Processing Source search name="+args.name)
    rs = source_search(args.name)
    print(rs)
