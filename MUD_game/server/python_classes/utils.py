from random import randint
from .Character import Character
from .Fighter import Fighter
from .Rogue import Rogue
from .Wizard import Wizard
from .Items import *

def roll_dice(max_value: int) -> int:
    return randint(1, max_value)
