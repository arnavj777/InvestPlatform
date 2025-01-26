import React, { useEffect, useState, useRef } from 'react';
import Highcharts from 'highcharts/highstock';
import HighchartsReact from 'highcharts-react-official';
import './Home.css';

function Home() {
  const [entryIndicators, setEntryIndicators] = useState([]);
  const [exitIndicators, setExitIndicators] = useState([]);
  const [minRange, setMinRange] = useState(null);
  const [maxRange, setMaxRange] = useState(null);
  const [chartData, setChartData] = useState([]);
  const [volumeData, setVolumeData] = useState([]);
  const [symbol, setSymbol] = useState('AAPL');

  const [entryIndicator, setEntryIndicator] = useState('');
  const [exitIndicator, setExitIndicator] = useState('');
  const [entryOperator, setEntryOperator] = useState('>');
  const [exitOperator, setExitOperator] = useState('>');
  const [entryValue, setEntryValue] = useState('');
  const [exitValue, setExitValue] = useState('');

  const technicalIndicators = [
    'Moving Average',
    'RSI',
    'Volatility Ratio',
    'Momentum Ratio',
    '% MACD',
    'ATR',
    'OBV',
    'Volume Ratio',
    'Stochastic',
    'Williams %R',
    'CMO',
    'Sentiment'
  ];

  const operators = ['>', '<', '>=', '<=', '='];

  const simulate = () => {
    if (minRange && maxRange) {
      fetch('/run_sim', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          timeframe: `${new Date(minRange).toLocaleDateString()}-${new Date(maxRange).toLocaleDateString()}`,
        }),
      });
    } else {
      console.error('Simulation requires valid minRange and maxRange');
    }
  };

  const symbolRef = useRef();

  const handleSymbol = () => {
    const value = symbolRef.current.value;
    fetch('/pipe', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ symbol: value }),
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.res && Array.isArray(data.res)) {
          const chartData = [];
          const volumeData = [];
          data.res.forEach((item) => {
            chartData.push([item[0], item[1], item[2], item[3], item[4]]);
            volumeData.push([item[0], item[5]]);
          });
          setChartData(chartData);
          setVolumeData(volumeData);
          setSymbol(value);
        } else {
          console.error('Unexpected API response:', data);
        }
      })
      .catch((error) => console.error('Error:', error));
    symbolRef.current.value = '';
  };

  const handleEntryAddition = () => {
    if (entryIndicator && entryOperator && entryValue) {
      const entryCondition = `${entryIndicator}:${entryOperator}${entryValue}`;
      setEntryIndicators((prev) => [...prev, entryCondition]);
      fetch('/add_entry_f', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ condition: entryCondition }),
      });
      setEntryIndicator('');
      setEntryOperator('>');
      setEntryValue('');
    }
  };

  const handleExitAddition = () => {
    if (exitIndicator && exitOperator && exitValue) {
      const exitCondition = `${exitIndicator}:${exitOperator}${exitValue}`;
      setExitIndicators((prev) => [...prev, exitCondition]);
      fetch('/add_exit_f', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ condition: exitCondition }),
      });
      setExitIndicator('');
      setExitOperator('>');
      setExitValue('');
    }
  };

  const handleEntryRemoval = (index) => {
    const conditionToRemove = entryIndicators[index]; // Get the condition to remove
    setEntryIndicators((prev) => prev.filter((_, i) => i !== index)); // Update state to remove it
  
    // Send request to backend to remove the entry condition
    fetch('/remove_entry_f', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ condition: conditionToRemove }),
    }).catch((error) => console.error('Error removing entry condition:', error));
  };
  
  const handleExitRemoval = (index) => {
    const conditionToRemove = exitIndicators[index]; // Get the condition to remove
    setExitIndicators((prev) => prev.filter((_, i) => i !== index)); // Update state to remove it
  
    // Send request to backend to remove the exit condition
    fetch('/remove_exit_f', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ condition: conditionToRemove }),
    }).catch((error) => console.error('Error removing exit condition:', error));
  };  

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
          setMinRange(event.min);
          setMaxRange(event.max);
        },
      },
    },
    series: [
      { type: 'candlestick', name: `${symbol} Stock Price`, data: chartData },
      { type: 'column', name: 'Volume', data: volumeData, yAxis: 1 },
    ],
  };

  return (
    <div className="app-container">
      <div className="main-content">
        <div className="chart-container">
          <HighchartsReact highcharts={Highcharts} constructorType={'stockChart'} options={chartOptions} />
        </div>

        <div className="example-section">
          {/* Search Bar */}
          <input type="text" ref={symbolRef} placeholder="Enter Symbol" />
          <button onClick={handleSymbol}>Submit</button>

          <div>
            <p>Min Range: {minRange ? new Date(minRange).toLocaleDateString() : 'N/A'}</p>
            <p>Max Range: {maxRange ? new Date(maxRange).toLocaleDateString() : 'N/A'}</p>
          </div>

          <button onClick={simulate}>Simulate</button>

          <h3>ENTRY</h3>
          <select value={entryIndicator} onChange={(e) => setEntryIndicator(e.target.value)}>
            <option value="" disabled>
              Select Technical Indicator
            </option>
            {technicalIndicators.map((indicator, index) => (
              <option key={index} value={indicator}>
                {indicator}
              </option>
            ))}
          </select>

          <select value={entryOperator} onChange={(e) => setEntryOperator(e.target.value)}>
            {operators.map((operator, index) => (
              <option key={index} value={operator}>
                {operator}
              </option>
            ))}
          </select>

          <input
            type="number"
            value={entryValue}
            onChange={(e) => setEntryValue(e.target.value)}
            placeholder="Enter Value"
          />
          <button onClick={handleEntryAddition}>Add Entry</button>

          <h3>EXIT</h3>
          <select value={exitIndicator} onChange={(e) => setExitIndicator(e.target.value)}>
            <option value="" disabled>
              Select Technical Indicator
            </option>
            {technicalIndicators.map((indicator, index) => (
              <option key={index} value={indicator}>
                {indicator}
              </option>
            ))}
          </select>

          <select value={exitOperator} onChange={(e) => setExitOperator(e.target.value)}>
            {operators.map((operator, index) => (
              <option key={index} value={operator}>
                {operator}
              </option>
            ))}
          </select>

          <input
            type="number"
            value={exitValue}
            onChange={(e) => setExitValue(e.target.value)}
            placeholder="Enter Value"
          />
          <button onClick={handleExitAddition}>Add Exit</button>

          <div className="indicators-container">
            <div className="indicators-column">
              <h3>Current Entry Indicators</h3>
              <ul>
                {entryIndicators.map((indicator, index) => (
                  <li key={index}>
                    {indicator}
                    <button
                      onClick={() => handleEntryRemoval(index)} // Call handleEntryRemoval
                      className="remove-btn"
                    >
                      Remove
                    </button>
                  </li>
                ))}
              </ul>
            </div>
            <div className="indicators-column">
              <h3>Current Exit Indicators</h3>
              <ul>
                {exitIndicators.map((indicator, index) => (
                  <li key={index}>
                    {indicator}
                    <button
                      onClick={() => handleExitRemoval(index)} // Call handleExitRemoval
                      className="remove-btn"
                    >
                      Remove
                    </button>
                  </li>
                ))}
              </ul>
            </div>
          </div>

        </div>
      </div>
    </div>
  );
}

export default Home;
