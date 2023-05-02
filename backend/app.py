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

    running_buy = False
    running_sell = False
    in_a_buy = False
    in_a_sell = False
    for index, row in data.iterrows():
        net = row['Close'] - row['Open']

        if not running_buy and net > 0:
            running_buy = net

        if not running_sell and net < 0:
            running_sell = net

        if index == 0:
            continue
        

        if (net > running_buy) and not in_a_buy:
            data.at[index, 'buy_indicator'] = 1
            in_a_buy = True
            in_a_sell = False
            running_buy = False

        if (net < running_sell) and not in_a_sell:
            data.at[index, 'sell_indicator'] = 1
            in_a_sell = True
            in_a_buy = False
            running_sell = False

        if net > 0 and net > running_buy :
            running_buy = net

        if net < 0 and net < running_sell:
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
            'net': row['net'],
            'Line1': row['Line1'], 
            'Line2': row['Line2'],
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


if __name__ == '__main__':
    app.run(debug=True)
