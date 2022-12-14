#
# dct_login
#


from helpers import *


# TODO job cancel not implemented

# Login functions
def dct_login(dct_query, user, password):
    payload = {"username": user, "password": password}
    resp = url_POST(dct_query, payload)
    if resp.status_code == 200:
        return resp.json()
    if resp.status_code == 201:
        print("User is unauthorized")
    else:
        dct_print_error(resp)
        sys.exit(1)


def dct_token(dct_query, dct_tkn, dct_type):
    tkn = dct_type + ' ' + dct_tkn
    payload = {"token": tkn}
    resp = url_POST(dct_query, payload)
    if resp.status_code == 200:
        return resp.json()
    if resp.status_code == 201:
        print("User is unauthorized")
    else:
        dct_print_error(resp)
        sys.exit(1)


# Init
parser = argparse.ArgumentParser(description="Delphix Login operations")
subparser = parser.add_subparsers(dest='command')

parser.add_argument('--version', action='version', version='%(prog)s Version '+cfg.version)
parser.add_argument('--config', type=str, required=False, help="Config file")
parser.add_argument('--debug', type=int, required=False, help="Debug level [0-2]",choices=[0,1,2])

# define commands

conn = subparser.add_parser('connect')
token = subparser.add_parser('token_info')

# define connect parms
conn.add_argument('--username', type=str, required=True, help="Userid for DCT login")
conn.add_argument('--password', type=str, required=True, help="Password for DCT login")

# define token parms
token.add_argument('--token', type=str, required=True, help="DCT Token")
token.add_argument('--type', type=str, required=False, help="DCT Token Type (default = 'Bearer')", default='Bearer')

# force help if no parms
args = parser.parse_args(args=None if sys.argv[1:] else ['--help'])

# Start processing
args = parser.parse_args()
# Read config
dct_read_config(args.config)
if args.debug:
    cfg.level = args.debug
# force help if no command
if dct_check_empty_command(args):
    parser.print_help()
    sys.exit(1)

if args.command == 'connect':
    dct_base_url = "/login"
    print("Login user=" + args.username)
    rs = dct_login(dct_base_url, args.username, args.password)
    dct_print_json_formatted(rs)

if args.command == 'token_info':
    dct_base_url = "/token-info"
    rs = dct_token(dct_base_url, args.token, args.type)
    dct_print_json_formatted(rs)
