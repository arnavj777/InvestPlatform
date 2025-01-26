import React from 'react';
import Highcharts from 'highcharts';
import HighchartsReact from 'highcharts-react-official';

function Simulations() {

  // Chart configuration
  const chartOptions = {
    chart: {
      type: 'line', // Specify the chart type
    },
    title: {
      text: 'Simple Line Chart', // Chart title
    },
    xAxis: {
      categories: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'], // X-axis categories
      title: {
        text: 'Months', // X-axis label
      },
    },
    yAxis: {
      title: {
        text: 'Values', // Y-axis label
      },
    },
    series: [
      {
        name: 'Dataset 1', // Legend name
        data: [29, 71, 106, 129, 144, 176], // Y-axis data points
      },
      {
        name: 'Dataset 2',
        data: [39, 61, 96, 119, 134, 166],
      },
    ],
  };

  return (
    <div>
      <h1>Simulation Page</h1>
      <p>Welcome to the Simulation Page!</p>
      <h1>Highcharts Line Chart Example</h1>
      <HighchartsReact highcharts={Highcharts} options={chartOptions} />
    </div>
  );
}

export default Simulations;
