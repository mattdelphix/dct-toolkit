import sys
def unpack_postgres_properties(config):
    # splits a string in the format var=value:True or var:value=False in a list of dictionaries
    if config == "":
        return []
    # create dictionary
    my_dict = {key: value for key, value in [item.split(
        '=') for item in config.split(' ')]}
    conf_final = []
    for key, value in my_dict.items():
        if ":" not in value:
            print("ERROR: Postgres properties must be in the format 'var=value:True' or 'var:value=False'")
            sys.exit(1)
        v, b = value.split(':')
        if b not in ['False','True']:
            print("ERROR: Postgres properties must be in the format 'var=value:True' or 'var:value=False'")
            sys.exit(1)
        t = {"propertyName": key, "value": v, "commentProperty": b}
        conf_final.append(t)
    return conf_final

my_str = "var=value:True var1=value1:False"

print(unpack_postgres_properties(my_str))
