from .mongo import mongo
from ..python_classes import *

'''
    Wrapper class for specific database interfaces.
    Required interface methods:
    **get_xxx**
        The get methods all retrieve the necessary data from the database and
        return an existing persistant object or throw an error
    -get_character
    -get_item
    -get_room
    -get_skill

    **save_xxx**
        The save methods all take an existing object and save it to the database
    -save_character
    -save_item
    -save_room
    -save_skill

    **verify_xxx**
        The verify methods all ensure that an object with the given properties exists
    -verify_character
    -verify_item
    -verify_room
    -verify_skill

    The interface is saved as DatabaseConnect.connection, and the connection will invoke the above functions
    as appropriate
'''
class DatabaseConnect:
    def __init__(self, interface=mongo):
        self.connection = interface
    def save_character(self, character):
        self.connnection.save_character(character)
     