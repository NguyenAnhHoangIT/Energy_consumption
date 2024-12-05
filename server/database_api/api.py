import time
import mysql.connector
import pandas as pd
from mysql.connector import Error
from datetime import datetime, timedelta
import sys
sys.path.append('..')
from server.data_ingestion.ingestion import *  # Import the function from ingestion


# Connect to MySQL
connection = mysql.connector.connect(
    host='localhost',
    user='root',
    password='12345',
    port="3306",
    database='db'
)
def getAll(table_name):
    try:
        # Create a cursor to execute SQL queries
        cursor = connection.cursor(dictionary=True)
        
        # Define the query
        query = f"SELECT * FROM {table_name}"
        
        # Execute the query
        cursor.execute(query)
        
        # Fetch all rows
        result = cursor.fetchall()
        
        df = pd.DataFrame(result)

        # Close the cursor
        cursor.close()
        
        return df
    except Error as e:
        print(f"Error: {e}")
        return None

def getColumn(col_name):
    try:
        # Create a cursor to execute SQL queries
        cursor = connection.cursor(dictionary=True)
        
        # Define the query
        query = f"select id, interval_start_utc, interval_end_utc, {col_name} from energy_data"
        
        # Execute the query
        cursor.execute(query)
        
        # Fetch all rows
        result = cursor.fetchall()
        
        df = pd.DataFrame(result)

        # Close the cursor
        cursor.close()
        
        return df
    except Error as e:
        print(f"Error: {e}")
        return None
    
def getData():
    # neu chua lay du lieu lan nao se lay du lieu tu 4 nam truoc do
    start_date = datetime.utcnow() - timedelta(days=365*3)
    while start_date < datetime.utcnow():
        # Fetch data for the current month
        last_fetched_time = fetch_and_insert_data_range(start_date,connection)
        print(f"Fetched data for {start_date.strftime('%Y-%m')}")
        # Increment the start date by 2 month
        start_date += timedelta(days=60)
    last_fetched_time = start_date
    # chay trong vong lap
    while True:
        try:
            last_fetched_time = fetch_and_insert_data(last_fetched_time,connection)
            last_fetched_time = datetime.utcnow() - timedelta(minutes=5) # lay du lieu tu 5 phut truoc
            print("Waiting for the next fetch...")
            time.sleep(300)  # Wait 5 minutes before the next fetch
        except KeyboardInterrupt:
            print("Script interrupted by the user. Exiting...")
            break
        except Exception as e:
            print(f"An error occurred: {e}")
            time.sleep(60)  # Wait 1 minute before retrying in case of failure


