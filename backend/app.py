from flask_cors import CORS
from flask import Flask, jsonify, request
import yfinance as yf
from datetime import datetime, timedelta
import pandas as pd

app = Flask(__name__)
CORS(app, origins="http://127.0.0.1:3000", allow_headers=["Content-Type"])

def convert_data_format(data):
    new_data = []
    for index, row in data.iterrows():
        new_data.append({
            'date': row['Date'],
            'open': row['Open'],
            'high': row['High'],
            'low': row['Low'],
            'close': row['Close'],
            'green': row['Close'] > row['Open'],
            'red': row['Close'] < row['Open'],
        })

    return new_data


def get_start_end_dates(date):
    start_date = datetime.strptime(date, "%Y-%m-%d")
    end_date = start_date + timedelta(days=1)
    return start_date, end_date


@app.route('/api', methods=['GET'])
def get_stock_data():
    stock = request.args.get('stock')
    date = request.args.get('date')
    print("Stock: ", stock, " Date: ", date)
    interval = '5m'
    start_date, end_date = get_start_end_dates(date)
    data = yf.download(stock, start=start_date, end=end_date, interval=interval)
    print(data)
    data.reset_index(inplace=True)
    data['Date'] = data['Datetime'].dt.strftime('%Y-%m-%d %H:%M:%S')
    formatted_data = convert_data_format(data)
    return jsonify(formatted_data)


if __name__ == '__main__':
    app.run(debug=True)
