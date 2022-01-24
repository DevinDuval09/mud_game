'''Provides enums for skills'''
from enum import Enum
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
        if self.value == 0:
            return "strength"
        elif self.value < 4:
            return "dexterity"
        elif self.value < 9:
            return "intelligence"
        elif self.value < 14:
            return "wisdom"
        elif self.value < 18:
            return "charisma"
        else:
            print(f"{self} not implemented")

'''Proficiency with armor and weapon classes and misc tool sets'''
class EquipmentClasses(Enum):
    SHIELDS = 0
    SIMPLE_WEAPONS = 1
    MARTIAL_WEAPONS = 2
    LIGHT_ARMOR = 3
    MEDIUM_ARMOR = 4
    HEAVY_ARMOR = 5
    THIEVES_TOOLS = 6
    SMITH_TOOLS = 7
    LEATHER_TOOLS = 8
    FORGERY_TOOLS = 9
    MAKEUP_TOOLS = 10

'''Specific equipment types'''
class EquipmentTypes(Enum):
    SHIELDS = 0
    SHORT_SWORD = 1
    LONG_SWORD = 2
    GREAT_SWORD = 3
    HAND_AXE = 4
    BATTLE_AXE = 5
    GREAT_AXE = 6
    LIGHT_HAMMER = 7
    WAR_HAMMER = 8
    SHORT_BOW = 9
    LONG_BOW = 10
    HAND_CROSSBOW = 11
    LIGHT_CROSSBOW = 12
    HEAVY_CROSSBOW = 13
    DAGGERS = 14
    STAFFS = 15
    RAPIERS = 16
    DARTS = 17
    SLINGS = 18
class EquipmentSlots(Enum):
    HEAD = 0
    CHEST = 1
    ARMS = 2
    GLOVES = 3
    MAIN_HAND = 4
    OFF_HAND = 5
    BELT = 6
    LEGS = 7
    FEET = 8
    CLOAK = 9
    BACK = 10

    


