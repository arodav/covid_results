import requests
import json

from argparse import ArgumentParser

parser = ArgumentParser(description='Process some args.')

parser.add_argument('--url', dest='url',help='Web page hosting the REST API.')
parser.add_argument('--field', dest='field',help='GET request in JSON format.', required=False)
parser.add_argument('--value', dest='value',help='GET request in JSON format.', required=False)

args = parser.parse_args()

request = {args.field: args.value}

if not request:
    path = f"{args.url}/api/v1/country_test_done/all"
    query = None
else:
    path = f'{args.url}/api/v1/country_test_done'
    query = request

# GET request
response = requests.get(path,params=query)
print(response.text)

# http://127.0.0.1:5000