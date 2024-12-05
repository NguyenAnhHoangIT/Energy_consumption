from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)

@app.route('/get_energy_data', methods=['GET'])
def get_energy_data():

    return jsonify()

if __name__ == '__main__':
    app.run(debug=True)

