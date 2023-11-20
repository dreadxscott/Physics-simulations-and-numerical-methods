import pandas as pd
import requests
import os
from io import StringIO

# Define the URL for peak streamflow data
url = "https://nwis.waterdata.usgs.gov/nwis/peak?site_no=01302020&agency_cd=USGS&format=rdb"

# Send a GET request to the URL
response = requests.get(url)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Convert the response content to a string and create a StringIO object
    data_string = StringIO(response.text)

    # Read the data into a Pandas DataFrame, skipping the disclaimer and unnecessary lines
    peak_streamflow_data = pd.read_csv(data_string, sep='\t', skiprows=72, comment='#')

    # Remove the unwanted row after the column names
    data_df = peak_streamflow_data[~peak_streamflow_data.iloc[:, 0].str.startswith('5s')]

    # Save the DataFrame to a TSV file in the "data" folder
    data_folder = "data"
    os.makedirs(data_folder, exist_ok=True)  # Create the folder if it doesn't exist

    # Save the DataFrame to a TSV file
    data_df.to_csv('data/peak_streamflow_data.tsv', sep='\t', index=False)
    print("Peak streamflow data saved successfully.")
else:
    print("Failed to retrieve data. Check the URL or try again later.")
