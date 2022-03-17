import { Footer } from "./components/Footer";
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

  const chartNames = ["sleep"];

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
        charts: ["sleep"],
      }),
    }).then((res) =>
      res.json().then((chartJSON) => {
        setCharts(chartJSON);
      })
    );
  }, []);

  const logSleep = async () => {
    const res = await fetch("/api/logSleep", {
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
      },
      method: "POST",
      body: JSON.stringify({
        currTime: new Date().getTime(),
      }),
    });
    const resText = await res.text();
    console.log("api called", resText);
  };

  return (
    // Use columns horizontally, set
    <div
      className="columns is-flex-direction-column"
      style={{ height: "100vh" }}
    >
      <Navbar />
      <div className="column is-narrow has-text-centered">
        <button className="button" onClick={logSleep}>
          Log Sleep
        </button>
      </div>
      <div className="column has-text-centered">
        {charts && <Charts charts={charts} chartNames={chartNames} />}
      </div>
      <Footer />
    </div>
  );
}

export default App;
