# Libraries needed 

# note to self: in main ipynb file you only need to call on the df, everything under can be ignored
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
print(df["date"])
# from now on to main ipynb file

def calculate_moving_avg(temperatures):
    moving_avg = temperatures.rolling(window=7).mean() # calculates the mean of 7 days at a time
    return moving_avg

df["moving_avg"] = calculate_moving_avg(df["temperature"])

plt.scatter(df["date"], df["temperature"], label="Daily temperature", s=10)
plt.plot(df["date"], df["moving_avg"], label="7-day moving average")

plt.xlabel("Date")
plt.ylabel("Temperature (°C)")
plt.title("Daily temperature and 7-day moving average in 2025")
plt.legend()
plt.show()