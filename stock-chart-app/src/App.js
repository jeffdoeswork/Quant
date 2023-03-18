import React, { useState } from 'react';
import { Line } from 'react-chartjs-2';
import axios from 'axios';
import { Chart, LinearScale, CategoryScale, PointElement, LineController, LineElement } from 'chart.js';

Chart.register(LinearScale);
Chart.register(CategoryScale);
Chart.register(PointElement);
Chart.register(LineController);
Chart.register(LineElement);



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
        const dates = data.map((entry) => entry.Date);
        const closingPrices = data.map((entry) => entry.Close);
  
        setChartData({
          labels: dates,
          datasets: [
            {
              label: 'Closing Price',
              data: closingPrices,
              borderColor: 'rgba(75,192,192,1)',
              backgroundColor: 'rgba(0,0,0,0)',
              borderWidth: 2,
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
      <Line data={chartData} key={Math.random()} />
      </div>
    </div>
  );
}

export default App;
