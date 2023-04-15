import React from 'react';
import Plot from 'react-plotly.js';

const CustomBarChart = ({ data }) => {

    const calculateShapes = (data) => {
        const shapes = data.map((d) => d.close - d.open);
      
        const shapeAve = shapes.slice(0, 5).reduce((a, b) => a + b, 0) / 5;
        const shapeAve3 = shapes.slice(0, 3).reduce((a, b) => a + b, 0) / 3;
      
        const shapeMagnAve =
          shapes.slice(0, 5).map(Math.abs).reduce((a, b) => a + b, 0) / 5;
      
        const shapeAve31 = shapes.reduce((a, b) => a + b, 0) / shapes.length;
      
        return {
          shapeAve,
          shapeAve3,
          shapeMagnAve,
          shapeAve31,
        };
      };
      
      
  const { shapeAve, shapeAve3, shapeMagnAve, shapeAve31 } = calculateShapes(data);

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
      y: Array(data.length).fill(shapeAve),
      type: 'scatter',
      mode: 'lines',
      line: { color: 'blue' },
      name: 'shapeAve',
    },
    // Add more lines as needed
  ];

  const layout = {
    title: 'Custom Bar Chart with Lines',
    yaxis: { title: 'Price' },
    xaxis: { type: 'category' },
    showlegend: true,
  };

  return <Plot data={plotData} layout={layout} />;
};

export default CustomBarChart;
