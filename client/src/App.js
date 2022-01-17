import './App.css';
import RoomScreen from './RoomScreen.tsx';
import PlayerScreen from './PlayerScreen.tsx';
import UserInput from './Input.tsx';

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
  var inventory = ["Healing Potion", "Scroll", "Bread"];
  return (
    <div className="App">
        <PlayerScreen equipment={equipment}
                      maxHealth={maxHealth}
                      currentHealth={currentHealth}
                      stats={stats}
                      inventory={inventory} />
        <RoomScreen key={"RoomDisplay"}
                    description={room.description}
                    items={room.items}
                    itemAlignment={room.itemAlignment}
                    characters={room.characters}
                    charAlignment={room.charAlignment} />
        <UserInput />
    </div>
  );
}

export default App;
