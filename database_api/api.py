import time
import mysql.connector
from mysql.connector import Error
from datetime import datetime, timedelta
from data_ingestion.ingestion import fetch_and_insert_data  # Import the function from ingestion

# Connect to MySQL
connection = mysql.connector.connect(
    host='localhost',
    user='root',
    password='12345',
    port="3306",
    database='db'
)

def getData():
    # neu chua lay du lieu lan nao se lay du lieu tu 60 ngay truoc do
    last_fetched_time = datetime.utcnow() - timedelta(days=60)

    # chay trong vong lap
    while True:
        try:
            last_fetched_time = fetch_and_insert_data(last_fetched_time,connection)
            last_fetched_time = datetime.utcnow() - timedelta(minutes=30) # lay du lieu tu 30 phut truoc
            print("Waiting for the next fetch...")
            time.sleep(1800)  # Wait 30 minutes before the next fetch
        except KeyboardInterrupt:
            print("Script interrupted by the user. Exiting...")
            break
        except Exception as e:
            print(f"An error occurred: {e}")
            time.sleep(60)  # Wait 1 minute before retrying in case of failure


