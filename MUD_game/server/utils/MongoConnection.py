"""Provides mongodb interface for objects"""
import pymongo as pm


class MongoConnection:
    """mongodb connection"""

    def __init__(
        self, host="127.0.0.1", port=27017, db_name=None, related_collections=[]
    ):
        """
        set default host to not local computer
        """
        self.host = host
        self.port = port
        self.connection = None
        self.db = None
        self._db_name = db_name
        self._collections = related_collections
        for col in related_collections:
            setattr(self, f"{col}", None)

    def __enter__(self):
        """
        provide context manager for connection
        """
        self.connection = pm.MongoClient(self.host, self.port)
        self.db = self.connection[self._db_name]
        for col in self._collections:
            setattr(self, f"{col}", self.db[col])

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.db = None
        for col in self._collections:
            setattr(self, f"{col}", None)
        self.connection.close()

    def connect(self):
        """
        non context manager for connection
        """

        self.__enter__()
        return True

    def close(self, *args):
        """
        non context manager to close connection
        """
        self.connection.close()
        return True

    def _verify_docs(self, collection, **kwargs):
        """verify that a doc exists meeting each criteria"""
        with self:
            col = self.db[collection]
            for kw, arg in kwargs.items():
                query = {kw: arg}
                record = col.find_one(query)
                if not record:
                    return False
        return True

    @staticmethod
    def _create_dict(update=True, **kwargs):
        """create an update statement from given kwargs"""
        if update:
            return {
                "$set": {kw: arg for (kw, arg) in kwargs.items() if arg is not None}
            }
        return {kw: arg for (kw, arg) in kwargs.items() if arg is not None}

    def save_item(self, item):
        with mongo:
            collection = mongo.db["Items"]
            save_dict = {
                "number": self.number,
                "description": self._description,
                "skills": [skill.value() for skill in self.skills],
                "general_proficiencies": [skill.value() for skill in self.general_proficiencies],
                "specific_proficiencies": [skill.value() for skill in self.specific_proficiences],
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

    def save_container(self, container):
        super().save()
        with mongo:
            inventory = [item.number for item in self.inventory]
            mongo.db["Items"].update_one({"number": self.number}, {"$set": {"inventory": inventory}})

    def save_equipment(self, equipment):
        super().save()
        slot_update = {"slot": self.slot.value}
        equipment_type_update = {"equipment_type": self.equipment_type.value}
        equipment_class_update = {"equipment_class": self.equipment_class.value}
        updates = [slot_update, equipment_class_update, equipment_type_update]
        with mongo:
            for update in updates:
                mongo.db["Items"].update_one({"number": self.number}, {"$set": update})

    def save_room(self, room):
        room_dict = {
            "number": self.number,
            "description": self._description,
            "inventory": [item.number for item in self.inventory],
            "characters": [NPC.name for NPC in self.characters],
            "exits": {
                direction: room_number
                for (direction, room_number) in self.exits.items()
            },
        }
        with mongo:
            collection = mongo.db["Rooms"]
            query = collection.find({"number": self.number})
            if query.count() == 1:
                collection.replace_one({"number": self.number}, room_dict)
            if query.count() == 0:
                collection.insert_one({**room_dict})

    def _save_object(self, collection, id_name, id_val, **kwargs):
        with self:
            collection = self[collection]
            existing_doc = collection.find_one({id_name: id_val})
            if existing_doc:
                collection.replace_one({id_name: id_val}, kwargs)
            else:
                collection.insert_one({**kwargs})

    def save_character(self, character):
        self._save_object("Player", "name", character.name, character)





mongo = MongoConnection(
    db_name="Realms_MUD", related_collections=["Players", "Items", "Rooms", "Npcs"]
)
