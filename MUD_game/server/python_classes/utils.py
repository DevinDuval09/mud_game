from random import randint
from ..utils.mongo import mongo
from .Character import Character
from .Fighter import Fighter
from .Rogue import Rogue
from .Wizard import Wizard
from .Items import *

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


