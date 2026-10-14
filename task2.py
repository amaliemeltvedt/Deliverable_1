# Importing necessary packages
import requests
import pandas as pd
import os

# Reusing the code from task 1
from dotenv import load_dotenv
load_dotenv()
client_id = os.getenv("MET_CLIENT_ID")

# Changing the parameters to find precipitation 
endpoint = 'https://frost.met.no/observations/v0.jsonld'
parameters = {
'sources': 'SN17850',
'elements': 'sum(precipitation_amount P1D)',
'referencetime': '2025-01-01/2025-12-31',
}

# From the example code
# Issue an HTTP GET request
r = requests.get(endpoint, parameters, auth=(client_id,''))
# Extract JSON data
json = r.json()

# From the example code
# Check if the request worked, print out any errors
if r.status_code == 200:
    data = json['data']
    print('Data retrieved from frost.met.no!')
else:
    print('Error! Returned status code %s' % r.status_code)
    print('Message: %s' % json['error']['message'])
    print('Reason: %s' % json['error']['reason'])
    
# Printing the first data points to check if it worked
print(data[:3])