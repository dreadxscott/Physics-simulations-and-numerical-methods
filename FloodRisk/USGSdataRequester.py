import os
import requests
import pandas as pd
from io import StringIO

def download_water_data(site, parameter, start_date, end_date):
    # Customize the URL based on user input
    url = f"https://nwis.waterservices.usgs.gov/nwis/iv/?sites={site}&parameterCd={parameter}&startDT={start_date}&endDT={end_date}&siteStatus=all&format=rdb"

    # Send a GET request to the URL
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Convert the response content to a string
        data_str = response.text

        # Use StringIO to create a file-like object from the string
        data_io = StringIO(data_str)

        # Read the data into a DataFrame, skipping the first row after the header and keeping the header names
        data_df = pd.read_csv(data_io, sep='\t', comment='#', skiprows=27)

        # Remove the unwanted row after the column names
        data_df = data_df[~data_df.iloc[:, 0].str.startswith('5s')]

        # Save the DataFrame to a TSV file in the "data" folder
        data_folder = "data"
        os.makedirs(data_folder, exist_ok=True)  # Create the folder if it doesn't exist

        # Extract the parameter code from the URL
        parameter_code = url.split('&')[1].split('=')[1]

        file_name = os.path.join(data_folder, f"{site}_{start_date}_to_{end_date}_{parameter_code}_data.tsv")
        data_df.to_csv(file_name, sep='\t', index=False)

        print(f"Data downloaded and saved successfully as {file_name}.")
    else:
        print(f"Error: Unable to fetch data. Status code: {response.status_code}")

# Example usage:
site_code = "01302020"  # Replace with your desired site code
parameter_code = "00060"  # Replace with your desired parameter code
start_date = "2022-11-17T21:55:18.097-05:00"  # Replace with your desired start date
end_date = "2023-11-17T21:55:18.097-05:00"    # Replace with your desired end date

download_water_data(site_code, parameter_code, start_date, end_date)
