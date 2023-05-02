import React, { useState, useEffect } from 'react';
import { useForm } from 'react-hook-form';
import './App.css';
import NewChart from './NewChart';
import CustomBarChart from './CustomBarChart';

const App = () => {
  const [data, setData] = useState([]);
  const { register, handleSubmit } = useForm();

  const onSubmit = (data) => {
    fetchStockData(data.stock);
  };

  const fetchStockData = async (stock) => {
    try {
      const response = await fetch(`http://127.0.0.1:5000/api?stock=${stock}`);
      const jsonData = await response.json();
      setData(jsonData);
    } catch (error) {
      console.error("Error fetching stock data:", error);
    }
  };
  

  useEffect(() => {
  }, []);

  return (
    <div className="App">
      <form onSubmit={handleSubmit(onSubmit)}>
        <label htmlFor="stock">Stock Ticker:</label>
        <input type="text" id="stock" {...register('stock')} required />

        <button type="submit">Fetch Data</button>
      </form>

      <NewChart data={data} />
      <br></br>
      <CustomBarChart data={data} />
    </div>
  );
};
export default App;
