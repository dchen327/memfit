import "bulma/css/bulma.min.css";
import { Navbar } from "./components/Navbar";
import { initializeApp } from "firebase/app";
import { useEffect, useState } from "react";
import Charts from "./components/Charts";

const firebaseConfig = {
  apiKey: "AIzaSyAOP5AI_22FkCuUhsaCoCuXwp4J1CpMDQo",
  authDomain: "mem-fit.firebaseapp.com",
  projectId: "mem-fit",
  storageBucket: "mem-fit.appspot.com",
  messagingSenderId: "30218199815",
  appId: "1:30218199815:web:0063e72bf03da378eb9ba2",
};

initializeApp(firebaseConfig);

interface ICharts {
  [chartName: string]: string;
}

function App() {
  const [charts, setCharts] = useState<ICharts | null>(null);

  const chartNames = ["Sleep"];

  useEffect(() => {
    console.log("pulling chart from api");
    fetch("/api/charts", {
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
      },
      method: "POST",
      body: JSON.stringify({
        // params: charts is a list of chart names to return
        charts: ["Sleep"],
      }),
    }).then((res) =>
      res.json().then((chartJSON) => {
        setCharts(chartJSON);
      })
    );
  }, []);

  const logSleep = () => {
    fetch("/api/logSleep", {
      method: "POST",
    });
    console.log("api called");
  };

  return (
    <div>
      <section className="section">
        <Navbar />
      </section>
      <section className="section">
        <button className="button" onClick={logSleep}>
          Log Sleep
        </button>
      </section>
      <section className="section">
        {charts && <Charts charts={charts} chartNames={chartNames} />}
      </section>
    </div>
  );
}

export default App;
