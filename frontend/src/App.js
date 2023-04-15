import React, { useState, useEffect } from 'react';
import './App.css';
import NewChart from './NewChart';
import CustomBarChart from './CustomBarChart';

const App = () => {
  const [data, setData] = useState([]);

  const fetchStockData = async (stock, dateRange) => {
    try {
      const response = await fetch(`http://127.0.0.1:5000/api?stock=${stock}&date_range=${dateRange}`);
      const jsonData = await response.json();
      setData(jsonData);
      console.log(jsonData);
    } catch (error) {
      console.error("Error fetching stock data:", error);
    }
  };

  useEffect(() => {
    fetchStockData("AAPL", "Week"); // Replace "AAPL" and "Week" with the desired stock and date range.
  }, []);

  return (
    <div className="App">
      <NewChart data={data} />

      <br></br>

      <CustomBarChart data={data} />
    </div>
  );
};

export default App;
