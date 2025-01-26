import React, { useState, useEffect } from 'react';
import Highcharts from 'highcharts';
import HighchartsReact from 'highcharts-react-official';

function Simulations() {
  const [charts, setCharts] = useState([]); // Initialize as an empty array

  // Fetch charts dynamically from the backend
  const fetchCharts = () => {
    fetch('/sim_charts', {
      method: 'GET',
      headers: { 'Content-Type': 'application/json' },
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json(); // Parse JSON response
      })
      .then((data) => {
        if (Array.isArray(data)) {
          setCharts(data); // Update charts with data from the backend
        } else {
          console.error('Unexpected API response:', data);
        }
      })
      .catch((error) => {
        console.error('Error fetching charts:', error);
      });
  };

  // Load charts on component mount
  useEffect(() => {
    fetchCharts();
  }, []);

  const handleRemoveChart = (index) => {
    setCharts((prev) => prev.filter((_, i) => i !== index));
  };

  return (
    <div>
      <h1>Simulation Page</h1>
      <p>Welcome to the Simulation Page!</p>

      <div>
        <button onClick={fetchCharts}>Load Charts</button>
      </div>

      <div style={{ marginTop: '20px' }}>
        <h2>Dynamic Charts</h2>
        {charts.length > 0 ? (
          charts.map((chartOptions, index) => (
            <div
              key={index}
              style={{
                marginBottom: '20px',
                border: '1px solid gray',
                padding: '10px',
              }}
            >
              <HighchartsReact highcharts={Highcharts} options={chartOptions} />
              
              <h3>{chartOptions.symbol} Additional Info</h3>
              {chartOptions.textData && chartOptions.textData.length > 0 ? (
                <ul>
                  {chartOptions.textData.map((line, idx) => (
                    <li key={idx}>{line}</li>
                  ))}
                </ul>
              ) : (
                <h6>No additional data available.</h6>
              )}
              
              <button
                onClick={() => handleRemoveChart(index)}
                style={{ marginTop: '10px' }}
              >
                Remove Chart
              </button>
            </div>
          ))
        ) : (
          <p>No charts available.</p> // Show this message if charts array is empty
        )}
      </div>
    </div>
  );
}

export default Simulations;
