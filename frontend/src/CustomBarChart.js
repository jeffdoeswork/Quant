import React from 'react';
import Plot from 'react-plotly.js';

const CustomBarChart = ({ data }) => {
      
  const plotData = [
    {
      x: [null, null, ...data.map((d) => d.date)],
      y: [null, null, ...data.map((d) => d.Gas)],
      type: 'bar',
      marker: {
        color: 'gray',
      },
    },
    {
      x: [null, null, ...data.map((d) => d.date)],
      y: [null, null, ...data.map((d) => d.TopManifold)],
      type: 'scatter',
      mode: 'lines',
      line: { color: 'orange' },
      name: 'Top Flow',
    },
    {
      x: [null, null, ...data.map((d) => d.date)],
      y: [null, null, ...data.map((d) => d.BottomManifold)],
      type: 'scatter',
      mode: 'lines',
      line: { color: 'orange' },
      name: 'Bottom Flow',
    },
    {
      x: [null, null, ...data.map((d) => d.date)],
      y: [null, null, ...data.map((d) => d.GasNew)],
      type: 'scatter',
      mode: 'lines',
      line: { color: 'green' },
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
