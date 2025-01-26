import React, { useState, useRef } from 'react';
import Highcharts from 'highcharts';
import HighchartsReact from 'highcharts-react-official';

function Simulations() {
  const [charts, setCharts] = useState([
    {
      chart: { type: 'line' },
      title: { text: 'Default Chart 1' },
      xAxis: {
        categories: ['Point 1', 'Point 2', 'Point 3', 'Point 4'],
      },
      yAxis: { title: { text: 'Values' } },
      series: [
        {
          name: 'Series 1',
          data: [10, 20, 15, 30],
        },
      ],
    },
    {
      chart: { type: 'column' },
      title: { text: 'Default Chart 2' },
      xAxis: {
        categories: ['Category A', 'Category B', 'Category C'],
      },
      yAxis: { title: { text: 'Frequency' } },
      series: [
        {
          name: 'Series 1',
          data: [5, 12, 8],
        },
      ],
    },
  ]);

  const titleRef = useRef();
  const dataRef = useRef();

  const handleAddChart = () => {
    const title = titleRef.current.value.trim();
    const dataString = dataRef.current.value.trim();

    if (!title || !dataString) {
      alert('Please provide a valid title and data.');
      return;
    }

    const parsedData = dataString.split(',').map((num) => parseFloat(num));

    if (parsedData.some(isNaN)) {
      alert('Please provide a valid list of numbers separated by commas.');
      return;
    }

    const newChartConfig = {
      chart: { type: 'line' },
      title: { text: title },
      xAxis: {
        categories: Array(parsedData.length)
          .fill()
          .map((_, i) => `Point ${i + 1}`),
      },
      yAxis: { title: { text: 'Values' } },
      series: [
        {
          name: title,
          data: parsedData,
        },
      ],
    };

    setCharts((prev) => [...prev, newChartConfig]);
    titleRef.current.value = '';
    dataRef.current.value = '';
  };

  const handleRemoveChart = (index) => {
    setCharts((prev) => prev.filter((_, i) => i !== index));
  };

  return (
    <div>
      <h1>Simulation Page</h1>
      <p>Welcome to the Simulation Page!</p>

      <div style={{ marginTop: '20px' }}>
        <h2>Dynamic Charts</h2>
        {charts.map((chartOptions, index) => (
          <div key={index} style={{ marginBottom: '20px', border: '1px solid gray', padding: '10px' }}>
            <HighchartsReact highcharts={Highcharts} options={chartOptions} />
            <button onClick={() => handleRemoveChart(index)} style={{ marginTop: '10px' }}>
              Remove Chart
            </button>
          </div>
        ))}
      </div>
    </div>
  );
}

export default Simulations;
