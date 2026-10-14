# importing necessary packages
import requests
import pandas as pd
import os
from dotenv import load_dotenv

# Load MET client ID
load_dotenv()
client_id = os.getenv("MET_CLIENT_ID")

# From the task description
endpoint = 'https://frost.met.no/observations/v0.jsonld'

# Store data for both years in a dictionary
weather_data = {}

# Loading data from 1925 and 2025
for year in [1925, 2025]:
    parameters = {
        'sources': 'SN17850',
        'elements': 'mean(air_temperature P1D)',
        'referencetime': f'{year}-01-01/{year}-12-31',
    }

    # Issue an HTTP GET request
    r = requests.get(endpoint, parameters, auth=(client_id,''))
    # Extract JSON data
    json_data = r.json()

    # Check if the request worked, print out any errors
    if r.status_code == 200:
        weather_data[year] = json_data["data"]
        print(f'Data for {year} retrieved from frost.met.no!')
    else:
        print(f'Error retrieving data for {year}! Returned status code {r.status_code}')
        print('Message: %s' % json_data['error']['message'])
        print('Reason: %s' % json_data['error']['reason'])
