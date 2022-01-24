from random import randint
from ..utils.mongo import mongo
from Character import Character
from Fighter import Fighter
from Rogue import Rogue
from Wizard import Wizard
from Items import *

def roll_dice(max_value: int) -> int:
    return randint(1, max_value)

def create_character_fromId(name: str) -> Character:
    #get document based on character name and call from Id from appropriate class
    character_class = ''
    class_dict = {"Fighter": Fighter, "Rogue": Rogue, "Wizard": Wizard}
    with mongo:
        doc = mongo.db["Players"].find_one({"name": name})
        if doc:
            character_class = doc["class"]
        else:
            print(f"{name} does not exist in database.")
            return
    return class_dict[character_class].fromId(name)

def create_item_fromId(id: int) -> Item:
    with mongo:
        doc = mongo.db["Items"].find_one({"id": id})
        item_type = doc.pop("item_type", None)
        desc = doc.pop("description", None)
        doc.pop("id", None)
        if item_type == "Equipment":
            slot = doc.pop("slot", None)
            item_skill = doc.pop("specific_skill", None)
            item_class = doc.pop("general_skill", None)
            return Equipment(id,
                            desc,
                            slot,
                            specific_skill=item_skill,
                            general_skill=item_class,
                            **doc)
        elif item_type == "Item":
            return Item(id,
                        desc,
                        **doc)
        elif item_type == "Container":
            pass
        elif item_type == "Book":
            pass
        else:
            print(f"{item_type} not implemented.")

