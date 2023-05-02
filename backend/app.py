from flask_cors import CORS
from flask import Flask, jsonify, request
import yfinance as yf  # use IEX Cloud one day
from datetime import datetime, timedelta
import pandas as pd

app = Flask(__name__)
CORS(app, origins="http://localhost:3000", allow_headers=["Content-Type"])
def get_current_day_ohlc(symbol):
    # Fetch intraday data for the stock with a 5-minute interval
    data = yf.download(tickers=symbol, interval='5m', period='1d')
    print("hey look at me download data: ", data)
    # Calculate Open, High, Low, and Close for the current day
    open_price = data.iloc[0]['Open']
    high_price = data['High'].max()
    low_price = data['Low'].min()
    close_price = data.iloc[-1]['Close']
    end_date = datetime.now()


    # Create a DataFrame with the consolidated OHLC data
    ohlc_data = pd.DataFrame({'Open': [open_price],
                              'High': [high_price],
                              'Low': [low_price],
                              'Close': [close_price],},
                             index=[data.index[0].date()])
    ohlc_data['Date'] = end_date

    return(ohlc_data)

def process_stock_data(data, length):
    data['sell_indicator'] = 0
    data['buy_indicator'] = 0
    data['net'] = data['Close'] - data['Open']
    data['netabs'] = data['net'].abs()

    if length == "week":

        data['Line1'] = data['netabs'].rolling(window=5).mean()
        data['Line1'].iloc[0] = data['netabs'].iloc[0]
        data['Line1'].iloc[1] = (data['netabs'].iloc[0] + data['netabs'].iloc[1]) / 2
        data['Line1'].iloc[2] = (data['netabs'].iloc[0] + data['netabs'].iloc[1] + data['netabs'].iloc[2]) / 3
        data['Line1'].iloc[3] = (data['netabs'].iloc[0] + data['netabs'].iloc[1] + data['netabs'].iloc[2] + data['netabs'].iloc[3]) / 4


        data['Line2'] = data['Line1'] * -1

        data['Gas'] = data['net'].rolling(window=5).mean()
        data['Gas'].iloc[0] = 0
        data['Gas'].iloc[1] = (data['net'].iloc[0] + data['net'].iloc[1]) / 2
        data['Gas'].iloc[2] = (data['net'].iloc[0] + data['net'].iloc[1] + data['net'].iloc[2]) / 3
        data['Gas'].iloc[3] = (data['net'].iloc[0] + data['net'].iloc[1] + data['net'].iloc[2] + data['net'].iloc[3]) / 4

        data['GasNew'] = data['Gas'] * 2

        data['TopManifold'] = data['Line1'].rolling(window=3).mean()
        data['TopManifold'].iloc[0] = data['Line1'].iloc[0]
        data['TopManifold'].iloc[1] = (data['Line1'].iloc[0] + data['Line1'].iloc[1]) / 2
        data['TopManifold'].iloc[2] = (data['Line1'].iloc[0] + data['Line1'].iloc[1] + data['Line1'].iloc[2]) / 3
        data['TopManifold'].iloc[3] = (data['Line1'].iloc[0] + data['Line1'].iloc[1] + data['Line1'].iloc[2] + data['Line1'].iloc[3]) / 4
        data['TopManifold'] = data['TopManifold'] * 0.2

        data['BottomManifold'] = data['TopManifold'] * -1

    else:
        
        data['Line1'] = data['netabs'].rolling(window=3).mean()
        data['Line1'].iloc[0] = data['netabs'].iloc[0]
        data['Line1'].iloc[1] = (data['netabs'].iloc[0] + data['netabs'].iloc[1]) / 2

        data['Line2'] = data['Line1'] * -1

        data['Gas'] = data['net'].rolling(window=3).mean()
        data['Gas'].iloc[0] = 0
        data['Gas'].iloc[1] = (data['net'].iloc[0] + data['net'].iloc[1]) / 2

        data['GasNew'] = data['Gas'] * 2

        data['TopManifold'] = data['Line1'].rolling(window=3).mean()
        data['TopManifold'].iloc[0] = data['Line1'].iloc[0]
        data['TopManifold'].iloc[1] = (data['Line1'].iloc[0] + data['Line1'].iloc[1]) / 2
        data['TopManifold'] = data['TopManifold'] * 0.5

        data['BottomManifold'] = data['TopManifold'] * -1


    data['Avg_Close'] = data['Close'].rolling(window=3).mean()
    data['Avg_Open'] = data['Open'].rolling(window=3).mean()

    data['condition1'] = data['Avg_Close'] > data['Avg_Open']
    data['condition2'] = data['Avg_Close'] < data['Avg_Open']

    data['buy_indicator'] = data['condition1'].apply(lambda x: 1 if x else 0)
    data['sell_indicator'] = data['condition2'].apply(lambda x: 1 if x else 0)

    data.drop('condition1', axis=1, inplace=True)
    data.drop('condition2', axis=1, inplace=True)
    data.drop('Adj Close', axis=1, inplace=True)
    data.drop('Volume', axis=1, inplace=True)
    # for index, row in data.iterrows():
    return data


def convert_data_format(data):
    output = []
    for _, row in data.iterrows():
        output.append({
            'date': row['index'],
            'open': row['Open'],
            'high': row['High'],
            'low': row['Low'],
            'close': row['Close'],
            'net': row['net'],
            'TopManifold': row['TopManifold'], 
            'BottomManifold': row['BottomManifold'],
            'Gas': row['Gas'],
            'GasNew': row['GasNew'],
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
    current_day_ohlc = get_current_day_ohlc(stock)
    print("current day: ", current_day_ohlc)
    data = data.append(current_day_ohlc)
    data = data.reset_index()
    data = process_stock_data(data, "day")
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
    current_day_ohlc = get_current_day_ohlc(stock)
    print("current day: ", current_day_ohlc)

    data = data.append(current_day_ohlc)

    data = data.reset_index()
    data = process_stock_data(data, "week")
    print(data)
    data.reset_index(inplace=True)
    data['Date'] = data['Date'].dt.strftime('%Y-%m-%d')
    formatted_data = convert_data_format(data)
    return jsonify(formatted_data)


if __name__ == '__main__':
    app.run(debug=True)
