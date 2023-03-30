import logo from './logo.svg';
import './App.css';
import StockChart from './StockChart';
import NewChart from './NewChart';


const App = () => {
  const data = [
    {
      date: '2021-03-01',
      open: 100,
      high: 110,
      low: 95,
      close: 105,
    },
    {
      date: '2021-03-02',
      open: 105,
      high: 115,
      low: 100,
      close: 110,
    },
    // more data...
  ];

  return (
    <div className="App">
      <NewChart data={data} />
    </div>
  );
};

export default App;