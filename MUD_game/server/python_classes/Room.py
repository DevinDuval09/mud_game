from os import stat
from typing import Dict
from .Items import *


class Room(object):

    def __init__(self, number, description, inventory:int=[], characters:str=[], exits:Dict[str,int]={}):
        self.number = number
        self._description = description
        self.inventory = inventory
        self.characters = characters
        self.exits = exits

    def description(self):
        """Provide description of room along with any a list of interactable items"""
        desc = self._description
        if self.inventory:
            desc += f'\nIn the room you see a {" ".join([item.description() for item in self.inventory])}.'
        if self.characters:
            desc += f"\nStanding in the room you see {[character.name for character in self.characters]}."

        if self.exits.keys():
            desc += f"\n There are exits to the {self.exits.keys()}."
        return desc
