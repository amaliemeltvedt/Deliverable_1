# importing necessary packages
import requests
import pandas as pd
import os
from dotenv import load_dotenv
import matplotlib.dates as mdates
import matplotlib.pyplot as plt

# Load MET client ID
load_dotenv()
client_id = os.getenv("MET_CLIENT_ID")

# From the task description
endpoint = 'https://frost.met.no/observations/v0.jsonld'

# Store data for both years in a dictionary
temperature_data = {}

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
        temperature_data[year] = json_data["data"]
        print(f'Data for {year} retrieved from frost.met.no!')
    else:
        print(f'Error retrieving data for {year}! Returned status code {r.status_code}')
        print('Message: %s' % json_data['error']['message'])
        print('Reason: %s' % json_data['error']['reason'])

# Extract data for 1925 and store in a DataFrame
df_1925 = pd.DataFrame([
    {
        "date": entry["referenceTime"],
        "temperature": observation["value"]
    }
    for entry in temperature_data[1925]
    for observation in entry["observations"]
    if observation["timeOffset"] == "PT0H"
])

# Extract data for 2025 and store in a DataFrame
df_2025 = pd.DataFrame([
    {
        "date": entry["referenceTime"],
        "temperature": observation["value"]
    }
    for entry in temperature_data[2025]
    for observation in entry["observations"]
    if observation["timeOffset"] == "PT0H"
])

# Convert the dates to datetime objects
df_1925["date"] = pd.to_datetime(df_1925["date"])
df_2025["date"] = pd.to_datetime(df_2025["date"])

# Create a new date for plotting purposes, setting the year to 2000 for both datasets
df_1925["plot_date"] = pd.to_datetime(
    "2000-" + df_1925["date"].dt.strftime("%m-%d")
)
df_2025["plot_date"] = pd.to_datetime(
    "2000-" + df_2025["date"].dt.strftime("%m-%d")
)

# Making the plot
fig, ax = plt.subplots()

ax.plot(
    df_1925["plot_date"],
    df_1925["temperature"],
    label="1925",
    color='pink'
)
ax.plot(
    df_2025["plot_date"],
    df_2025["temperature"],
    label="2025",
    color='purple'
)

ax.set_xlabel("Month")
ax.set_ylabel("Temperature (°C)")
ax.set_title("Temperature in 1925 and 2025 at SN17850")

# Show only month on the x-axis
ax.xaxis.set_major_locator(mdates.MonthLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter("%b"))

ax.legend()
fig.tight_layout()
plt.show() 

# Making a summary-table of 1925 and 2025
summary_table = pd.DataFrame({
    "1925": df_1925["temperature"].agg(["mean", "median", "min", "max"]),
    "2025": df_2025["temperature"].agg(["mean", "median", "min", "max"])
}).round(2)

print("\nSummary Table:")
print(summary_table)

