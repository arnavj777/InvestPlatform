from flask import Flask, jsonify, Response
import pandas as pd
import mplfinance as mpf
import io

app = Flask(__name__)

@app.route('/api/data')
def get_data():
    return jsonify({'message': 'Hello from Flask!'})

if __name__ == '__main__':
    app.run(debug=True)
