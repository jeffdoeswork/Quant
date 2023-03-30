import React from 'react';
import { Chart } from 'react-google-charts';

const CandlestickChartWithRedDot = () => {
  const data = [
    ['Trading Time', 'Low', 'Opening', 'Closing', 'High'],
    // Add your trading data for a single day here
    ['2023-03-26 10:00', 100, 110, 120, 130],
    ['2023-03-26 11:00', 90, 100, 110, 120],
    ['2023-03-26 12:00', 80, 90, 100, 110],
    // ...
  ];

  const blueDotData = data.slice(1).map((d, i) => ({
    x: i,
    y: d[2],
  }));

  return (
    <Chart
      chartType="ComboChart"
      data={data}
      options={{
        chartArea: { width: '90%', height: '70%' },
        legend: 'none',
        seriesType: 'candlesticks',
        series: {
          1: {
            type: 'scatter',
            pointSize: 5,
            color: 'blue',
            lineWidth: 0,
            visibleInLegend: false,
          },
        },
        candlestick: {
          fallingColor: { strokeWidth: 0, fill: '#a52714' },
          risingColor: { strokeWidth: 0, fill: '#0f9d58' },
        },
        vAxis: {
          title: 'Price',
        },
        hAxis: {
          title: 'Trading Time',
        },
      }}
      width="100%"
      height="400px"
    />
  );
};



export default CandlestickChartWithRedDot;
