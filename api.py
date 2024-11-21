import requests
import mysql.connector
from mysql.connector import Error

# 1. Fetch data from the API
api_url = "https://api.gridstatus.io/v1/datasets/caiso_fuel_mix/query?api_key=734c5f6f8951487d90de7ef8ccb75832&limit=1000"
response = requests.get(api_url)
data = response.json()  # assuming the data is returned in JSON format

# 2. Connect to MySQL
try:
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='12345',
        database='db'
    )
    
    if connection.is_connected():
        cursor = connection.cursor()

        # 3. Prepare and execute the INSERT statement
        insert_query = """
                        INSERT INTO energy_data (
                        interval_start_utc, interval_end_utc, solar, wind, geothermal, biomass, biogas, 
                        small_hydro, coal, nuclear, natural_gas, large_hydro, batteries, imports, other
                        ) VALUES (
                            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                        )
                    """

        # Assuming 'data' contains a list of records with keys 'timestamp', 'fuel_type', 'percentage'
        for record in data['data']:
            values = (
                record['interval_start_utc'], record['interval_end_utc'], record['solar'], 
                record['wind'], record['geothermal'], record['biomass'], record['biogas'], 
                record['small_hydro'], record['coal'], record['nuclear'], record['natural_gas'], 
                record['large_hydro'], record['batteries'], record['imports'], record['other']
                )

            # Execute insert query
            cursor.execute(insert_query, values)

        # Commit the transaction
        connection.commit()

        print(f"{cursor.rowcount} records inserted successfully.")

except Error as e:
    print(f"Error: {e}")

