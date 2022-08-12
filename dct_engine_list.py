#
# DCT engine list

import os
import sys
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

#force temporarily os environment vars
os.environ.setdefault('API_KEY', 'APK 2.YYgpjHxljW7A7gdU1Llu8ZiUacHw84gfbnuaqSXmNFpP8yFxsOxF1xt4urW9D3ZN')
os.environ.setdefault('HOST', 'https://uvo18oz1uisfurv1b4l.vm.cld.sr')

API_KEY = os.environ['API_KEY']
HOST = os.environ['HOST']

if API_KEY is None:
    raise Exception("Fill out valid API KEY")
if HOST is None:
    raise Exception("Fill out valid hostname")


#build api URL
command="v2/management/engines?limit=50&sort=id"
api_url=HOST+"/"+command

# build headers
headers= {}
headers['accept'] = "application/json"
headers['Authorization'] = API_KEY

response = requests.get(api_url, headers=headers, verify=False)

if response.status_code == 200:
    dct_output = response.json()['items']
    print(dct_output)
else:
    print(f"ERROR: Status = {response.status_code}")
    sys.exit(1)

# print list
for index in range(len(dct_output)):
    print(f"Engine {dct_output[index]['id']} = {dct_output[index]['uuid']}")