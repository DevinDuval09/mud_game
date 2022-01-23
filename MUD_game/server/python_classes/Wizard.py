from Character import Character
from Skills import *
class Wizard(Character):
    def __init__(self, *args, **kwargs):
        super().__init__(specific_prof=[EquipmentTypes.DAGGERS,
                                        EquipmentTypes.STAFFS,
                                        EquipmentTypes.SLINGS,
                                        EquipmentTypes.LIGHT_CROSSBOW,
                                        EquipmentTypes.DARTS],
                         *args, **kwargs)
    
    def recover(self):
        pass
    
    def cast(self):
        pass
