from .MongoConnection import MongoConnection
from ..python_classes import *
import hashlib
import random
import string

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
    app_iterations = 100
    def __init__(self, host:str, port:int, db_name:str, table_names:list, *args, interface=MongoConnection, **kwargs):
        self.connection = interface(host, port, db_name, table_names)
    def _salt_generator(self, size=None):
        if not size:
            size = random.randint(5, 12)
        characters = string.ascii_letters + string.digits + string.punctuation
        return ''.join(random.choice(characters) for i in range(size))

    def _hasher(self, password, salt):
        return hashlib.pbkdf2_hmac("sha256", password.encode(), salt, DatabaseConnect.app_iterations)

    def save_character(self, character, include_password=False):
        self.connection.save_character(character, include_password)
    def verify_character(self, name):
        return self.connection.verify_character(name)
    def create_new_character(self, character, password):
        salt = self._salt_generator().encode()
        db_password = self._hasher(password, salt)
        character.salt = salt
        character.password = db_password
        self.save_character(character, True)
    def verify_password(self, name, password):
        user_dict = self.connection.get_character(name)
        print(user_dict)
        print(f"user: {user_dict['name']} password: {user_dict['password']} provided password: {password}")
        #problem is how to handle getting the salt to verify the password
        if self._hasher(password) != user_dict["password"]:
            return False
        return True
    def get_room(self, room_number):
        return self.connection.get_room(room_number)
