from flask_cors import CORS
from flask import Flask, jsonify, request
import yfinance as yf
from datetime import datetime, timedelta
import pandas as pd

app = Flask(__name__)
CORS(app, origins="http://127.0.0.1:3000", allow_headers=["Content-Type"])

def process_stock_data(data):
    data['sell_indicator'] = 0
    data['buy_indicator'] = 0

    running_buy = 0
    running_sell = 0
    in_a_buy = False
    in_a_sell = False
    for index, row in data.iterrows():
        if index == 0:
            continue

        net = row['Close'] - row['Open']

        if (net > 0) and (net > running_buy) and not in_a_buy:
            data.at[index, 'buy_indicator'] = 1
            in_a_buy = True
            in_a_sell = False
            running_sell = 0
            
        if (net < 0) and (net < running_sell) and not in_a_sell:
            data.at[index, 'sell_indicator'] = 1
            in_a_sell = True
            in_a_buy = False
            running_buy = 0
            

        if net > 0:
            running_buy = net
        if net < 0:
            running_sell = net


            
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
            'buy_indicator': row['buy_indicator'],
            'sell_indicator': row['sell_indicator']
        })
    return output



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
    data = process_stock_data(data)
    print(data)
    data.reset_index(inplace=True)
    data['Date'] = data['Datetime'].dt.strftime('%Y-%m-%d %H:%M:%S')
    formatted_data = convert_data_format(data)
    return jsonify(formatted_data)


if __name__ == '__main__':
    app.run(debug=True)
