from helpers import *


# Engine API
#
# TODO implement
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


def engine_delete(engine_id):
    resp = url_DELETE("/management/engines/" + urllib.parse.quote(engine_id))
    if resp.status_code == 204:
        print(f"Deleted engine with ID={engine_id}")
        return resp.json()
    else:
        print(f"ERROR: Status = {resp.status_code} - {resp.text}")
        sys.exit(1)


def engine_register(name, hostname, user, password, insecure_ssl, unsafe_ssl):
    # TODO add hashicorp, trustore and tags
    payload = {"name": name, "hostname": hostname, "username": user, "password": password, "insecure_ssl": insecure_ssl,
               "unsafe_ssl_hostname_check": unsafe_ssl}
    resp = url_POST("/management/engines", payload)
    if resp.status_code == 201:
        print(f"Registered engine with ID={resp['id']}")
        return resp.json()
    else:
        print(f"ERROR: Status = {resp.status_code} - {resp.text}")
        sys.exit(1)
