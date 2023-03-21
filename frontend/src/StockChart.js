import React, { Component } from "react";
import { Chart } from "react-google-charts";

class StockChart extends Component {
  constructor(props) {
    super(props);
    this.state = {
      ticker: "",
      dateRange: "Day",
      data: [["Date", "Low", "Opening value", "Closing value", "High"]],
    };
  }

  handleInputChange = (event) => {
    const target = event.target;
    const value = target.value;
    const name = target.name;

    this.setState({
      [name]: value,
    });
  };

  handleSubmit = async (event) => {
    event.preventDefault();
    const { ticker, dateRange } = this.state;

    const response = await fetch(
      `http://127.0.0.1:5000/api?stock=${ticker}&date_range=${dateRange}`
    );
    const stockData = await response.json();

    const data = [
      ["Date", "Low", "Opening value", "Closing value", "High"],
      ...stockData.map((item) => [
        item.Date,
        item.Low,
        item.Open,
        item.Close,
        item.High,
      ]),
    ];

    this.setState({ data });
  };

  render() {
    const { data, ticker, dateRange } = this.state;

    return (
      <div>
        <h2>Stock Chart</h2>
        <form onSubmit={this.handleSubmit}>
          <label htmlFor="ticker">Stock:</label>
          <input
            type="text"
            id="ticker"
            name="ticker"
            value={ticker}
            onChange={this.handleInputChange}
          />
          <label htmlFor="dateRange">Date Range:</label>
          <select
            id="dateRange"
            name="dateRange"
            value={dateRange}
            onChange={this.handleInputChange}
          >
            <option value="Day">Day</option>
            <option value="Week">Week</option>
            <option value="Month">Month</option>
          </select>
          <button type="submit">Submit</button>
        </form>
        <Chart
          width={"100%"}
          height={"400px"}
          chartType="CandlestickChart"
          loader={<div>Loading Chart</div>}
          data={data}
          options={{
            legend: "none",
            bar: { groupWidth: "80%" },
            candlestick: {
              fallingColor: { strokeWidth: 0, fill: "#a52714" }, // red
              risingColor: { strokeWidth: 0, fill: "#0f9d58" }, // green
            },
          }}
        />
      </div>
    );
  }
}

export default StockChart;
