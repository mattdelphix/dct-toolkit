#
# dc_connector
#

import argparse
from helpers import *


# Init
parser = argparse.ArgumentParser(description="Delphix DCT Masking Connector operations")
subparser = parser.add_subparsers(dest='command')

parser.add_argument('--version', action='version', version='%(prog)s 1.0')

# define commands
lst = subparser.add_parser('list')
tst = subparser.add_parser('test')

# define list parms
lst.add_argument('--format', type=str, required=False, help="Type of output",  choices=['json', 'report'])

# define test parms
tst.add_argument('--id', type=str, required=True, help="Connector ID to be tested")
tst.add_argument('--format', type=str, required=False, help="Type of output",  choices=['json', 'report'])

# force help if no parms
args = parser.parse_args(args=None if sys.argv[1:] else ['--help'])

# Start processing
dct_base_url = "/connectors"

if args.command == 'list':
    rs = dct_search("Masking connector List", dct_base_url, None, "No Masking connectors defined.", args.format)
    print(rs)

if args.command == 'test':
    rs = dct_act_by_id(dct_base_url, args.id, "/test")
    print(rs)
