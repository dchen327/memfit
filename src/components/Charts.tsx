import PlotlyChart from "./PlotlyChart";

interface Props {
  charts: { [chartName: string]: string };
  chartNames: string[];
}

const Charts = (props: Props) => {
  return (
    <>
      {props.charts &&
        props.chartNames.map((chartName: string, index: number) => {
          return (
            <PlotlyChart key={index} chartJSON={props.charts[chartName]} />
          );
        })}
    </>
  );
};

export default Charts;
