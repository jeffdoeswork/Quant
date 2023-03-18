// App.js
import React, { useState } from 'react';
import { Candlestick } from 'react-chartjs-2';
import axios from 'axios';
import Chart from 'react-apexcharts';

function App() {
  const [stock, setStock] = useState('');
  const [dateRange, setDateRange] = useState('Day');
  const [chartData, setChartData] = useState({
    labels: [],
    datasets: [
      {
        label: 'Closing Price',
        data: [],
        borderColor: 'rgba(75,192,192,1)',
        backgroundColor: 'rgba(0,0,0,0)',
        borderWidth: 2,
      },
    ],
  });
  
  const options = {
    scales: {
      y: {
        beginAtZero: true,
      },
    },
  };

  
  const fetchData = async () => {
    try {
      const response = await axios.get('http://127.0.0.1:5000/api/stock', {
        params: { stock, date_range: dateRange },
      });
      const data = response.data;
      console.log(data);
  
      if (Array.isArray(data)) {
        const ohlcData = data.map((entry) => ({
          t: entry.Date,
          o: entry.Open,
          h: entry.High,
          l: entry.Low,
          c: entry.Close,
        }));

        const dates = data.map((entry) => entry.Date);
        const closingPrices = data.map((entry) => [entry.Open, entry.High, entry.Low, entry.Close]);
        
        setChartData({
          labels: dates,
          datasets: [
            {
              data: closingPrices,
            },
          ],
        });

      } else {
        console.error('Error fetching data: Data is not an array');
      }
    } catch (error) {
      console.error('Error fetching data:', error);
    }
  };

  const chartOptions = {
    chart: {
      type: 'candlestick',
    },
    title: {
      text: `${stock} Price`,
    },
    xaxis: {
      type: 'datetime',
      categories: chartData.labels,
    },
    yaxis: {
      tooltip: {
        enabled: true,
      },
    },
  };

  const series = [
    {
      data: chartData.datasets[0].data.map((price, index) => {
        return {
          x: chartData.labels[index],
          y: price,
        };
      }),
    },
  ];

  return (
    <div className="App">
      <h1>Stock Chart App</h1>
      <form
        onSubmit={(e) => {
          e.preventDefault();
          fetchData();
        }}
      >
        <label>
          Stock:
          <input
            type="text"
            value={stock}
            onChange={(e) => setStock(e.target.value)}
          />
        </label>
        <label>
          Date Range:
          <select
            value={dateRange}
            onChange={(e) => setDateRange(e.target.value)}
          >
            <option value="Day">Day</option>
            <option value="Week">Week</option>
            <option value="Month">Month</option>
          </select>
        </label>
        <button type="submit">Fetch Data</button>
      </form>
      <div>
        <Chart options={chartOptions} series={series} type="candlestick" />
      </div>
    </div>
  );
}

export default App;
