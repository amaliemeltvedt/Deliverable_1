# Reusing code from task 1 and 2
# Importing necessary packages

import requests
import pandas as pd
import os
import matplotlib.pyplot as plt

# Reusing the code from task 1
from dotenv import load_dotenv
load_dotenv()
client_id = os.getenv("MET_CLIENT_ID")

# From the task description, reused from task 1
# Switched elements to max instead of mean
endpoint = 'https://frost.met.no/observations/v0.jsonld'
parameters = {
'sources': 'SN17850',
'elements': 'max(air_temperature P1D)',
'referencetime': '2025-01-01/2025-12-31',
}

# From the example code, reused from 1
# Issue an HTTP GET request for air temp
temperature_response = requests.get(endpoint, parameters, auth=(client_id,''))
# Extract JSON data
temperature_data = temperature_response.json()["data"]

# Fetch station information
source_endpoint = 'https://frost.met.no/sources/v0.jsonld'

source_response = requests.get(
    source_endpoint,
    params={'ids': parameters['sources']},
    auth=(client_id, '')
)

source_data = source_response.json()
station_name = source_data["data"][0]["name"]

# Extract dates and values for temperature
temperature_dates = [
    item["referenceTime"] for item in temperature_data
]
temperatures = [
    item["observations"][0]["value"] for item in temperature_data
]

# Convert dates to datetime objects
temperature_dates = pd.to_datetime(temperature_dates)

# Creating empty lists for the for loop
consecutive_days = 0
heatwaves = []
start_date = None
end_date = None

# Creating a for loop to add one day if temp is above 27
# It then adds to heatwave count if it lasted over 5 days
# It also adds the dates
for date, temperature in zip(temperature_dates, temperatures):
    if temperature >= 27:
        if consecutive_days == 0:
            start_date = date

        consecutive_days += 1
        end_date = date

    else:
        if consecutive_days >= 5:
            dates = f"{start_date.date()} - {end_date.date()}"
            heatwaves.append(dates)

        consecutive_days = 0
        
# Checking again in case a heatwave continues after the last day of the data set       
if consecutive_days >= 5:
    dates = f"{start_date.date()} - {end_date.date()}"
    heatwaves.append(dates)
        
# Making a function to print using the yml format
def print_summary():
    print("dates:")
    for date in heatwaves:
        print(f"- {date}")

    print(f"station_id: {parameters['sources']}")
    print(f"station_name: {station_name}")
    print(f"year: {parameters['referencetime'][:4]}")
    
print_summary()