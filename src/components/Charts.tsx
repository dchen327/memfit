import PlotlyChart from "./PlotlyChart";

interface Props {
  charts: ;
  chartNames: string[];
}

const Charts = (props: Props) => {
  return (
    <>
      {props.charts &&
        props.chartNames.map((chartName: string, index: number) => {
          console.log(typeof chartName);
          return (
            <PlotlyChart key={index} chartJSON={props.charts[chartName]} />
          );
        })}
    </>
  );
};

export default Charts;
