import Plot from "react-plotly.js";

interface Props {
  key: number;
  chartJSON: string;
}

const PlotlyChart = (props: Props) => {
  // prop is a string, convert to chart object (with data and layout)
  const chart = JSON.parse(props.chartJSON);
  console.log("chart being made");
  const layout = chart.layout;
  layout["autosize"] = true;
  console.log(layout);
  return (
    <>
      <Plot
        data={chart.data}
        layout={layout}
        useResizeHandler
        style={{ width: "100%", height: "100%" }}
      />
    </>
  );
};

export default PlotlyChart;
