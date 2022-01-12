import logo from './logo.svg';
import './App.css';
import HealthScreen from "./HealthScreen.tsx";

function App() {
  const maxHealth = 40;
  const currentHealth = 10;
  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Edit <code>src/App.js</code> and save to reload.
        </p>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
        <p>
          <HealthScreen maxHealth={maxHealth} currentHealth={currentHealth} />
        </p>
      </header>
    </div>
  );
}

export default App;
