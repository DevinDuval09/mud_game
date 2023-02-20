from .Skills import *
from .Character import Character
from .Character import EquipmentSlots
from .Items import create_item_fromId
#TODO: skills and proficiencies aren't saving correctly
class Fighter(Character):

    def __init__(self, style, *args, **kwargs):
        self.type = "Fighter"
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

    def heal(self):
        pass

    def surge(self):
        pass

    def resist(self):
        pass