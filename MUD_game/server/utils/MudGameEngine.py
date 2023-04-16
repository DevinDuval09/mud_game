from .DatabaseConnection import DatabaseConnect
from ..python_classes.Fighter import Fighter
from ..python_classes.Wizard import Wizard
from ..python_classes.Rogue import Rogue
from ..python_classes.Room import Room
from ..python_classes.Items import Item

'''
ObjectManager is here to track the state of active objects on the server.
'''
class MudGameEngine:
    character_classes = {
                        "fighter": Fighter,
                        "rogue": Rogue,
                        "wizard": Wizard
                        }

    def __init__(self, database:DatabaseConnect):
        #characters logged into this instance
        self.active_characters = []
        #rooms that have been generated for this instance
        self.active_rooms={}
        self.db_connect = database

    def create_item(self, number:int) -> Item:
        return create_item_fromId(number)


    def create_room(self, id:int):
        new_room = Room.fromId(id)
        self.active_rooms[id] = new_room
        return new_room

    def execute_player_input(self, player: str, command: str) -> dict:
        character = self.active_characters[player]
        room = None
        if(character.room) in self.active_rooms.keys():
            room = self.active_rooms[character.room]
        else:
            room = self.create_room(character.room)
        args = command.lower().split(" ")
        command = args.pop(0)
        if command == "move":
            #remove character from current room
            #put character in new room
            #update characters current room
            #generate message to moving player
            #generate messages to other players
            pass

    def create_new_character(self, player:dict):
        player_class = MudGameEngine.character_classes[player["type"]]
        cleaned_dict = {}
        for key, val in player.items():
            if key == "strength":
                cleaned_dict["STR"] = int(val)
            elif key == "dexterity":
                cleaned_dict["DEX"] = int(val)
            elif key == "constitution":
                cleaned_dict["CON"] = int(val)
            elif key == "wisdom":
                cleaned_dict["WIS"] = int(val)
            elif key == "intelligence":
                cleaned_dict["INT"] = int(val)
            elif key == "charisma":
                cleaned_dict["CHA"] = int(val)
            elif key == "password":
                pass #passwords aren't attached to objects
            else:
                cleaned_dict[key] = val
        new_character = player_class(**cleaned_dict)
        new_character.level = 1
        new_character.room = 1
        self.active_characters.append(new_character)
        if 0 not in self.active_rooms.keys():
            self.active_rooms[0] = self.db_connect.get_room(0)
        return new_character

    def get_state(self, user:str, data:str):
        print(f"Engine: request received from {user} for {data}")



