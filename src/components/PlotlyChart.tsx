import React from "react";
import Plot from "react-plotly.js";

interface Props {
  chartJSON: string;
}

const PlotlyChart = (props: Props) => {
  // prop is a string, convert to chart object (with data and layout)
  const chart = JSON.parse(props.chartJSON);
  return (
    <>
      <Plot data={chart.data} layout={chart.layout} />
    </>
  );
};

export default PlotlyChart;
