import argparse
from engines import *

parser = argparse.ArgumentParser(description = "Delphix DCT Engine operations")
subparser = parser.add_subparsers(dest='command')

parser.add_argument('--version', action='version', version='%(prog)s 1.0')

# define commands

list = subparser.add_parser('list')
search = subparser.add_parser('search')
register = subparser.add_parser('register')

# define search parms
search.add_argument('--name', type=str, required=True, help="engine UUID search string")

# define register parms
register.add_argument('--hostname', type=str, required=True, help="Name used to refer to the engine in DCT")
register.add_argument('--hostaddress', type=str, required=True, help="hostname or ip address")
register.add_argument('--user', type=str, required=True, help="admin user")
register.add_argument('--password', type=str, required=True, help="admin password")

args = parser.parse_args()

if args.command == 'list':
  print("Processing Engine list")
  rs = engine_list()
  print(rs)

if args.command == 'search':
  print("Processing Engine search name="+args.name)
  rs = engine_search(args.name)
  print(rs)

if args.command == 'register':
  print("Processing Engine register ")
