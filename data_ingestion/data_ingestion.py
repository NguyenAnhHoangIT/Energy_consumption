import requests
import mysql.connector
from mysql.connector import Error
from datetime import datetime, timedelta, timezone
import time

def fetch_and_insert_data(last_fetched_time):
    start_time = last_fetched_time.strftime('%Y-%m-%dT%H:%M:%SZ')
    current_time = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')

    # API URL with time filters
    api_url = f"https://api.gridstatus.io/v1/datasets/caiso_fuel_mix/query?api_key=0287b26403464cf3921101a5c07e97b4&start_time={start_time}&end_time={current_time}"

    print(f"Fetching data from {start_time} to {current_time}...")

    response = requests.get(api_url)

    if response.status_code == 200:
        data = response.json()  
    else:
        print(f"Failed to fetch data from API. Status code: {response.status_code}")
        return last_fetched_time

    if data:
        connection = None  

        try:
            connection = mysql.connector.connect(
                host='localhost',
                user='root',
                password='0915146847',
                database='db'
            )

            if connection.is_connected():
                cursor = connection.cursor()

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

                connection.commit()

                print(f"{cursor.rowcount} records inserted successfully.")

                last_fetched_time = datetime.now(timezone.utc)

        except Error as e:
            print(f"Error: {e}")
        finally:
            if connection and connection.is_connected():
                cursor.close()
                connection.close()
                print("MySQL connection closed.")
    time.sleep(300)

last_fetched_time = datetime.now(timezone.utc) - timedelta(days=1)
fetch_and_insert_data(last_fetched_time)
print("Fetching data completed.")
