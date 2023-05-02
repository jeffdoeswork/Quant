import Plot from 'react-plotly.js';
import React, { useState, useEffect } from 'react';
import { useForm } from 'react-hook-form';

const NewChart = ({ data }) => {

        const plotData = [
          // {
          //   x: data.map(d => d.date),
          //   y: data.map(d => (d.buy_indicator || d.sell_indicator) ? d.close : null),
          //   mode: 'markers',
          //   marker: {
          //     size: 10,
          //     color: data.map(d => {
          //       if (d.buy_indicator) return 'green';
          //       if (d.sell_indicator) return 'red';
          //       return null;
          //     }),
          //   },
          //   type: 'scatter',
          //   hoverinfo: 'none',
          // },
          {
            x: data.map(d => d.date),
            y: data.map(d => (d.buy_indicator) ? d.high : null),
            mode: 'markers',
            marker: {
              size: 10,
              color: 'green',
              },
            type: 'scatter',
            hoverinfo: 'none',
          },
          {
            x: data.map(d => d.date),
            y: data.map(d => (d.sell_indicator) ? d.low : null),
            mode: 'markers',
            marker: {
              size: 10,
              color: 'red',
              },
            type: 'scatter',
            hoverinfo: 'none',
          },
          // OHLC data
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

          // {
          //   x: data.map((d) => d.date),
          //   y: data.map((d) => d.buy_indicator),
          //   type: 'scatter',
          //   mode: 'markers',
          //   marker: {
          //     size: 10,
          //     color: data.map(d => {
          //       if (d.buy_indicator) return 'green';
          //       if (d.sell_indicator) return 'red';
          //       return null;
          //     }),
          //   },
          //   name: 'Red Dot',
          // },

        ];
        
        const layout = {
          // title: 'OHLC Chart with Custom Indicators',
          yaxis: {
            title: 'Price',
          },
          xaxis: {
            rangeslider: { visible: false },
          },
          showlegend: false,
          width: 1200,
        };
      
        return <Plot data={plotData} layout={layout} />;
      };

export default NewChart;
