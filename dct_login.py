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
        return
    else:
        print(f"ERROR: Status = {resp.status_code} - {resp.text}")
        sys.exit(1)


def dct_token(dct_query, dct_tkn, dct_type):
    tkn = dct_type + ' ' + dct_tkn
    payload = {"token": tkn}
    resp = url_POST(dct_query, payload)
    if resp.status_code == 200:
        return resp.json()
    if resp.status_code == 201:
        print("User is unauthorized")
        return
    else:
        print(f"ERROR: Status = {resp.status_code} - {resp.text}")
        sys.exit(1)


# Init
parser = argparse.ArgumentParser(description="Delphix Login operations")
subparser = parser.add_subparsers(dest='command')

parser.add_argument('--version', action='version', version='%(prog)s 1.0')
parser.add_argument('--config', type=str, required=False, help="Config file")

# define commands

conn = subparser.add_parser('connect')
token = subparser.add_parser('token_info')

# define connect parms
conn.add_argument('--user', type=str, required=True, help="Userid for DCT login")
conn.add_argument('--password', type=str, required=True, help="Password for DCT login")

# define token parms
token.add_argument('--token', type=str, required=True, help="DCT Token")
token.add_argument('--type', type=str, required=False, help="DCT Token Type (default = 'Bearer'", default='Bearer')

# force help if no parms
args = parser.parse_args(args=None if sys.argv[1:] else ['--help'])

# Start processing
dct_read_config(args.config)

if args.command == 'connect':
    dct_base_url = "/login"
    print("Login user=" + args.user)
    rs = dct_login(dct_base_url, args.user, args.password)
    print(rs)

if args.command == 'token_info':
    dct_base_url = "/token-info"
    rs = dct_token(dct_base_url, args.token, args.type)
    print(rs)
