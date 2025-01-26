import React, { useEffect, useState, useRef } from 'react';
import Highcharts from 'highcharts/highstock';
import HighchartsReact from 'highcharts-react-official';
import './Home.css';

function Home() {
  // Simulation Functionality
  const simulate = () => {
    fetch('/run_sim', {
      method: 'POST', // Use POST to send data
      headers: {
        'Content-Type': 'application/json', // Tell the server you're sending JSON
      },
      body: JSON.stringify({ timeframe: `${new Date(minRange).toLocaleDateString()}-${new Date(maxRange).toLocaleDateString()}` }) // Send the condition as JSON
    })
  }

  // Exit Factor Functionality
  const exitFactorRef = useRef();
  const handleExitAddition = () => {
    const factor = exitFactorRef.current.value;
    fetch('/add_exit_f', {
      method: 'POST', // Use POST to send data
      headers: {
        'Content-Type': 'application/json', // Tell the server you're sending JSON
      },
      body: JSON.stringify({ condition: factor }) // Send the condition as JSON
    })
    exitFactorRef.current.value = ""; // Clear the input field after submission
  }

  // Entry Factor Functionality
  const entryFactorRef = useRef();
  const handleEntryAddition = () => {
    const factor = entryFactorRef.current.value;
    fetch('/add_entry_f', {
      method: 'POST', // Use POST to send data
      headers: {
        'Content-Type': 'application/json', // Tell the server you're sending JSON
      },
      body: JSON.stringify({ condition: factor }) // Send the condition as JSON
    })

    entryFactorRef.current.value = ""; // Clear the input field after submission
  }

  // Simulation Winow Functionality
  const [minRange, setMinRange] = useState(null);
  const [maxRange, setMaxRange] = useState(null);

  // Symbol Selector Functionality
  const [symbol, setSymbol] = useState('AAPL');
  const symbolRef = useRef();
  const handleSymbol = () => {
    const value = symbolRef.current.value;

    fetch('/pipe', {
      method: 'POST', // Use POST to send data
      headers: {
        'Content-Type': 'application/json', // Tell the server you're sending JSON
      },
      body: JSON.stringify({ symbol: value }), // Send the symbol as JSON
    })
      .then((response) => response.json())
      .then((data) => {
        const chartData = [];
        const volumeData = [];
        const responseData = data.res;
  
        // Process response data to update the chart
        responseData.forEach((item) => {
          chartData.push([item[0], item[1], item[2], item[3], item[4]]);
          volumeData.push([item[0], item[5]]);
        });
  
        setChartData(chartData); // Update chart data state
        setVolumeData(volumeData); // Update volume data state
        setSymbol(value); // Update symbol in state
      })
      .catch((error) => console.error('Error:', error));

    symbolRef.current.value = ""; // Clear the input field after submission
  }

  const [chartData, setChartData] = useState([]);
  const [volumeData, setVolumeData] = useState([]);
  const [message, setMessage] = useState('');

  useEffect(() => {
    fetch('/api/data')
      .then(response => response.json())
      .then(data => setMessage(data.message));
  }, []);

  useEffect(() => {
    fetch('/pipe')
      .then(response => response.json())
      .then((data) => {
        const chartData = [];
        const volumeData = [];
        const responseData = data.res;

        responseData.forEach(item => {
          chartData.push([item[0], item[1], item[2], item[3], item[4]]);
          volumeData.push([item[0], item[5]]);
        });

        setChartData(chartData);
      });
  }, []);

  const chartOptions = {
    rangeSelector: { selected: 1 },
    title: { text: `${symbol} Stock Price` },
    yAxis: [
      { labels: { align: 'left' }, height: '80%' },
      { labels: { align: 'left' }, top: '80%', height: '20%', offset: 0 },
    ],
    xAxis: {
      events: {
        afterSetExtremes: (event) => {
          setMinRange(event.min); // Store the new min value
          setMaxRange(event.max); // Store the new max value
        },
      },
    },
    series: [
      { type: 'candlestick', name: `${symbol} Stock Price`, data: chartData },
      { type: 'column', name: 'Volume', data: volumeData, yAxis: 1 },
    ],
  };

  const entry_click = () => {
    console.log('entry click');
  };

  return (
    <div className="app-container">

      {/* Main Content */}
      <div className="main-content">
        <div className="chart-container">
          <HighchartsReact
            highcharts={Highcharts}
            constructorType={'stockChart'}
            options={chartOptions}
          />
        </div>

        <div className="example-section">
          
          {/* Symbol HTML */}
          <input type="text" ref={symbolRef}></input>
          <button onClick={handleSymbol}>Submit</button>

          {/* Window Range HTML */}
          <div>
            <p>Min Range: {minRange ? new Date(minRange).toLocaleDateString() : 'N/A'}</p>
            <p>Max Range: {maxRange ? new Date(maxRange).toLocaleDateString() : 'N/A'}</p>
          </div>

          {/* Simulate HTML */}
          <button onClick={simulate}>Simulate</button>

          {/* Entry Factor HTML */}
          <h3>ENTRY</h3>
          <input type="text" ref={entryFactorRef}></input>
          <button onClick={handleEntryAddition}>Add</button>

          {/* Exit Factor HTML */}
          <h3>EXIT</h3>
          <input type="text" ref={exitFactorRef}></input>
          <button onClick={handleExitAddition}>Add</button>

        </div>
      </div>
    </div>
  );
}

export default Home;