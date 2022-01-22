"""track item information"""
#from logger import logger

# TODO: passive vs active skills
from types import MethodType
from ..utils.mongo import mongo

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
        active_skills=[],
        passive_skills=[],
        proficiency_skills={},
        **stats,
    ):
        self.number = id
        self._description = description
        self.active_skills = active_skills
        self.proficiency_skills = proficiency_skills
        self.passive_skills = passive_skills
        for key, value in stats.items():
            if key.lower() != "inventory_items":
                setattr(self, key, value)

    def description(self):
        return f"a {self._description}."

    def save(self):
        with mongo:
            collection = mongo.db["Items"]
            save_dict = {
                "number": self.number,
                "description": self._description,
                "active_skills": [skill.__name__ for skill in self.active_skills],
                "passive_skills": [skill.__name__ for skill in self.passive_skills],
                "proficiency_skills": self.proficiency_skills,
            }
            for stat in stats_list:
                if stat in dir(self):
                    save_dict[stat] = getattr(self, stat)
            update = collection.find_one({"number": self.number})
            save_dict["item_type"] = type(self).__name__
            if update:
                collection.replace_one({"number": self.number}, save_dict)
            else:
                collection.insert_one(save_dict)


class Container(Item):
    def __init__(
        self, id, description, active_skills=[], proficiency_skills={}, **stats
    ):
        super().__init__(
            id,
            description,
            active_skills=active_skills,
            proficiency_skills=proficiency_skills,
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
        id,
        description,
        slot,
        associated_skill=None,
        active_skills=[],
        proficiency_skills={},
        **stats,
    ):
        super().__init__(
            id,
            description,
            active_skills=active_skills,
            proficiency_skills=proficiency_skills,
            **stats,
        )
        self.slot = slot
        self.associated_skill = associated_skill


class Book(Item):
    def __init__(
        self,
        id,
        description,
        effect=[None],
        active_skills=[],
        passive_skills=[],
        proficiency_skills=[],
        **stats,
    ):
        super().__init__(
            id,
            description,
            active_skills=active_skills,
            passive_skills=passive_skills,
            proficiency_skills=proficiency_skills,
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
                elif effect == "passive_skills":
#                    logger.info(
#                        "Adding these passive skills to player: ".format(
#                            *self.passive_skills
#                        )
#                    )
                    for skill in self.passive_skills:
                        if skill not in player.passive_skills:
                            message += (
                                f"suddenly understand the art of {skill.__name__}"
                            )
                            player.passive_skills.append(skill)
                elif effect == "active_skills":
#                    logger.info(
#                        "Adding these active skills to player: ".format(
#                            *self.active_skills
#                        )
#                    )
                    for skill in self.active_skills:
                        if skill.__name__ not in dir(player):
                            message += f"think you can now {skill.__name__}"
                            setattr(player, skill.__name__, MethodType(skill, player))
                            print(getattr(player, skill.__name__))
                elif effect == "proficiency_skills":
#                    logger.info(
#                        "Adding these proficiency skills: ".format(
#                            *self.proficiency_skills
#                        )
#                    )
                    for skill, rating in self.proficiency_skills.items():
                        print("skill: ", skill)
                        print("rating: ", rating)
                        message += f"gain a better understanding of {skill} usage"
                        if skill in player.proficiency_skills.keys():
                            player.proficiency_skills[skill] += rating
                        else:
                            player.proficiency_skills[skill] = rating
                else:
                    message += "realize it is gibberish"
            else:
#                logger.info("No effects added to player.")
                message += "think it is a bit of a bore"
            message += "."
        return message
