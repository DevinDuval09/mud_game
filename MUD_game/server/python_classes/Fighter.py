from .Skills import *
from .Character import Character
from .Character import EquipmentSlots
from ..utils.mongo import mongo
from .Items import create_item_fromId
#TODO: skills and proficiencies aren't saving correctly
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
                equipment_dict[EquipmentSlots(slot)] = item
            print(player_doc)
        return cls(
                    player_doc["style"],
                    player_doc["name"],
                    player_doc["room"],
                    player_doc["description"],
                    player_doc["strength"],
                    player_doc["dexterity"],
                    player_doc["constitution"],
                    player_doc["intelligence"],
                    player_doc["wisdom"],
                    player_doc["charisma"],
                    inventory=inventory_dict,
                    equipment=equipment_dict,
                    hit_dice=10,
                    level=player_doc["level"],
                    general_prof=[EquipmentClasses(prof) for prof in player_doc["general proficiencies"]],
                    specific_prof=[EquipmentTypes(prof) for prof in player_doc["specific proficiencies"]],
                    skills=[Skills(num) for num in player_doc["skills"]]
                    )



    def __init__(self, style, *args, **kwargs):
        general_prof = []
        if "general_prof" in kwargs.keys():
            general_prof = kwargs.pop("general_prof")
        else:
            general_prof=[EquipmentClasses.SIMPLE_WEAPONS,
                          EquipmentClasses.MARTIAL_WEAPONS,
                          EquipmentClasses.LIGHT_ARMOR,
                          EquipmentClasses.MEDIUM_ARMOR,
                          EquipmentClasses.HEAVY_ARMOR,
                          EquipmentClasses.SHIELDS]

        super().__init__(general_prof=general_prof, *args, **kwargs)
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
            print(doc)
            if doc:
                update_dict = mongo._create_dict(update=True, **save_dict)
                mongo.db["Players"].update_one({"name": self.name}, update_dict)
            else:
                update_dict = mongo._create_dict(update=False, **save_dict)
                mongo.db["Players"].insert_one(update_dict)

    
    def heal(self):
        pass

    def surge(self):
        pass

    def resist(self):
        pass