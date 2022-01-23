from Skills import *
from Character import Character
class Fighter(Character):
    def __init__(self, style, *args, **kwargs):
        super.__init__(general_proficienes=[EquipmentClasses.SIMPLE_WEAPONS,
                                            EquipmentClasses.MARTIAL_WEAPONS,
                                            EquipmentClasses.LIGHT_ARMOR,
                                            EquipmentClasses.MEDIUM_ARMOR,
                                            EquipmentClasses.HEAVY_ARMOR,
                                            EquipmentClasses.SHIELDS],
                                             *args,
                                             **kwargs)
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