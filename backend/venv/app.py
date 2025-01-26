try:
    import json
    from flask import Flask, render_template,make_response,request
    import requests
    import json
    print("ALl modules Loaded ")
except Exception as e:
    print("Error : {} ".format(e))
from dataset_manager import *
from simulation import simulation

app = Flask(__name__)
sim = simulation('AAPL')


@app.route('/')
def hello_world():
    return render_template("index.html")


@app.route('/pipe', methods=["GET", "POST"])
def pipe():
    # Get the JSON data sent from React
    data = request.get_json()
    symbol = data.get('symbol', 'AAPL')  # Default to 'AAPL' if symbol is not provided

    # Getting Symbol Data
    fetch_symbol(symbol)
    # Creating Simulation Instance
    global sim
    sim = simulation(symbol)

    # Perform some action with the symbol (e.g., fetch stock data)
    print(f"Received symbol: {symbol}")

    # symbol = 'AAPL'
    json_data = csv_to_json(symbol)
    return {"res":json.loads(json_data)}

@app.route('/add_entry_f', methods=["GET", "POST"])
def add_entry_f():
    # Get the JSON data sent from React
    data = request.get_json()
    condition = (data.get('condition', 'RSI:<=30')).split(':')  # Default to 'AAPL' if symbol is not provided
    sim.add_entry_condition(condition[0], condition[1])
    return {}

@app.route('/add_exit_f', methods=["GET", "POST"])
def add_exit_f():
    # Get the JSON data sent from React
    data = request.get_json()
    condition = (data.get('condition', 'RSI:>=50')).split(':')  # Default to 'AAPL' if symbol is not provided
    sim.add_exit_condition(condition[0], condition[1])
    return {}

@app.route('/run_sim', methods=["GET", "POST"])
def run_sim():
    # Get the JSON data sent from React
    data = request.get_json()
    timeframe = (data.get('timeframe', '10/31/2023-12/20/2023')).split('-')  # Default to 'AAPL' if symbol is not provided
    print(timeframe)
    sim.crop_dataset(timeframe[0],timeframe[1])
    sim.simulate()
    sim.plot_sim()
    return {}
    

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)