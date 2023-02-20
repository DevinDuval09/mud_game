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

    def __init__(self, database:DatabaseConnect):
        #characters logged into this instance
        self.active_characters = []
        #rooms that have been generated for this instance
        self.active_rooms={}
        self.db_connect = database

    def create_character(self, name:str, *args, char_class=None, **kwargs):
        doc = None
        new_character = None
        with mongo:
            doc = mongo.db["Players"].find_one({"name": name})
        if(doc):
            #pull a character from the server
            new_character = create_character_fromId(name)
        else:
            #make a brand new character and save it to the db
            class_dict = {"Fighter": Fighter, "Rogue": Rogue, "Wizard": Wizard}
            if char_class in class_dict.keys():
                new_character = class_dict[char_class].create(*args, **kwargs)
                
        if new_character:
            self.active_characters.append(new_character)


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



