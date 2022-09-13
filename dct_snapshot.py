#
# dct_snapshot
#

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
