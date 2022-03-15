import { Navbar } from "./components/Navbar";
import "bulma/css/bulma.min.css";

function App() {
  const logSleep = () => {
    const newDate = new Date();
    console.log(newDate.toLocaleDateString());
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
