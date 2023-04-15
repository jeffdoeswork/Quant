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


def get_start_end_dates(date_range):
    end_date = datetime.now()
    if date_range == 'Day':
        start_date = end_date - timedelta(days=1)
    elif date_range == 'Week':
        start_date = end_date - timedelta(weeks=1)
    elif date_range == 'Month':
        start_date = end_date - timedelta(days=30)
    else:
        raise ValueError("Invalid date_range value")

    return start_date, end_date

@app.route('/api', methods=['GET'])
def get_stock_data():
    stock = request.args.get('stock')
    date_range = request.args.get('date_range')
    print("Stock: ", stock, " Date: ", date_range)
    # Set interval based on the date_range
    interval = '5m'
    start_date, end_date = get_start_end_dates(date_range)
    data = yf.download(stock, start=start_date, end=end_date, interval=interval)
    print(data)
    data.reset_index(inplace=True)
    data['Date'] = data['Datetime'].dt.strftime('%Y-%m-%d %H:%M:%S')
    formatted_data = convert_data_format(data)
    print(data)

    return jsonify(formatted_data)


if __name__ == '__main__':
    app.run(debug=True)
