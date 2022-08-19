from helpers import *

# Engine API
#
#TODO implement
# POST /management/engines/{engineId}/tags
# Create tags for a engine.
# GET /management/engines/{engineId}/tags
# Get tags for a Engine.
# POST /management/engines/{engineId}/tags/delete
# Delete tags for an Engine.
# GET /management/vaults/hashicorp
# Returns a list of configured Hashicorp vaults.
# POST /management/vaults/hashicorp
# Configure a new Hashicorp Vault
# GET /management/vaults/hashicorp/{vaultId}
# Get a Hashicorp vault by id
# DELETE /management/vaults/hashicorp/{vaultId}
# Delete a Hashicorp vault by id
# GET /management/smtp
# Returns the SMTP configuration
# PUT /management/smtp
# Update SMTP Config.
# POST /management/smtp/validate
# Validate SMTP Config.

def engine_list():
    resp = url_GET("/management/engines?limit=50&sort=id")
    if resp.status_code == 200:
        report_data = resp.json()['items']
        if report_data:
            tabular_report("DELPHIX Data Control Tower - ENGINE LIST",report_data)
            return report_data
        else:
            print(f"\nNo Engines defined.")
            return
    else:
        print(f"ERROR: Status = {resp.status_code} - {resp.text}")
        sys.exit(1)
    return

def engine_search(FILTER):
    payload = {}
    payload["filter_expression"] = "SEARCH '"+FILTER+"'"
    resp = url_POST("/management/engines/search?limit=50&sort=id",payload)
    if resp.status_code == 200:
        report_data = resp.json()['items']
        if report_data:
            tabular_report("DELPHIX Data Control Tower - ENGINE SEARCH",report_data)
            return report_data
        else:
            print(f"\nNo Engines match search criteria.")
            return
    else:
        print(f"ERROR: Status = {resp.status_code} - {resp.text}")
        sys.exit(1)
    return

def engine_delete(ENGINE_ID):
    resp = url_DELETE("/management/engines/"+urllib.parse.quote(ENGINE_ID))
    if resp.status_code == 200:
        print(f"Deleted engine with ID={ENGINE_ID}")
        return resp.json()
    else:
        print(f"ERROR: Status = {resp.status_code} - {resp.text}")
        sys.exit(1)
    return

def engine_register(NAME, HOSTNAME, USER, PASSWORD, INSECURE_SSL, UNSAFE_SSL):
    #TODO add hashicorp, trustore and tags
    payload = {}
    payload["name"] = NAME
    payload["hostname"] = HOSTNAME
    payload["username"] = USER
    payload["password"] = PASSWORD
    payload["insecure_ssl"] = INSECURE_SSL
    payload["unsafe_ssl_hostname_check"] = UNSAFE_SSL
    resp = url_POST("/management/engines",payload)
    if resp.status_code == 201:
        print(f"Registered engine with ID={resp['id']}")
        return resp.json()
    else:
        print(f"ERROR: Status = {resp.status_code} - {resp.text}")
        sys.exit(1)
    return

def engine_by_id(ENGINE_ID):
    resp = url_GET("/management/engines/"+ENGINE_ID)
    if resp.status_code == 200:
        return resp.json()
    else:
        print(f"ERROR: Status = {resp.status_code} - {resp.text}")
        sys.exit(1)
    return
