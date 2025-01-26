import React, { useEffect, useState } from 'react';
import Highcharts from 'highcharts/highstock';
import HighchartsReact from 'highcharts-react-official';
import './App.css';

function App() {
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
    title: { text: 'AAPL Stock Price' },
    yAxis: [
      { labels: { align: 'left' }, height: '80%' },
      { labels: { align: 'left' }, top: '80%', height: '20%', offset: 0 },
    ],
    series: [
      { type: 'candlestick', name: 'AAPL Stock Price', data: chartData },
      { type: 'column', name: 'Volume', data: volumeData, yAxis: 1 },
    ],
  };

  const entry_click = () => {
    console.log('entry click');
  };

  return (
    <div className="app-container">
      {/* Navigation Bar */}
      <nav className="navbar">
        <div className="logo">Logo</div>
        <div className="nav-links">
          <a href="#" className="nav-link">Home</a>
          <a href="#" className="nav-link">About</a>
          <a href="#" className="nav-link">Contact</a>
        </div>
      </nav>

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
          <h1 className="example-title">Yolo</h1>
          <button onClick={entry_click} className="custom-button">
            Click me
          </button>
        </div>
      </div>
    </div>
  );
}

export default App;