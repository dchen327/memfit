import "bulma/css/bulma.min.css";
import { Navbar } from "./components/Navbar";
import { initializeApp } from "firebase/app";

const firebaseConfig = {
  apiKey: "AIzaSyAOP5AI_22FkCuUhsaCoCuXwp4J1CpMDQo",
  authDomain: "mem-fit.firebaseapp.com",
  projectId: "mem-fit",
  storageBucket: "mem-fit.appspot.com",
  messagingSenderId: "30218199815",
  appId: "1:30218199815:web:0063e72bf03da378eb9ba2",
};

initializeApp(firebaseConfig);

function App() {
  const logSleep = () => {
    fetch("/api/logSleep");
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
    </div>
  );
}

export default App;
