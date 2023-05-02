import React from 'react';
import Plot from 'react-plotly.js';

const CustomBarChart = ({ data }) => {
      
  const plotData = [
    {
      x: data.map((d) => d.date),
      y: data.map((d) => d.close - d.open),
      type: 'bar',
      marker: {
        color: data.map((d) => (d.close - d.open > 0 ? 'green' : 'red')),
      },
    },
    {
      x: data.map((d) => d.date),
      y: data.map((d) => d.Line1),
      type: 'scatter',
      mode: 'lines',
      line: { color: 'orange' },
      name: 'Top Flow',
    },
    {
      x: data.map((d) => d.date),
      y: data.map((d) => d.Line2),
      type: 'scatter',
      mode: 'lines',
      line: { color: 'purple' },
      name: 'Bottom Flow',
    },
    {
      x: data.map((d) => d.date),
      y: data.map((d) => d.Gas),
      type: 'scatter',
      mode: 'lines',
      line: { color: 'blue' },
      name: 'Gas',
    },
    // Add more lines as needed
  ];

  const layout = {
    // title: 'Custom Bar Chart with Lines',
    yaxis: { title: 'Price' },
    xaxis: { type: 'category' },
    showlegend: true,
    width: 1200,
  };

  return <Plot data={plotData} layout={layout} />;
};

export default CustomBarChart;
