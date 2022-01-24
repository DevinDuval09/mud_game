from math import ceil, floor
from enum import Enum
from .Items import Equipment, Item
from .Skills import EquipmentSlots, EquipmentClasses, EquipmentTypes, Skills
'''Base class for all characters'''
stats = ["strength", "dexterity", "constitution", "intelligence", "wisdom", "charisma", "AC"]
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
        self.equipment = {}
        for slot in EquipmentSlots:
            if slot not in equipment.keys() or equipment[slot] is None:
                self.equipment[slot] = None
            else:
                self.equipment[slot] = equipment[slot]
        self.AC = self._calc_AC()
        self.hit_dice = hit_dice
        self.level = level
        self.proficiency_bonus = ceil(self.level / 4) + 1
        self.general_proficiencies = general_prof #list of enums from Skills.py
        self.specific_proficiencies = specific_prof
        self.skills = skills
    
    def _calc_stat_bonus(self, stat: str):
        return floor((getattr(self, stat) - 10) / 2)
    
    def _calc_AC(self):
        class ARMOR_TYPE(Enum):
            UNARMORED = 0
            LIGHT_ARMOR = 1
            MEDIUM_ARMOR = 2
            HEAVY_ARMOR = 3
        armor = ARMOR_TYPE.UNARMORED
        armor_score = 0
        for _, item in self.equipment.items():
            if "AC" in dir(item):
                armor_score += getattr(item, "AC")
            if not item:
                continue
            if item.equipment_class == EquipmentClasses.LIGHT_ARMOR:
                armor = ARMOR_TYPE.LIGHT_ARMOR
            elif item.equipment_class == EquipmentClasses.MEDIUM_ARMOR:
                armor = ARMOR_TYPE.MEDIUM_ARMOR
            elif item.equipment_class == EquipmentClasses.HEAVY_ARMOR:
                armor = ARMOR_TYPE.HEAVY_ARMOR
        if armor == ARMOR_TYPE.UNARMORED:
            return armor_score + self._calc_stat_bonus("dexterity") + 10
        if armor == ARMOR_TYPE.LIGHT_ARMOR:
            return armor_score + self._calc_stat_bonus("dexterity")
        if armor == ARMOR_TYPE.MEDIUM_ARMOR:
            return armor_score + min(self._calc_stat_bonus("dexterity"), 2)
        if armor == ARMOR_TYPE.HEAVY_ARMOR:
            return armor_score
            

    def save(self) -> dict:
        save_dict = {"name": self.name}
        equipment_dict = {}
        for slot, item in self.equipment.items():
            if item:
                equipment_dict[str(slot.value)] = item.number
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


    
    def grab(self, item: Item):
        #take item out of current room and put into inventory
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

    def equip(self, item: str) -> str:
        if item not in self.inventory.keys():
            return f"You do not have {item} in your inventory."
        item_object = self.inventory.pop(item)
        if self.equipment[item_object.slot] is not None:
            return f"You have to remove {self.equipment[item_object.slot]} first."
        for skill in item_object.skills:
            self.skills.append(skill)
        for prof in item_object.general_proficiencies:
            self.general_proficiencies.append(prof)
        for prof in item_object.specific_proficiencies:
            self.specific_proficiencies.append(prof)
        for stat in dir(item_object):
            if stat in stats:
                current_stat = getattr(self, stat)
                setattr(self, stat, current_stat + getattr(item_object, stat))
        self.equipment[item_object.slot] = item_object
        self.AC = self._calc_AC()
        if item_object.slot == EquipmentSlots.HEAD:
            return f"You equip the {item_object._description} on your head."
        elif item_object.slot == EquipmentSlots.CHEST:
            return f"You equip the {item_object._description} on your chest."
        elif item_object.slot == EquipmentSlots.MAIN_HAND:
            return f"You grab the {item_object._description} firmly in your hand."
        elif item_object.slot == EquipmentSlots.OFF_HAND:
            return f"You hold the {item_object._description} in your off hand."
        elif item_object.slot == EquipmentSlots.LEGS:
            return f"You pull the {item_object._description} over your legs."
        elif item_object.slot == EquipmentSlots.FEET:
            return f"You strap the {item_object._description} to your feet."
        else:
            return f"{item_object.slot} not implemented."
        

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

    def palm(self):
        #sneaky grab
        pass

    def steal(self):
        #palm something off another NPC or player
        pass
