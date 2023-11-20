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
    peak_streamflow_data = peak_streamflow_data[~peak_streamflow_data.iloc[:, 0].str.startswith('5s')]

    # Extract the datetimes of the peaks
    peak_datetimes = peak_streamflow_data['peak_dt']

    # For each peak datetime, download the corresponding year's worth of data
    for peak_datetime in peak_datetimes:
        # Construct the URL for one year of data (adjust the parameters as needed)
        year_start = peak_datetime.split('-')[0]
        year_end = str(int(year_start) + 1)
        data_url = f"https://nwis.waterservices.usgs.gov/nwis/iv/?sites=01302020&parameterCd=00060&startDT={year_start}-01-01&endDT={year_end}-01-01&siteStatus=all&format=rdb"

        # Send a GET request to the data URL
        data_response = requests.get(data_url)

        # Check if the request was successful (status code 200)
        if data_response.status_code == 200:
            # Convert the response content to a string and create a StringIO object
            data_string = StringIO(data_response.text)

            # Read the data into a Pandas DataFrame, skipping the disclaimer and unnecessary lines
            data_df = pd.read_csv(data_string, sep='\t', skiprows=30, comment='#')

            # Save the DataFrame to a TSV file in the "data" folder
            data_folder = "data"
            os.makedirs(data_folder, exist_ok=True)  # Create the folder if it doesn't exist
            data_df.to_csv(f'data/peak_streamflow_data_{peak_datetime}.tsv', sep='\t', index=False)
            print(f"Data for {peak_datetime} saved successfully.")
        else:
            print(f"Failed to retrieve data for {peak_datetime}. Check the URL or try again later.")
else:
    print("Failed to retrieve peak streamflow data. Check the URL or try again later.")
