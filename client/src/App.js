import logo from './logo.svg';
import './App.css';
import HealthScreen from "./HealthScreen.tsx";
import EquipmentPanel from './EquipmentScreen.tsx';
import StatScreen from './StatScreen.tsx';
import RoomScreen from './RoomScreen.tsx';

function App() {
  const maxHealth = 40;
  const currentHealth = 10;
  var equipment = {};
  equipment["Helmet"] = "Iron Helmet";
  equipment["Torso"] = "Breastplate";
  equipment["Arms"] = null;
  equipment["MainHand"] = "Longsword";
  equipment["OffHand"] = "Shield";
  equipment["Legs"] = "Leather pants";
  equipment["Belt"] = "Leather belt";
  equipment["Back"] = "Backpack";
  equipment["Feet"] = "Leather boots";
  equipment["Cloak"] = null;
  var stats = {};
  stats["Str"] = 18;
  stats["Dex"] = 15;
  stats["Con"] = 17;
  stats["Int"] = 7;
  stats["Wis"] = 8;
  stats["Cha"] = 10;
  stats[""] = null;
  stats["AC"] = 16;
  var room = {};
  room["description"] = "A room.";
  room["items"] = ["Table", "Chair", "Candle"];
  room["characters"] = ["Larry", "Curly", "Moe"];
  room["itemAlignment"] = "left";
  room["charAlignment"] = "right";
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
        <div>
          <StatScreen stats={stats} />
        </div>
        <div>
          <RoomScreen description={room.description}
                      items={room.items}
                      itemAlignment={room.itemAlignment}
                      characters={room.characters}
                      charAlignment={room.charAlignment} />
        </div>
      </header>
    </div>
  );
}

export default App;
