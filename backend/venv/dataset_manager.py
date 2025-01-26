import yfinance as yf
import numpy as np
import pandas as pd
import os
import json

# ---------- Getting Directory String ----------
root_dir = os.getcwd()
backend_dir = os.path.join(root_dir, "backend\\venv\\Datasets")

# ---------- Fetching All Symbol Data ----------
def fetch_symbol(symbol):
    # Fetching Data From YF
    data = yf.download(symbol, period="max")

    # Setting Up The Date Column & Cleaning Structure
    data.reset_index(inplace=True)
    data['Date'] = data['Date'].dt.strftime('%Y-%m-%d')  # Convert Date to strings
    data.columns = data.columns.get_level_values(0)  # Removes multi-header structure

    # Adding Return Feature
    data['Return'] = data['Close'].pct_change()
    data.dropna(inplace=True)

    # Getting The First & Last Dates Available
    first_date = data.iloc[0]['Date']
    last_date = data.iloc[len(data) - 1]['Date']

    # Save Data to a CSV File
    filename = os.path.join(backend_dir, f'{symbol}_data.csv')
    print(filename)
    data.to_csv(filename, index=False)

    # Returns The Timeframe Available
    return data

# ---------- Live Dataset Functionality ----------
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
    
    # Cropping Dataset
    start_i = data.loc[data['Date'] == start_date].index[0]
    end_i = data.loc[data['Date'] == end_date].index[0]
    data = data.iloc[start_i:end_i+1]

    # Save Data to a CSV File
    filename = os.path.join(backend_dir, f'{symbol}_data.csv')
    data.to_csv(filename, index=False)
    print(f'Cropped {symbol}: {start_date}:{end_date}')

    return data

def add_balances(symbol, balances):
    data = pd.read_csv(os.path.join(backend_dir, f'{symbol}_data.csv'))
    data['Balance'] = balances

    # Save Data to a CSV File
    filename = os.path.join(backend_dir, f'{symbol}_data.csv')
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
