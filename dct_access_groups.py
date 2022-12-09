#
# dc_maskingjob_set
#


from helpers import *

def access_group_update(base_url, name, role_id):
    payload = {"name": name,
               "policies": [{"role_id": role_id}]
               }
    #dct_create - will not work because OK response is code 201 not 200.
    resp = url_POST(base_url, payload)
    if resp.status_code == 201:
        rsp = resp.json()
        print("Access Group created with name " + name)
        return rsp
    else:
        print(f"ERROR: Status = {resp.status_code} - {resp.text}")
        sys.exit(1)

# Init
parser = argparse.ArgumentParser(description="Delphix DCT Masking job set operations")
subparser = parser.add_subparsers(dest='command')

parser.add_argument('--version', action='version', version='%(prog)s 1.0')
parser.add_argument('--config', type=str, required=False, help="Config file")

# define commands
lst = subparser.add_parser('list')
search = subparser.add_parser('search')
view = subparser.add_parser('view')
create = subparser.add_parser('create')
update = subparser.add_parser('update')
delete = subparser.add_parser('delete')
tag_create = subparser.add_parser('tag_create')
tag_list = subparser.add_parser('tag_list')
tag_delete = subparser.add_parser('tag_delete')
tag_delete_all = subparser.add_parser('tag_delete_all')
add_account = subparser.add_parser('add_account')
delete_account = subparser.add_parser('delete_account')
add_policy = subparser.add_parser('add_policy')
delete_policy = subparser.add_parser('delete_policy')

# define list parms
lst.add_argument('--format', type=str, required=False, help="Type of output", choices=['json', 'report'])

# define view parms
view.add_argument('--id', type=str, required=True, help="Access Group ID to be viewed")

# define search parms
search.add_argument('--filter', type=str, required=False, help="Access Group search string")
search.add_argument('--format', type=str, required=False, help="Type of output", choices=['json', 'report'])

# define create parms
#create.add_argument('--id', type=str, required=False, help="Access Group ID to be updated")
create.add_argument('--name', type=str, required=True, help="Access Group name to be updated")
"""create.add_argument('--single_account', type=str, required=False, choices=['true', 'false'],
                    help="Access Group is single account or not")
create.add_argument('--account_id', type=str, required=False,
                    help="List of accounts ids included individually (as opposed to added by tags) in the Access group")
create.add_argument('--tagged_account_id', type=str, required=False,
                    help="List of accounts ids included by tags in the Access group.")
create.add_argument('--account_tags', type=str, required=False,
                    help="List of account tags. Accounts matching any of these tags will be automatically added to "
                         "the Access group.")
create.add_argument('--policy_id', type=str, required=False, help="The Access group policy ID")
create.add_argument('--policy_name', type=str, required=False, help="The Access group policy name")"""
create.add_argument('--role_id', type=str, required=True, help="The Access group role id")


# define update parms
update.add_argument('--id', type=str, required=True, help="Access Group ID to be updated")
update.add_argument('--name', type=str, required=True, help="Access Group name to be updated")

# define delete parms
delete.add_argument('--id', type=str, required=True, help="Access Group ID or name to be deleted")

# define tag_create params
tag_create.add_argument('--id', type=str, required=True, help="Access Group ID to add tags to")
tag_create.add_argument('--tags', nargs='*', type=str, required=True, action=dct_parsetags,
                        help="Tags in this format:  key=value key=value")
# define tag_list parms
tag_list.add_argument('--id', type=str, required=True, help="Access Group ID for tags list")
tag_list.add_argument('--format', type=str, required=False, help="Type of output", choices=['json', 'report'])

# define tag_delete params
tag_delete.add_argument('--id', type=str, required=True, help="Access Group ID to delete tags from")
tag_delete.add_argument('--key', type=str, required=True, help="Tags key of existing tag")

# define tag_delete_all params
tag_delete_all.add_argument('--id', type=str, required=True, help="Access Group ID to delete tags from")

# define add_account params
add_account.add_argument('--id', type=str, required=True, help="Access Group ID to add the accounts to")
add_account.add_argument('--account_id', type=str, required=True, help="Account ID to be added")

# define add_account params
delete_account.add_argument('--id', type=str, required=True, help="Access Group ID to delete the account from")
delete_account.add_argument('--account_id', type=str, required=True, help="Account ID to be deleted")

# define add_policy params
add_policy.add_argument('--id', type=str, required=True, help="Access Group ID to add the policy to")
add_policy.add_argument('--policy_name', type=str, required=True, help="Policy name to be added to the Access Group")
add_policy.add_argument('--role_id', type=str, required=True, help="Role ID to be added to the Access Group policy")

# define delete_policy params
delete_policy.add_argument('--id', type=str, required=True, help="Access Group ID to delete the account from")
delete_policy.add_argument('--policy_id', type=str, required=True, help="Policy ID to be deleted")

# force help if no parms
args = parser.parse_args(args=None if sys.argv[1:] else ['--help'])

# Start processing
dct_read_config(args.config)

dct_base_url = "/access-groups"

if args.command == 'view':
    rs = dct_view_by_id(dct_base_url, args.id)
    print(rs)

if args.command == 'list':
    rs = dct_search("Access Groups", dct_base_url, None, "No Access Groups defined.", args.format)
    print(rs)

if args.command == 'search':
    rs = dct_search("Access Group", dct_base_url, args.filter, "No Access Group match the search criteria.",
                    args.format)
    print(rs)

if args.command == "create":
    access_group_update(dct_base_url, args.name, args.role_id)

if args.command == "update":
    payload = {"name": args.name}
    rs = url_PATCH(dct_base_url + "/" + urllib.parse.quote(args.id), payload)
    if rs.status_code == 200:
        print("Access Group " + args.id + " Name has been updated with new name " + args.name)
    else:
        print(f"ERROR: Status = {rs.status_code} - {rs.text}")
        sys.exit(1)

if args.command == "delete":
    rs = dct_delete_by_id(dct_base_url, "Access Group Deleted", args.id, 204)
    print(rs)

if args.command == 'tag_create':
    payload = {"tags": args.tags}
    rs = dct_post_by_id(dct_base_url, args.id, payload, "tags")
    if rs.status_code == 200:
        print("Create tags for Account - ID=" + args.id)
    else:
        print(f"ERROR: Status = {rs.status_code} - {rs.text}")
        sys.exit(1)

if args.command == 'tag_list':
    rs = dct_list_by_id(dct_base_url, args.id, "/tags", args.format)
    print(rs)

if args.command == 'tag_delete':
    payload = {"key": args.key}
    rs = dct_post_by_id(dct_base_url, args.id, payload, "tags/delete")
    if rs.status_code == 200:
        print("Delete tag for Masking Job Set - ID=" + args.id)
    else:
        print(f"ERROR: Status = {rs.status_code} - {rs.text}")
        sys.exit(1)

if args.command == 'tag_delete_all':
    payload = {}
    rs = dct_post_by_id(dct_base_url, args.id, payload, "tags/delete")
    if rs.status_code == 200:
        print("Deleted all tags for Masking Job Set - ID=" + args.id)
    else:
        print(f"ERROR: Status = {rs.status_code} - {rs.text}")
        sys.exit(1)

if args.command == 'add_account':
    payload = {"account_ids": [args.account_id]}
    rs = dct_post_by_id(dct_base_url, args.id, payload, "account-ids")
    if rs.status_code == 200:
        print("Added account(s) with ID " + args.account_id + " to Access Group ID " + args.id)
    else:
        print(f"ERROR: Status = {rs.status_code} - {rs.text}")
        sys.exit(1)

if args.command == "delete_account":
    dct_delete_ref_by_id(dct_base_url, "Account ID " + args.account_id + " deleted from Access Group ID" + args.id,
                         args.id, "account-ids", args.account_id)

if args.command == 'add_policy':
    payload = {"policies": [{
        "name": args.policy_name,
        "role_id": args.role_id
    }]}
    rs = dct_post_by_id(dct_base_url, args.id, payload, "policies")
    if rs.status_code == 200:
        print("Added Policy " + args.policy_name + " with role " + args.role_id + " to Access Group ID " + args.id)
    else:
        print(f"ERROR: Status = {rs.status_code} - {rs.text}")
        sys.exit(1)

if args.command == 'delete_policy':
    dct_delete_ref_by_id(dct_base_url, "Policy ID " + args.policy_id + " deleted from Access Group ID" + args.id,
                         args.id, "policies", args.policy_id)
