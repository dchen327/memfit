import Plot from "react-plotly.js";

interface Props {
  key: number;
  chartJSON: string;
}

const PlotlyChart = (props: Props) => {
  // prop is a string, convert to chart object (with data and layout)
  const chart = JSON.parse(props.chartJSON);
  console.log("chart being made");
  return (
    <>
      <Plot data={chart.data} layout={chart.layout} />
    </>
  );
};

export default PlotlyChart;
