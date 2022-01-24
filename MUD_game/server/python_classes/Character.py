from math import ceil
from enum import Enum
from .Items import Equipment, Item
from .Skills import EquipmentSlots, EquipmentClasses, EquipmentTypes, Skills
'''Base class for all characters'''
stats = ["strength", "dexterity", "constitution", "intelligence", "wisdom", "charisma"]
class Character:
    @classmethod
    def createNew(cls, name):
        pass

    def __init__(
        self,
        name: str,
        spawn_room_number: int = 0,
        desc: str = "",
        STR: int = 0,
        DEX: int = 0,
        CON: int = 0,
        INT: int = 0,
        WIS: int = 0,
        CHA: int = 0,
        inventory: dict = {}, #holds inventory objects. key: item name, value item object
        equipment: dict = {}, #key: equipment slot enum: equipment object
        hit_dice: int = 6,
        level: int = 1,
        general_prof: EquipmentClasses = [],
        specific_prof: EquipmentTypes = [],
        skills: Skills = [],
    *args,
    **kwargs):
        self.name = name
        self.spawn_room = spawn_room_number
        self.description = desc
        self.strength = STR
        self.dexterity = DEX
        self.constitution = CON
        self.intelligence = INT
        self.wisdom = WIS
        self.charisma = CHA
        self.inventory = inventory
        self.equipment = equipment
        self.hit_dice = hit_dice
        self.level = level
        self.proficiency_bonus = ceil(self.level / 4) + 1
        self.general_proficiencies = general_prof #list of enums from Skills.py
        self.specific_proficiencies = specific_prof
        self.skills = skills

    def save(self) -> dict:
        save_dict = {"name": self.name}
        equipment_dict = {}
        for slot, item in self.equipment.values():
            if item:
                equipment_dict[slot.value] = item.id
        save_dict["equipment"] = equipment_dict
        save_dict["inventory"] = [item.id for item in self.inventory.items()]
        for stat in stats:
            save_dict[stat] = getattr(self, stat)
        save_dict["room"] = self.spawn_room
        save_dict["description"] = self.description
        save_dict["level"] = self.level
        save_dict["general proficiencies"] = [prof.value for prof in self.general_proficiencies]
        save_dict["specific proficiencies"] = [prof.value for prof in self.specific_proficiencies]
        save_dict["skills"] = [skill.value for skill in self.skills]

        return save_dict


    
    def grab(self):
        pass

    def drop(self):
        pass

    def move(self):
        pass

    def look(self):
        pass

    def say(self):
        pass

    def open(self):
        pass

    def equip(self):
        pass

    def remove(self):
        pass

    def read(self):
        pass

    def attack(self):
        pass

    def hide(self):
        pass

    def disengage(self):
        pass

    def dash(self):
        pass

    def hide(self):
        pass

    def sneak(self):
        pass
