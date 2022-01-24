from Skills import *
from Character import Character
from ..utils.mongo import mongo
from utils import create_item_fromId
class Fighter(Character):
    @classmethod
    def fromId(cls, name: str):
        player_doc = ''
        inventory_dict = {}
        equipment_dict = {}
        with mongo:
            player_doc = mongo.db["Players"].find_one({"name": name})
            #inventory_keys = player_doc["inventory"]
            for number in player_doc["inventory"]:
                item = create_item_fromId(number)
                inventory_dict[item.description] = item
            for slot, number in player_doc["equipment"]:
                item = create_item_fromId(number)
                equipment_dict[slot] = item
        return cls(
                    player_doc["name"],
                    player_doc["room"],
                    player_doc["description"],
                    player_doc["strength"],
                    player_doc["dexterity"],
                    player_doc["constitution"],
                    player_doc["intelligence"],
                    player_doc["wisdom"],
                    player_doc["charisma"],
                    style=player_doc["style"],
                    inventory=inventory_dict,
                    equipment=equipment_dict,
                    hit_dice=10,
                    level=player_doc["level"],
                    general_prof=player_doc["general_proficiencies"],
                    specific_prof=player_doc["specific_proficiencies"],
                    skills=player_doc["skills"]
                    )



    def __init__(self, style, *args, **kwargs):
        super.__init__(general_proficienes=[EquipmentClasses.SIMPLE_WEAPONS,
                                            EquipmentClasses.MARTIAL_WEAPONS,
                                            EquipmentClasses.LIGHT_ARMOR,
                                            EquipmentClasses.MEDIUM_ARMOR,
                                            EquipmentClasses.HEAVY_ARMOR,
                                            EquipmentClasses.SHIELDS],
                                             *args,
                                             **kwargs)
        self.style = style
        if (style == "archery"):
            pass
        elif (style == "dueling"):
            pass
        elif (style == "defense"):
            pass
        elif (style == "gw_fighting"):
            pass
    
    def save(self):
        save_dict = super().save()
        save_dict["style"] = self.style
        save_dict["character type"] = "Fighter"
        with mongo:
            doc = mongo.db["Players"].find_one({"name": self.name})
            if doc:
                update_dict = mongo._create_dict(update=True, **save_dict)
                mongo.db["Players"].update_one({"name": save_dict["name"]}, **update_dict)
            else:
                update_dict = mongo._create_dict(update=False, **save_dict)
                mongo.db["Players"].insert_one(update_dict)

    
    def heal(self):
        pass

    def surge(self):
        pass

    def resist(self):
        pass