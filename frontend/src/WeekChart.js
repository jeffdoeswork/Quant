import React from 'react';
import Plot from 'react-plotly.js';

const WeekChart = ({ data }) => {
      
  const plotData = [
    {
      x: data.map((d) => d.date),
      y: data.map((d) => d.GasNew),
      type: 'bar',
      marker: {
        // color: data.map((d) => (d.close - d.open > 0 ? 'green' : 'red')),
         color: 'gray',
      },
    },
    {
      x: data.map((d) => d.date),
      y: data.map((d) => d.TopManifold),
      type: 'scatter',
      mode: 'lines',
      line: { color: 'orange' },
      name: 'Top Flow',
    },
    {
      x: data.map((d) => d.date),
      y: data.map((d) => d.BottomManifold),
      type: 'scatter',
      mode: 'lines',
      line: { color: 'orange' },
      name: 'Bottom Flow',
    },
    {
      x: data.map((d) => d.date),
      y: data.map((d) => d.Gas),
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

export default WeekChart;
