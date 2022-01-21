import './App.css';
import RoomScreen from './RoomScreen.tsx';
import PlayerScreen from './PlayerScreen.tsx';
import UserInput from './Input.tsx';
import MainScreen from './MainScreen.tsx';

history = ["Welcome to a world of Dragons, Magic, and Adventure!"];

function getRoom()
{
    //need to beable to parse out description, inventory, and characters
}

function getCharacter()
{
    //need to beable to parse out health, equipment, inventory, and stats
}

function updateHistory()
{
    //sent new line to MainScreen?
}

function App() {
  return (
    <div className="App">
        <MainScreen history={history} />
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
