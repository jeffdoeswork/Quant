import Plot from 'react-plotly.js';
import React, { useState, useEffect } from 'react';
import { useForm } from 'react-hook-form';

const NewChart = ({ data }) => {

        const plotData = [
          {
            x: data.map(d => d.date),
            close: data.map(d => d.close),
            high: data.map(d => d.high),
            low: data.map(d => d.low),
            open: data.map(d => d.open),
      
            decreasing: { line: { color: 'grey' } },
            increasing: { line: { color: 'grey' } },
            line: { color: 'rgba(31,119,180,1)' },
            type: 'ohlc',
          },
          {
            x: data.map(d => d.date),
            y: data.map(d => (d.green || d.red) ? d.close : null),
            mode: 'markers',
            marker: {
              size: 10, // Increase the size of the markers
              color: data.map(d => {
                if (d.green) return 'green';
                if (d.red) return 'red';
                return null;
              }),
            },
            type: 'scatter',
          },
        ];
      
        const layout = {
          title: 'OHLC Chart with Custom Indicators',
          yaxis: {
            title: 'Price',
          },
          xaxis: {
            rangeslider: { visible: false },
          },
          showlegend: false,
        };
      
        return <Plot data={plotData} layout={layout} />;
      };

export default NewChart;
