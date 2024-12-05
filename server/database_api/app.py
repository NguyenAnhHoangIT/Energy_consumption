from flask import Flask, jsonify
from flask_cors import CORS
import pymysql

app = Flask(__name__)
CORS(app)  # Cho phép Frontend kết nối đến API

# Cấu hình kết nối MySQL
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '12345',
    'database': 'db'
}

@app.route('/get_energy_data', methods=['GET'])
def get_energy_data():
    # Kết nối tới MySQL
    connection = pymysql.connect(**db_config)
    cursor = connection.cursor(pymysql.cursors.DictCursor)

    # Truy vấn toàn bộ dữ liệu và sắp xếp theo interval_end_utc
    query = """
        SELECT *
        FROM energy_data
        ORDER BY interval_end_utc
    """
    cursor.execute(query)
    rows = cursor.fetchall()

    # Đóng kết nối
    cursor.close()
    connection.close()

    return jsonify(rows)

