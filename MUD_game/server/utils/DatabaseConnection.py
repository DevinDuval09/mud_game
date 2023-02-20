from .MongoConnection import MongoConnection
from ..python_classes import *

'''
    Wrapper class for specific database interfaces.
    Required interface methods:
    __enter__ -allows database connection to be used as a context manager
    __exit__ -closes database connection when context it exited
    connect - connect to database outside of a context manager
    close - closes connection outside of a context manager
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
    def __init__(self, host:str, port:int, db_name:str, table_names:list, *args, interface=MongoConnection, **kwargs):
        self.connection = interface(host, port, db_name, table_names)
    def save_character(self, character):
        self.connection.save_character(character)
     