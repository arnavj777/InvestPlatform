import React, { useEffect, useState, useRef } from 'react';
import Highcharts from 'highcharts/highstock';
import HighchartsReact from 'highcharts-react-official';
import './Home.css';

function Home() {
  const [entryIndicators, setEntryIndicators] = useState([]);
  const [exitIndicators, setExitIndicators] = useState([]);
  const entryFactorRef = useRef();
  const exitFactorRef = useRef();
  const symbolRef = useRef();

  const [minRange, setMinRange] = useState(null);
  const [maxRange, setMaxRange] = useState(null);
  const [chartData, setChartData] = useState([]);
  const [volumeData, setVolumeData] = useState([]);
  const [symbol, setSymbol] = useState('AAPL');

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

  const handleEntryAddition = () => {
    const factor = entryFactorRef.current.value;
    if (factor) {
      setEntryIndicators((prev) => [...prev, factor]);
      fetch('/add_entry_f', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ condition: factor }),
      });
      entryFactorRef.current.value = '';
    }
  };

  const handleExitAddition = () => {
    const factor = exitFactorRef.current.value;
    if (factor) {
      setExitIndicators((prev) => [...prev, factor]);
      fetch('/add_exit_f', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ condition: factor }),
      });
      exitFactorRef.current.value = '';
    }
  };

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
          <input type="text" ref={symbolRef} placeholder="Enter Symbol" />
          <button onClick={handleSymbol}>Submit</button>

          <div>
            <p>Min Range: {minRange ? new Date(minRange).toLocaleDateString() : 'N/A'}</p>
            <p>Max Range: {maxRange ? new Date(maxRange).toLocaleDateString() : 'N/A'}</p>
          </div>

          <button onClick={simulate}>Simulate</button>

          <h3>ENTRY</h3>
          <input type="text" ref={entryFactorRef} placeholder="Add Entry Indicator" />
          <button onClick={handleEntryAddition}>Add</button>

          <h3>EXIT</h3>
          <input type="text" ref={exitFactorRef} placeholder="Add Exit Indicator" />
          <button onClick={handleExitAddition}>Add</button>

          {/* Two-column layout for indicators */}
          <div className="indicators-container">
  {/* Entry Indicators */}
  <div className="indicators-column">
    <h3>Current Entry Indicators</h3>
    <ul>
      {entryIndicators.map((indicator, index) => (
        <li key={index}>
          {indicator.replace(':', '')}
          <button
            onClick={() =>
              setEntryIndicators((prev) =>
                prev.filter((_, i) => i !== index)
              )
            }
            className="remove-btn"
          >
            Remove
          </button>
        </li>
      ))}
    </ul>
  </div>

  {/* Exit Indicators */}
  <div className="indicators-column">
    <h3>Current Exit Indicators</h3>
    <ul>
      {exitIndicators.map((indicator, index) => (
        <li key={index}>
          {indicator.replace(':', '')}
          <button
            onClick={() =>
              setExitIndicators((prev) =>
                prev.filter((_, i) => i !== index)
              )
            }
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
