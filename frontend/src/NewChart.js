import React from 'react';
import Plot from 'react-plotly.js';

const NewChart = ({ data }) => {

        const plotData = [
          {
            x: data.map(d => d.date),
            close: data.map(d => d.close),
            high: data.map(d => d.high),
            low: data.map(d => d.low),
            open: data.map(d => d.open),
      
            decreasing: { line: { color: 'red' } },
            increasing: { line: { color: 'green' } },
            line: { color: 'rgba(31,119,180,1)' },
            type: 'ohlc',
          },
        ];
      
        const layout = {
          title: 'OHLC Chart',
          yaxis: {
            title: 'Price',
          },
          xaxis: {
            rangeslider: { visible: false },
          },
        };
      
        return <Plot data={plotData} layout={layout} />;
      };

export default NewChart;
