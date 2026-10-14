# Libraries needed (pandas is not standard and must be installed in Python)
import requests
import pandas as pd
import os
import matplotlib.pyplot as plt

# fra chat
from dotenv import load_dotenv
load_dotenv()
client_id = os.getenv("MET_CLIENT_ID")

# From the task description
endpoint = 'https://frost.met.no/observations/v0.jsonld'
parameters = {
'sources': 'SN17850',
'elements': 'mean(air_temperature P1D)',
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

# Extract dates and temperatures from the json-data

df = pd.DataFrame([
    {
        "date": entry["referenceTime"],
        "temperature": observation["value"]
    }
    for entry in data
    for observation in entry["observations"]
    if observation["timeOffset"] == "PT0H"
    ])

# Convert the dates to datetime objects
df["date"] = pd.to_datetime(df["date"])

# Making the plot
fig, ax = plt.subplots()
ax.plot(df["date"], df["temperature"])

# Formatting the plot
ax.set_xlabel("Date")
ax.set_ylabel("Temperature (°C)")
ax.set_title("Daily Mean Air Temperature in 2025 at SN17850")

# Make the x-axis labels more readable
fig.autofmt_xdate()

# Show the plot
plt.show()

# Making a summary table 
summary_table = df[["temperature"]].agg(["mean", "median", "min", "max"]).round(2)
print("\nSummary Table:")
print(summary_table)