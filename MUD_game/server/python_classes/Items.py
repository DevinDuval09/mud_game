"""track item information"""
#from logger import logger

# TODO: each Item subclass needs a unique fromId class method 
from types import MethodType
from .Skills import *

stats_list = [
    "strength",
    "dexterity",
    "constitution",
    "intelligence",
    "wisdom",
    "charisma",
    "AC", #armor class
]

item_types = [
    "Item",
    "Container",
    "Equipment",
    "Book"
]


class Item(object):
    def __init__(
        self,
        id,
        description,
        skills=[], #skill enum granted by item
        general_proficiencies=[], #equipment class enums granted by item
        specific_proficiencies=[], #specific equipment enum granted by item
        **stats, #stat increases granted by item
    ):
        self.number = id
        self._description = description
        self.skills = skills
        self.general_proficiencies = general_proficiencies
        self.specific_proficiencies = specific_proficiencies
        for key, value in stats.items():
            if key.lower() != "inventory_items": #guard againt container inventory
                setattr(self, key, value)

    def description(self):
        return f"a {self._description}."


class Container(Item):
    def __init__(
        self, id, description, skills=[], specific_proficiencies={}, **stats
    ):
        super().__init__(
            id,
            description,
            skills=skills,
            specific_proficiencies=specific_proficiencies,
            **stats,
        )
        self._open = False
        self.inventory = []
        if "inventory_items" in stats:
            self.inventory.extend(stats["inventory_items"])

    def description(self):
        if self._open:
            return "an open " + self._description + f" containing {self.inventory}."
        else:
            return f"a {self._description}."

    def open(self):
        self._open = True
        return f"You open the {self._description}. It contains {self.inventory}."

class Equipment(Item):
    def __init__(
        self,
        id: int,
        description: str,
        slot: EquipmentSlots,
        equipment_type: EquipmentTypes=None,
        equipment_class: EquipmentClasses=None,
        **stats,
    ):
        super().__init__(
            id,
            description,
            **stats,
        )
        self.slot = slot
        self.equipment_type=equipment_type
        self.equipment_class=equipment_class

class Book(Item):
    def __init__(
        self,
        id: int,
        description: str,
        effect=[None],
        skills: Skills=[],
        general_proficiencies: EquipmentClasses=[],
        specific_proficiencies: EquipmentTypes=[],
        **stats,
    ):
        super().__init__(
            id,
            description,
            skills=skills,
            general_proficiencies=general_proficiencies,
            specific_proficiencies=specific_proficiencies,
            **stats,
        )
        self.effects = effect

    def reading_effect(self, player) -> str:
        message = "You read the book and "
        for effect in self.effects:
            if effect:
                if effect == "stats":
                    my_stats = [stat for stat in stats_list if stat in dir(self)]
#                    logger.info("Adding following stats to player: %s" % my_stats)
                    my_values = [getattr(self, stat) for stat in my_stats]
                    for stat, value in zip(my_stats, my_values):
                        message += f"feel your {stat} increasing "
                        setattr(player, stat, getattr(player, stat) + value)
                elif effect == "general_proficiencies":
#                    logger.info(
#                        "Adding these passive skills to player: ".format(
#                            *self.general_proficiencies
#                        )
#                    )
                    for skill in self.general_proficiencies:
                        if skill not in player.general_proficiencies:
                            message += (
                                f"suddenly understand the art of {skill.__name__}"
                            )
                            player.general_proficiencies.append(skill)
                elif effect == "skills":
#                    logger.info(
#                        "Adding these active skills to player: ".format(
#                            *self.skills
#                        )
#                    )
                    for skill in self.skills:
                        if skill.__name__ not in dir(player):
                            message += f"think you can now {skill.__name__}"
                            setattr(player, skill.__name__, MethodType(skill, player))
                            print(getattr(player, skill.__name__))
                elif effect == "specific_proficiencies":
#                    logger.info(
#                        "Adding these proficiency skills: ".format(
#                            *self.specific_proficiencies
#                        )
#                    )
                    for skill, rating in self.specific_proficiencies.items():
                        print("skill: ", skill)
                        print("rating: ", rating)
                        message += f"gain a better understanding of {skill} usage"
                        if skill in player.specific_proficiencies.keys():
                            player.specific_proficiencies[skill] += rating
                        else:
                            player.specific_proficiencies[skill] = rating
                else:
                    message += "realize it is gibberish"
            else:
#                logger.info("No effects added to player.")
                message += "think it is a bit of a bore"
            message += "."
        return message
