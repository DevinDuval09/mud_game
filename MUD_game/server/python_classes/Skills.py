'''Provides enums for skills'''
from enum import Enum
from .Character import Character

'''General skills'''
class Skills(Enum):
    #strength skills
    ATHLETICS = 0
    #dexterity skills
    ACROBATICS = 1
    SLEIGHT_OF_HAND = 2
    STEALTH = 3
    #intelligence skills
    ARCANA = 4
    HISTORY = 5
    INVESTIGATION = 6
    NATURE = 7
    RELIGION = 8
    #wisdom skills
    ANIMAL_HANDLING = 9
    INSIGHT = 10
    MEDICINE = 11
    PERCEPTION = 12
    SURVIVAL = 13
    #charisma skills
    DECEPTION = 14
    INTIMIDATION = 15
    PERFORMANCE = 16
    PERSUATION = 17

    def get_stat(self):
        if self == 0:
            return "strength"
        elif self < 4:
            return "dexterity"
        elif self < 9:
            return "intelligence"
        elif self < 14:
            return "wisdom"
        elif self < 18:
            return "charisma"
        else:
            print(f"{self} not implemented")

'''Proficiency with armor and weapon classes and misc tool sets'''
class EquipmentClasses(Enum):
    SIMPLE_WEAPONS = 0
    MARTIAL_WEAPONS = 1
    LIGHT_ARMOR = 2
    MEDIUM_ARMOR = 3
    HEAVY_ARMOR = 4
    SHIELDS = 5
    THIEVES_TOOLS = 6
    SMITH_TOOLS = 7
    LEATHER_TOOLS = 8
    FORGERY_TOOLS = 9
    MAKEUP_TOOLS = 10

'''Specific equipment types'''
class EquipmentTypes(Enum):
    SHORT_SWORD = 0
    LONG_SWORD = 1
    GREAT_SWORD = 2
    HAND_AXE = 3
    BATTLE_AXE = 4
    GREAT_AXE = 5
    LIGHT_HAMMER = 6
    WAR_HAMMER = 7
    SHORT_BOW = 8
    LONG_BOW = 9
    HAND_CROSSBOW = 10
    LIGHT_CROSSBOW = 11
    HEAVY_CROSSBOW = 12
    DAGGERS = 13
    STAFFS = 14
    


