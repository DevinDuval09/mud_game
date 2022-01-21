from mongo import mongo
from ..python_classes.Character import *

'''
ObjectManager is here to track the state of active objects on the server.
'''
class ServerStateManager:

    def __init__(self):
        self.active_characters = []
        self.active_rooms=[]

    def create_character(self, from_server:bool, id:int=None):
        if(from_server):
            #pull a character from the server
            new_character = Character.fromId(id)
            self.active_characters.append(new_character)
        else:
            #make a brand new character and save it to the db
            pass

    def create_item(self, name:str):
        with mongo:
            #create the item
            pass

    def create_room(self, id:int):
        with mongo:
            #create room
            pass