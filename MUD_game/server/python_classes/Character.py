from math import ceil

from MUD_game.server.python_classes.Skills import EquipmentClasses, EquipmentTypes, Skills
'''Base class for all characters'''
#TODO: redo skills. Skills = standard DnD skills from Skills.py
# proficiencies = general and specific proficiencies from Skills.py
class Character:
    @classmethod
    def createNew(cls, name):
        pass

    @classmethod
    def fromId(cls, name):
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
        inventory = [], #holds inventory objects
        equipment = {}, #key: equipment slot value: equipment object
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

    def save(self):
        pass

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
