from os import stat
from typing import Dict
from ..utils.mongo import mongo
from .Items import *


class Room(object):
    @classmethod
    def fromId(cls, number):
        with mongo as m:
            collection = m.db["Rooms"]
            room_dict = collection.find_one({"number": number})
            return cls(
                room_dict["number"],
                room_dict["description"],
                inventory=[number for number in room_dict["inventory"]],
                characters=[npc for npc in room_dict["characters"]],
            )

    def __init__(self, number, description, inventory:int=[], characters:str=[], exits:Dict[str,int]={}):
        self.number = number
        self._description = description
        if len(inventory) > 0:
            self.inventory = []
            with mongo:
                collection = mongo.db["Items"]
                for number in inventory:
                    #inventory in instance is a collection of Item objects
                    item = collection.find_one({"id": number})
                    if item:
                        if item["item_type"] == "Item":
                            self.inventory.append(Item.fromId(number))
                        elif item["item_type"] == "Container":
                            self.inventory.append(Container.fromId(number))
                        elif item["item_type"] == "Equipment":
                            self.inventory.append(Equipment.fromId(number))
                        elif item["item_type"] == "Book":
                            print("Book not implemented.")
                        else:
                            item_type = item["item_type"]
                            print(f"{item_type} not implemented.")


        self.exits = exits
        self.characters = characters

    def save(self):
        room_dict = {
            "number": self.number,
            "description": self._description,
            "inventory": [item.number for item in self.inventory],
            "characters": [NPC.name for NPC in self.characters],
            "exits": {
                direction: room_number
                for (direction, room_number) in self.exits.items()
            },
        }
        with mongo:
            collection = mongo.db["Rooms"]
            query = collection.find({"number": self.number})
            if query.count() == 1:
                collection.replace_one({"number": self.number}, room_dict)
            if query.count() == 0:
                collection.insert_one({**room_dict})

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
