import yfinance as yf
import numpy as np
import pandas as pd
import os
import json
from datetime import datetime, timedelta

# ---------- Getting Directory String ----------
root_dir = os.getcwd()
backend_dir = os.path.join(root_dir, "backend\\venv\\Datasets")

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
    while not (start_date.strftime('%m/%d/%Y') in data['Date'].values):
        start_date += timedelta(days=1)
    while not (end_date.strftime('%m/%d/%Y') in data['Date'].values):
        end_date -= timedelta(days=1)

    # Convert back to desired string format with no leading zeros
    start_date = start_date.strftime('%m/%d/%Y').lstrip('0').replace('/0', '/')
    end_date = end_date.strftime('%m/%d/%Y').lstrip('0').replace('/0', '/')
    
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

def add_all_factors(symbol):
    add_rsi(symbol)
    add_volume_ratio(symbol)
    add_volatility_ratio(symbol)
    add_momentum_ratio(symbol)
    add_percent_macd(symbol)
    add_atr(symbol)
    add_obv(symbol)
    add_stochastic(symbol)
    add_williams_r(symbol)
    add_ichimoku(symbol)
    add_cmo(symbol)


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
    data.loc[:, 'Momentum Ratio'] = (data['Close'] - data['Close'].shift(10))/ data['Close'].shift(10)

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
    data['ATR'] = data['TR'].rolling(window=14).mean()/ data['Close']

    # Dropping NaN Rows
    data.dropna(inplace=True)
    data.reset_index(drop=True, inplace=True)

    # Save Data to a CSV File
    filename = os.path.join(backend_dir, f'{symbol}_data.csv')
    data.to_csv(filename, index=False)
    print(f'Added Average True Range')

def add_obv(symbol):
    data = pd.read_csv(os.path.join(backend_dir, f'{symbol}_data.csv'))

    # On-Balance Volume Normalized by Total Volume
    data['OBV'] = 0
    for i in range(1, len(data)):
        if data.loc[i, 'Close'] > data.loc[i - 1, 'Close']:
            data.loc[i, 'OBV'] = data.loc[i - 1, 'OBV'] + data.loc[i, 'Volume']
        elif data.loc[i, 'Close'] < data.loc[i - 1, 'Close']:
            data.loc[i, 'OBV'] = data.loc[i - 1, 'OBV'] - data.loc[i, 'Volume']
        else:
            data.loc[i, 'OBV'] = data.loc[i - 1, 'OBV']
    data['OBV Ratio'] = data['OBV'] / data['Volume'].sum()

    data.dropna(inplace=True)
    data.reset_index(drop=True, inplace=True)

    filename = os.path.join(backend_dir, f'{symbol}_data.csv')
    data.to_csv(filename, index=False)
    print(f'Added OBV (as Ratio)')

def add_Sentiment(symbol, time):
    import os
    import google.generativeai as genai
    import pandas as pd

    # Configure API key for Gemini
    genai.configure(api_key=os.environ["AIzaSyBePnJjq6UcQIwgWoAAFtp6tbOK_G8tzDY"])

    # Define the configuration for the model
    generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
    }

    # Initialize the generative model
    model = genai.GenerativeModel(
        model_name="learnlm-1.5-pro-experimental",
        generation_config=generation_config,
        system_instruction=(
            f"Analyze the sentiment for the stock symbol {symbol} over the time period {time}. "
            "Output a list of sentiment scores (0 to 100) for each trading day in the given period. "
            "Scores closer to 0 indicate negative sentiment, and closer to 100 indicate positive sentiment."
        ),
    )

    # Start a chat session and generate the sentiment response
    chat_session = model.start_chat()
    response = chat_session.send_message("Provide the sentiment scores as a list.")

    # Parse the response to extract sentiment values (assumes response text is JSON formatted)
    sentiment_scores = eval(response.text)  # Use `json.loads` if response text is in JSON format

    # Load the existing dataset
    filename = os.path.join(backend_dir, f'{symbol}_data.csv')
    data = pd.read_csv(filename)

    # Add the sentiment scores as a new column
    if len(sentiment_scores) == len(data):
        data['Sentiment'] = sentiment_scores
    else:
        raise ValueError("Mismatch between sentiment scores and dataset length.")

    # Save the updated dataset to the same CSV file
    data.to_csv(filename, index=False)
    print(f'Added Sentiment scores to {symbol} data.')

    return data



def add_stochastic(symbol):
    data = pd.read_csv(os.path.join(backend_dir, f'{symbol}_data.csv'))

    data['14 High'] = data['High'].rolling(window=14).max()
    data['14 Low'] = data['Low'].rolling(window=14).min()
    data['Stochastic'] = 100 * (data['Close'] - data['14 Low']) / (data['14 High'] - data['14 Low'])

    data.drop(columns=['14 High', '14 Low'], inplace=True)
    data.dropna(inplace=True)
    data.reset_index(drop=True, inplace=True)

    filename = os.path.join(backend_dir, f'{symbol}_data.csv')
    data.to_csv(filename, index=False)
    print(f'Added Stochastic Oscillator')


def add_williams_r(symbol):
    data = pd.read_csv(os.path.join(backend_dir, f'{symbol}_data.csv'))

    data['14 High'] = data['High'].rolling(window=14).max()
    data['14 Low'] = data['Low'].rolling(window=14).min()
    data['Williams %R'] = -100 * (data['14 High'] - data['Close']) / (data['14 High'] - data['14 Low'])

    data.drop(columns=['14 High', '14 Low'], inplace=True)
    data.dropna(inplace=True)
    data.reset_index(drop=True, inplace=True)

    filename = os.path.join(backend_dir, f'{symbol}_data.csv')
    data.to_csv(filename, index=False)
    print(f'Added Williams %R')



def add_ichimoku(symbol):
    data = pd.read_csv(os.path.join(backend_dir, f'{symbol}_data.csv'))

    data['Tenkan-Sen'] = (data['High'].rolling(window=9).max() + data['Low'].rolling(window=9).min()) / 2
    data['Kijun-Sen'] = (data['High'].rolling(window=26).max() + data['Low'].rolling(window=26).min()) / 2
    data['Senkou Span A'] = ((data['Tenkan-Sen'] + data['Kijun-Sen']) / 2).shift(26)
    data['Senkou Span B'] = ((data['High'].rolling(window=52).max() + data['Low'].rolling(window=52).min()) / 2).shift(26)

    data.dropna(inplace=True)
    data.reset_index(drop=True, inplace=True)

    filename = os.path.join(backend_dir, f'{symbol}_data.csv')
    data.to_csv(filename, index=False)
    print(f'Added Ichimoku Cloud')


def add_cmo(symbol):
    data = pd.read_csv(os.path.join(backend_dir, f'{symbol}_data.csv'))

    data['Up'] = np.where(data['Close'] > data['Close'].shift(1), data['Close'] - data['Close'].shift(1), 0)
    data['Down'] = np.where(data['Close'] < data['Close'].shift(1), data['Close'].shift(1) - data['Close'], 0)
    sum_up = data['Up'].rolling(window=14).sum()
    sum_down = data['Down'].rolling(window=14).sum()

    data['CMO'] = 100 * (sum_up - sum_down) / (sum_up + sum_down)

    data.drop(columns=['Up', 'Down'], inplace=True)
    data.dropna(inplace=True)
    data.reset_index(drop=True, inplace=True)

    filename = os.path.join(backend_dir, f'{symbol}_data.csv')
    data.to_csv(filename, index=False)
    print(f'Added Chande Momentum Oscillator')