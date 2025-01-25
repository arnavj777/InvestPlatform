import React, { useEffect, useState } from 'react';
import Highcharts from 'highcharts/highstock';
import HighchartsReact from 'highcharts-react-official';
import './App.css';

function App() {
  const [chartData, setChartData] = useState([]);
  const [volumeData, setVolumeData] = useState([]);
  const [message, setMessage] = useState('');

  // Fetch message (example data fetch)
  useEffect(() => {
    fetch('/api/data')
      .then(response => response.json())
      .then(data => setMessage(data.message));
  }, []);

  // Fetch stock data
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
        setVolumeData(volumeData);
      });
  }, []);

  // Highcharts configuration
  const chartOptions = {
    rangeSelector: { selected: 1 },
    title: { text: 'AAPL Stock Price' },
    yAxis: [
      {
        labels: { align: 'left' },
        height: '80%',
      },
      {
        labels: { align: 'left' },
        top: '80%',
        height: '20%',
        offset: 0,
      },
    ],
    series: [
      {
        type: 'candlestick',
        name: 'AAPL Stock Price',
        data: chartData,
      },
      {
        type: 'column',
        name: 'Volume',
        data: volumeData,
        yAxis: 1,
      },
    ],
  };

  const entry_click = () => {
    console.log('entry click');
  };

  return (
    <div
      style={{
        width: '100%',
        height: '100vh',
        backgroundColor: '#151B24',
        display: 'flex',
        flexDirection: 'column',
      }}
    >
      {/* Navigation Bar */}
      <nav
        style={{
          width: '100%',
          height: '60px',
          backgroundColor: '#1A1E29',
          display: 'flex',
          alignItems: 'center',
          padding: '0px',
          boxShadow: '0px 2px 4px rgba(0, 0, 0, 0.25)',
        }}
      >
        <div
          style={{
            color: '#FFFFFF',
            fontSize: '20px',
            fontWeight: 'bold',
            cursor: 'pointer',
          }}
        >
          Logo
        </div>
        <div style={{ marginLeft: 'auto', display: 'flex', gap: '20px' }}>
          <a
            href="#"
            style={{
              color: '#FFFFFF',
              textDecoration: 'none',
              fontSize: '16px',
              fontWeight: '500',
              cursor: 'pointer',
            }}
          >
            Home
          </a>
          <a
            href="#"
            style={{
              color: '#FFFFFF',
              textDecoration: 'none',
              fontSize: '16px',
              fontWeight: '500',
              cursor: 'pointer',
            }}
          >
            About
          </a>
          <a
            href="#"
            style={{
              color: '#FFFFFF',
              textDecoration: 'none',
              fontSize: '16px',
              fontWeight: '500',
              cursor: 'pointer',
            }}
          >
            Contact
          </a>
        </div>
      </nav>

      {/* Main Content */}
      <div
        style={{
          width: '100%',
          height: '100%',
          backgroundColor: '#0D1117',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
        }}
      >
        {/* Highcharts */}
        <div style={{ width: '90%', height: '60%', marginBottom: '20px' }}>
          <HighchartsReact
            highcharts={Highcharts}
            constructorType={'stockChart'}
            options={chartOptions}
          />
        </div>

        {/* Example Section */}
        <div
          style={{
            width: '90%',
            height: '30%',
            backgroundColor: '#2765c2',
            borderRadius: '8px',
          }}
        >
          <h1 style={{ color: '#FFFFFF', textAlign: 'center' }}>Yolo</h1>
          <button onClick={entry_click} className="custom-button">
            Click me
          </button>
        </div>
      </div>
    </div>
  );
}

export default App;
