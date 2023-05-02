from flask_cors import CORS
from flask import Flask, jsonify, request
import yfinance as yf
from datetime import datetime, timedelta
import pandas as pd

app = Flask(__name__)
CORS(app, origins="http://localhost:3000", allow_headers=["Content-Type"])

def process_stock_data(data):
    data['sell_indicator'] = 0
    data['buy_indicator'] = 0
    data['net'] = data['Close'] - data['Open']
    data['netabs'] = data['net'].abs()

    data['Line1'] = data['netabs'].rolling(window=5).mean()
    data['Line1'].iloc[0] = data['netabs'].iloc[0]
    data['Line1'].iloc[1] = (data['netabs'].iloc[0] + data['netabs'].iloc[1]) / 2
    data['Line1'].iloc[2] = (data['netabs'].iloc[0] + data['netabs'].iloc[1] + data['netabs'].iloc[2]) / 3
    data['Line1'].iloc[3] = (data['netabs'].iloc[0] + data['netabs'].iloc[1] + data['netabs'].iloc[2] + data['netabs'].iloc[3]) / 4


    data['Line2'] = data['Line1'] * -1

    data['Gas'] = data['net'].rolling(window=5).mean()
    data['Gas'].iloc[0] = data['net'].iloc[0]
    data['Gas'].iloc[1] = (data['net'].iloc[0] + data['net'].iloc[1]) / 2
    data['Gas'].iloc[2] = (data['net'].iloc[0] + data['net'].iloc[1] + data['net'].iloc[2]) / 3
    data['Gas'].iloc[3] = (data['net'].iloc[0] + data['net'].iloc[1] + data['net'].iloc[2] + data['net'].iloc[3]) / 4

    data['Gas'] = data['Gas'] * 2

    data['Avg_Close'] = data['Close'].rolling(window=3).mean()
    data['Avg_Open'] = data['Open'].rolling(window=3).mean()

    data['condition1'] = data['Avg_Close'] > data['Avg_Open']
    data['condition2'] = data['Avg_Close'] < data['Avg_Open']

    data['buy_indicator'] = data['condition1'].apply(lambda x: 1 if x else 0)
    data['sell_indicator'] = data['condition2'].apply(lambda x: 1 if x else 0)

    data.drop('condition1', axis=1, inplace=True)
    data.drop('condition2', axis=1, inplace=True)

    # for index, row in data.iterrows():
    return data


def convert_data_format(data):
    output = []
    for _, row in data.iterrows():
        output.append({
            'date': row['Date'],
            'open': row['Open'],
            'high': row['High'],
            'low': row['Low'],
            'close': row['Close'],
            'net': row['net'],
            'Line1': row['Line1'], 
            'Line2': row['Line2'],
            'Gas': row['Gas'],
            'buy_indicator': row['buy_indicator'],
            'sell_indicator': row['sell_indicator']
        })
    return output


def get_start_end_dates():
    end_date = datetime.now()
    start_date = end_date - timedelta(days=60)
    return start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')

@app.route('/api', methods=['GET'])
def get_stock_data():
    stock = request.args.get('stock')
    print("Stock: ", stock)
    interval = '1d'
    start_date, end_date = get_start_end_dates()
    data = yf.download(stock, start=start_date, end=end_date, interval=interval)
    data = data.reset_index()
    data = process_stock_data(data)
    print(data)
    data.reset_index(inplace=True)
    data['Date'] = data['Date'].dt.strftime('%Y-%m-%d')
    formatted_data = convert_data_format(data)
    return jsonify(formatted_data)


@app.route('/api-week', methods=['GET'])
def get_stock_data_week():
    stock = request.args.get('stock')
    print("Stock: ", stock)
    interval = '1wk' # changed to weekly interval
    start_date, end_date = get_start_end_dates()
    data = yf.download(stock, start=start_date, end=end_date, interval=interval)
    data = data.reset_index()
    data = process_stock_data(data)
    print(data)
    data.reset_index(inplace=True)
    data['Date'] = data['Date'].dt.strftime('%Y-%m-%d')
    formatted_data = convert_data_format(data)
    return jsonify(formatted_data)


if __name__ == '__main__':
    app.run(debug=True)
