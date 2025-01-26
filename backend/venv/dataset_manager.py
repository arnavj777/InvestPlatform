import yfinance as yf
import numpy as np
import pandas as pd
import os
import json
from datetime import datetime, timedelta

# ---------- Getting Directory String ----------
root_dir = os.getcwd()
backend_dir = os.path.join(root_dir, "backend\\venv\\Datasets")
sims_dir = os.path.join(root_dir, "backend\\venv\\Simulations")

# ---------- Fetching All Symbol Data ----------
def fetch_symbol(symbol):
    # Fetching Data From YF
    data = yf.download(symbol, period="max")

    # Setting Up The Date Column & Cleaning Structure
    data.reset_index(inplace=True)
    data['Date'] = data['Date'].dt.strftime('%m/%d/%Y').str.lstrip('0').str.replace('/0', '/')
    data.columns = data.columns.get_level_values(0)  # Removes multi-header structure

    # Adding Return Feature
    data['Return'] = data['Close'].pct_change()
    data.dropna(inplace=True)
    
    # Save Data to a CSV File
    filename = os.path.join(backend_dir, f'{symbol}_data.csv')
    print(filename)
    data.to_csv(filename, index=False)

    add_all_factors(symbol)

    # Returns The Timeframe Available
    return data

# ---------- Live Dataset Functionality ----------
def get_symbol(symbol):
    data = pd.read_csv(os.path.join(backend_dir, f'{symbol}_data.csv'))
    return data

def csv_to_json(symbol):
    data = pd.read_csv(os.path.join(backend_dir, f'{symbol}_data.csv'))
    json_dta = []
    data['Date'] = pd.to_datetime(data['Date']).astype(int) // 10**6

    json_dta = []
    for i in range(len(data)):
        json_dta.append([
            data.iloc[i]['Date'],
            data.iloc[i]['Open'],
            data.iloc[i]['High'],
            data.iloc[i]['Low'],
            data.iloc[i]['Close'],
            data.iloc[i]['Volume']
        ])
    return json.dumps(json_dta)

def fetch_updated_data(symbol):
    data = pd.read_csv(os.path.join(backend_dir, f'{symbol}_data.csv'))
    return data

def crop_data(symbol, start_date, end_date):
    data = pd.read_csv(os.path.join(backend_dir, f'{symbol}_data.csv'))

    # Convert start_date and end_date to datetime objects
    start_date = datetime.strptime(start_date, '%m/%d/%Y')
    end_date = datetime.strptime(end_date, '%m/%d/%Y')

    # Adjust start_date and end_date to match available dates in the dataset
    while not (start_date.strftime('%m/%d/%Y').lstrip('0').replace('/0', '/') in data['Date'].values):
        start_date += timedelta(days=1)
    while not (end_date.strftime('%m/%d/%Y').lstrip('0').replace('/0', '/') in data['Date'].values):
        end_date -= timedelta(days=1)
        print(end_date)

    # Convert back to desired string format with no leading zeros
    start_date = start_date.strftime('%m/%d/%Y').lstrip('0').replace('/0', '/')
    end_date = end_date.strftime('%m/%d/%Y').lstrip('0').replace('/0', '/')

    # Cropping Dataset
    start_i = data.loc[data['Date'] == start_date].index[0]
    end_i = data.loc[data['Date'] == end_date].index[0]
    data = data.iloc[start_i:end_i+1]

    # Save Data to a CSV File
    filename = os.path.join(sims_dir, f'{symbol}_sim.csv')
    data.to_csv(filename, index=False)
    print(f'Cropped {symbol}: {start_date}:{end_date}')

    return data

def add_balances(symbol, balances):
    data = pd.read_csv(os.path.join(sims_dir, f'{symbol}_sim.csv'))
    data['Balance'] = balances

    # Save Data to a CSV File
    filename = os.path.join(sims_dir, f'{symbol}_sim.csv')
    data.to_csv(filename, index=False)
    print(f'Added Balance to {symbol}')

    return data


# ---------- Factor Methods ----------
def add_factor(symbol, factor):
    if factor == 'RSI':
        add_rsi(symbol)
    elif factor == 'Volume Ratio':
        add_volume_ratio(symbol)
    elif factor == 'Volatility Ratio':
        add_volatility_ratio(symbol)
    elif factor == 'Momentum Ratio':
        add_momentum_ratio(symbol)
    elif factor == 'Percent MACD':
        add_percent_macd(symbol)

def add_all_factors(symbol):
    add_rsi(symbol)
    add_volume_ratio(symbol)
    add_volatility_ratio(symbol)
    add_momentum_ratio(symbol)
    add_percent_macd(symbol)
    add_atr(symbol)
    add_obv(symbol)


# RSI
def add_rsi(symbol):
    data = pd.read_csv(os.path.join(backend_dir, f'{symbol}_data.csv'))

    # Calculating RSI & Adding It
    gain = data['Return'].where(data['Return'] > 0, 0)
    loss = -data['Return'].where(data['Return'] < 0, 0)
    avg_gain = gain.rolling(window=14).mean()
    avg_loss = loss.rolling(window=14).mean()
    rs = avg_gain / avg_loss
    data.loc[:, 'RSI'] = 100 - (100 / (1 + rs))

    # Dropping NaN Rows
    data.dropna(inplace=True)
    data.reset_index(drop=True, inplace=True)

    # Save Data to a CSV File
    filename = os.path.join(backend_dir, f'{symbol}_data.csv')
    data.to_csv(filename, index=False)
    print(f'Added RSI')

# Volume Ratio
def add_volume_ratio(symbol):
    data = pd.read_csv(os.path.join(backend_dir, f'{symbol}_data.csv'))

    # Volume Ratio: Current volume divided by the 20-day average volume
    data.loc[:, 'Volume Ratio'] = data['Volume'] / data['Volume'].rolling(window=20).mean()

    # Dropping NaN Rows
    data.dropna(inplace=True)
    data.reset_index(drop=True, inplace=True)

    # Save Data to a CSV File
    filename = os.path.join(backend_dir, f'{symbol}_data.csv')
    data.to_csv(filename, index=False)
    print(f'Added Volume Ratio')

# Volatility Ratio
def add_volatility_ratio(symbol):
    data = pd.read_csv(os.path.join(backend_dir, f'{symbol}_data.csv'))

    # Volatility Ratio: Annualized standard deviation of daily returns
    data.loc[:, 'Volatility Ratio'] = data['Return'].rolling(window=20).std() * np.sqrt(252)

    # Dropping NaN Rows
    data.dropna(inplace=True)
    data.reset_index(drop=True, inplace=True)

    # Save Data to a CSV File
    filename = os.path.join(backend_dir, f'{symbol}_data.csv')
    data.to_csv(filename, index=False)
    print(f'Added Volatility Ratio')

# Momentum Ratio
def add_momentum_ratio(symbol):
    data = pd.read_csv(os.path.join(backend_dir, f'{symbol}_data.csv'))

    # Momentum: Difference between current close and close 10 days ago
    data.loc[:, 'Momentum Ratio'] = data['Close'] - data['Close'].shift(10)

    # Dropping NaN Rows
    data.dropna(inplace=True)
    data.reset_index(drop=True, inplace=True)

    # Save Data to a CSV File
    filename = os.path.join(backend_dir, f'{symbol}_data.csv')
    data.to_csv(filename, index=False)
    print(f'Added Momentum Ratio')

# % MACD
def add_percent_macd(symbol):
    data = pd.read_csv(os.path.join(backend_dir, f'{symbol}_data.csv'))

    # MACD: Percentage difference between 12-day EMA and 26-day EMA
    ema_12 = data['Close'].ewm(span=12, adjust=False).mean()
    ema_26 = data['Close'].ewm(span=26, adjust=False).mean()
    data.loc[:, '% MACD'] = 100 * (ema_12 - ema_26) / ema_12

    # Dropping NaN Rows
    data.dropna(inplace=True)
    data.reset_index(drop=True, inplace=True)

    # Save Data to a CSV File
    filename = os.path.join(backend_dir, f'{symbol}_data.csv')
    data.to_csv(filename, index=False)
    print(f'Added Percentage MACD Ratio')

def add_atr(symbol):
    data = pd.read_csv(os.path.join(backend_dir, f'{symbol}_data.csv'))

    # Calculate True Range
    data['TR'] = data[['High', 'Low', 'Close']].apply(
        lambda x: max(x['High'] - x['Low'], 
                      abs(x['High'] - x['Close']), 
                      abs(x['Low'] - x['Close'])), axis=1)

    # Calculate Average True Range (ATR)
    data['ATR'] = data['TR'].rolling(window=14).mean()

    # Dropping NaN Rows
    data.dropna(inplace=True)
    data.reset_index(drop=True, inplace=True)

    # Save Data to a CSV File
    filename = os.path.join(backend_dir, f'{symbol}_data.csv')
    data.to_csv(filename, index=False)
    print(f'Added Average True Range')

def add_obv(symbol):
    data = pd.read_csv(os.path.join(backend_dir, f'{symbol}_data.csv'))

    # Calculate On-Balance Volume
    data['OBV'] = 0
    for i in range(1, len(data)):
        if data.loc[i, 'Close'] > data.loc[i - 1, 'Close']:
            data.loc[i, 'OBV'] = data.loc[i - 1, 'OBV'] + data.loc[i, 'Volume']
        elif data.loc[i, 'Close'] < data.loc[i - 1, 'Close']:
            data.loc[i, 'OBV'] = data.loc[i - 1, 'OBV'] - data.loc[i, 'Volume']
        else:
            data.loc[i, 'OBV'] = data.loc[i - 1, 'OBV']

    # Save Data to a CSV File
    filename = os.path.join(backend_dir, f'{symbol}_data.csv')
    data.to_csv(filename, index=False)
    print(f'Added On-Balance Volume')
