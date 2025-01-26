try:
    import json
    from flask import Flask, render_template,make_response,request, jsonify
    import requests
    import json
    print("ALl modules Loaded ")
except Exception as e:
    print("Error : {} ".format(e))
from dataset_manager import *
from simulation import simulation

app = Flask(__name__)
sim = simulation('AAPL')
# ---------- Getting Directory String ----------
root_dir = os.getcwd()
backend_dir = os.path.join(root_dir, "backend\\venv\\Datasets")
sims_dir = os.path.join(root_dir, "backend\\venv\\Simulations")


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
    condition = (data.get('condition', 'RSI:<=30')).split(':')  # Default to 'AAPL' if symbol is not provide
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

@app.route('/sim_charts', methods=['GET', 'POST'])
def sim_charts():
    filenames = os.listdir(sims_dir)
    print(filenames)
    charts = []
    for i, filename in enumerate(filenames):
        data = pd.read_csv(os.path.join(sims_dir, filename))

        # Convert 'Date' and 'Balance' to lists
        dates = data['Date'].tolist()
        balances = data['Balance'].tolist()

        # Append chart configuration
        charts.append({
            "chart": {"type": "line"},
            "title": {"text": f"{filename.split('_')[0]}"},
            "xAxis": {"categories": dates},  # Use the converted list
            "yAxis": {"title": {"text": "Values"}},
            "series": [
                {"name": f"Dataset {i + 1}", "data": balances}  # Use the converted list
            ]
        })

    return jsonify(charts)
    

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)