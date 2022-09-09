from helpers import *


# TODO manage tags

def account_create(client_id, first_name, last_name, email, username, password, tags):
    tags_dic = json.loads(tags)
    payload = {"generate_api_key": 'true', "api_client_id": client_id, "first_name": first_name, "last_name": last_name,
               "email": email,
               "username": username, "password": password, "tags": tags_dic}
    resp = url_POST("/management/accounts", payload)
    if resp.status_code == 201:
        rsp = resp.json()
        print(f"Registered account with ID={rsp['id']}")
        return rsp
    else:
        print(f"ERROR: Status = {resp.status_code} - {resp.text}")
        sys.exit(1)


def account_delete(account_id):
    resp = url_DELETE("/management/accounts/" + urllib.parse.quote(account_id))
    if resp.status_code == 204:
        print(f"Deleted Account with ID={account_id}")
        return
    else:
        print(f"ERROR: Status = {resp.status_code} - {resp.text}")
        sys.exit(1)
