from math import ceil
from Character import Character
class Rogue(Character):
    def __init__(self, expertise: list, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expertise = []
        self.number_sneak_attack_dice = ceil(self.level / 2)

    def quick(self): #cunning action
        pass

    def dodge(self):
        pass
