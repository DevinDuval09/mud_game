from mongo import mongo
from ..python_classes.Fighter import Fighter
from ..python_classes.Wizard import Wizard
from ..python_classes.Rogue import Rogue
from ..python_classes.Room import Room
from ..python_classes.utils import create_character_fromId
from ..python_classes.Items import create_item_fromId
from ..python_classes.Items import Item
import json #to create json objects to pass to frontend. see json encoder

'''
ObjectManager is here to track the state of active objects on the server.
'''
class ServerStateManager:

    def __init__(self):
        self.active_characters = []
        self.active_rooms={}

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

    def execute_player_input(self, player: str, command: str) -> str:
        pass
