import logo from './logo.svg';
import './App.css';
import HealthScreen from "./HealthScreen.tsx";
import EquipmentPanel from './EquipmentScreen';
import Equipment from './Equipment';

function App() {
  const maxHealth = 40;
  const currentHealth = 10;
  const equipment = new Equipment(
                    Head= "Iron helmet",
                    Torso= "Breastplate",
                    Arms= null,
                    MainHand= "Longsword",
                    OffHand= "Shield",
                    Legs= "Leather pants",
                    Belt= "Leather belt",
                    Back= "Backpack",
                    Feet= "Leather boots",
                    Cloak= null
                  )
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
        <div>
          <HealthScreen maxHealth={maxHealth} currentHealth={currentHealth} />
        </div>
        <div>
          <EquipmentPanel equipment={equipment} />
        </div>
      </header>
    </div>
  );
}

export default App;
