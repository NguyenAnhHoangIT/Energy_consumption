import requests
import mysql.connector
from mysql.connector import Error
import time
from datetime import datetime, timedelta

# Function to fetch and insert data into the database
def fetch_and_insert_data(last_fetched_time):
    # Format the time in UTC as required by the API
    start_time = last_fetched_time.strftime('%Y-%m-%dT%H:%M:%SZ')
    current_time = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')

    # API URL with time filters
    api_url = f"https://api.gridstatus.io/v1/datasets/caiso_fuel_mix/query?api_key=734c5f6f8951487d90de7ef8ccb75832&start_time={start_time}&end_time={current_time}"

    print(f"Fetching data from {start_time} to {current_time}...")

    response = requests.get(api_url)

    # Check if the API request was successful
    if response.status_code == 200:
        data = response.json()  # assuming the data is returned in JSON format
    else:
        print(f"Failed to fetch data from API. Status code: {response.status_code}")
        return last_fetched_time

    if data:
        try:
            # Connect to MySQL
            connection = mysql.connector.connect(
                host='localhost',
                user='root',
                password='12345',
                database='db'
            )

            if connection.is_connected():
                cursor = connection.cursor()

                # Prepare the INSERT statement
                insert_query = """
                                INSERT INTO energy_data (
                                interval_start_utc, interval_end_utc, solar, wind, geothermal, biomass, biogas, 
                                small_hydro, coal, nuclear, natural_gas, large_hydro, batteries, imports, other
                                ) VALUES (
                                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                                )
                            """

                # Insert each record
                for record in data.get('data', []):
                    values = (
                        record.get('interval_start_utc', None), record.get('interval_end_utc', None), record.get('solar', None), 
                        record.get('wind', None), record.get('geothermal', None), record.get('biomass', None), record.get('biogas', None), 
                        record.get('small_hydro', None), record.get('coal', None), record.get('nuclear', None), record.get('natural_gas', None), 
                        record.get('large_hydro', None), record.get('batteries', None), record.get('imports', None), record.get('other', None)
                    )
                    cursor.execute(insert_query, values)

                # Commit the transaction
                connection.commit()

                print(f"{cursor.rowcount} records inserted successfully.")

                # Update the last fetched time to the current time
                last_fetched_time = datetime.utcnow()

        except Error as e:
            print(f"Error: {e}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
                print("MySQL connection closed.")

    return last_fetched_time

# Main loop to fetch new data every 30 minutes
last_fetched_time = datetime.utcnow() - timedelta(days=1)  # Start with 24 hours back

while True:
    last_fetched_time = fetch_and_insert_data(last_fetched_time)
    print("Waiting for the next fetch...")
    time.sleep(1800)  # Wait 30 minutes before the next fetch
