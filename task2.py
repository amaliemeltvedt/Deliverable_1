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
endpoint = 'https://frost.met.no/observations/v0.jsonld'
parameters = {
'sources': 'SN17850',
'elements': 'mean(air_temperature P1D)',
'referencetime': '2025-01-01/2025-12-31',
}

# From the example code, reused from 1
# Issue an HTTP GET request for air temp
temperature_response = requests.get(endpoint, parameters, auth=(client_id,''))
# Extract JSON data
temperature_data = temperature_response.json()["data"]

# Changing the parameters to find precipitation instead
# Set timeoffsets to default so only PT6H data is used
# Frost recommended to not use PT18H (according to ChatGPT)
endpoint = 'https://frost.met.no/observations/v0.jsonld'
parameters = {
'sources': 'SN17850',
'elements': 'sum(precipitation_amount P1D)',
'referencetime': '2025-01-01/2025-12-31',
"timeoffsets": "default"
}

# From the example code, modified for precipitation
# Issue an HTTP GET request for precipitation
precipitation_response = requests.get(endpoint, parameters, auth=(client_id,''))
# Extract JSON data
precipitation_data = precipitation_response.json()["data"]


# Everything under is by help from ChatGPT
# See AI chat log
  
# Extract dates and values for temperature
temperature_dates = [
    item["referenceTime"] for item in temperature_data
]
temperatures = [
    item["observations"][0]["value"] for item in temperature_data
]

# Extract dates and values for precipitation
precipitation_dates = [
    item["referenceTime"] for item in precipitation_data
]
precipitation = [
    item["observations"][0]["value"] for item in precipitation_data
]

# Convert dates to datetime objects
temperature_dates = pd.to_datetime(temperature_dates)
precipitation_dates = pd.to_datetime(precipitation_dates)

# Making the plot
fig, ax1 = plt.subplots()

# For temperature
ax1.plot(
    temperature_dates, temperatures,
    marker=".", markersize=2, label="Temperature"
)
ax1.set_ylabel("Temperature (°C)")

# For precipitation
ax2 = ax1.twinx()
ax2.bar(
    precipitation_dates, precipitation,
    width=0.5, alpha=0.4, label="Precipitation"
)
ax2.set_ylabel("Precipitation (mm)")

# Adding legend for readability
ax1.legend(loc="upper left")
ax2.legend(loc="upper right")

# Adding title
plt.title("Daily temperature and precipitation in 2025")
fig.autofmt_xdate() 
plt.show()