from flask_cors import CORS
from flask import Flask, jsonify, request
import yfinance as yf
from datetime import datetime, timedelta
import pandas as pd

app = Flask(__name__)
CORS(app, origins="http://127.0.0.1:3000", allow_headers=["Content-Type"])


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

@app.route('/api/stock', methods=['GET'])
def get_stock_data():
    stock = request.args.get('stock')
    date_range = request.args.get('date_range')

    # Set interval based on the date_range
    interval = '5m'
    if date_range == 'Day':
        interval = '5m'
        start_date, end_date = get_start_end_dates(date_range)
        data = yf.download(stock, start=start_date, end=end_date, interval=interval)
        print(data)
        data.reset_index(inplace=True)
        data['Date'] = data['Datetime'].dt.strftime('%Y-%m-%d %H:%M:%S')
        print(data)
    elif date_range == 'Week':
        interval = '30m'
        start_date, end_date = get_start_end_dates(date_range)
        data = yf.download(stock, start=start_date, end=end_date, interval=interval)
        print(data)
        data.reset_index(inplace=True)
        data = data[data['Datetime'].dt.weekday < 5]
        data['Date'] = data['Datetime'].dt.strftime('%Y-%m-%d %H:%M:%S')
        

        print(data)
    elif date_range == 'Month':
        interval = '1d'
        start_date, end_date = get_start_end_dates(date_range)
        data = yf.download(stock, start=start_date, end=end_date, interval=interval)
        print(data)
        data.reset_index(inplace=True)
        data = data[data['Date'].dt.weekday < 5]

        data['Date'] = data['Date'].dt.strftime('%Y-%m-%d %H:%M:%S')

        print(data)

    return jsonify(data.to_dict(orient='records'))


if __name__ == '__main__':
    app.run(debug=True)
