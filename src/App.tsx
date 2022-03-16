import "bulma/css/bulma.min.css";
import { Navbar } from "./components/Navbar";
import { initializeApp } from "firebase/app";
import { useEffect, useState } from "react";
import Charts from "./components/Charts";

const firebaseConfig = {
  apiKey: process.env.REACT_APP_FIREBASE_API_KEY,
  authDomain: process.env.REACT_APP_FIREBASE_AUTH_DOMAIN,
  projectId: process.env.REACT_APP_FIREBASE_PROJECT_ID,
  storageBucket: process.env.REACT_APP_FIREBASE_STORAGE_BUCKET,
  messagingSenderId: process.env.REACT_APP_FIREBASE_SENDER_ID,
  appId: process.env.REACT_APP_FIREBASE_APP_ID,
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
