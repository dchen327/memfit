import { Navbar } from "./components/Navbar";
import "bulma/css/bulma.min.css";

function App() {
  return (
    <div>
      <section className="section">
        <Navbar />
      </section>
      <section className="section">
        <button className="button">Log Sleep</button>
      </section>
    </div>
  );
}

export default App;
