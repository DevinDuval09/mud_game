from math import ceil
from Character import Character
from Skills import *
class Rogue(Character):
    def __init__(self, expertise: list, *args, **kwargs):
        super().__init__(general_prof=[EquipmentClasses.LIGHT_ARMOR,
                                       EquipmentClasses.SIMPLE_WEAPONS],
                        specific_prof=[EquipmentTypes.HAND_CROSSBOW,
                                       EquipmentTypes.SHORT_SWORD,
                                       EquipmentTypes.LONG_SWORD,
                                       EquipmentTypes.RAPIERS]
                        *args, **kwargs)
        self.expertise = [] #Skills enums
        self.number_sneak_attack_dice = ceil(self.level / 2)

    def quick(self): #cunning action
        pass

    def dodge(self):
        pass
