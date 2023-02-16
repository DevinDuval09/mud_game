from .mongo import mongo
from ..python_classes.Room import Room
from ..python_classes.Items import *

'''
    Provides a cli commands to create various objects and save them to server
'''

def create_room():
    #provide command line command to create a new room
    description = input("enter room description:")
    exit_keys = input("Enter comma delimited list of exits with no spaces:").split(",")
    exit_dict = {}
    for direction in exit_keys:
        #room numbers do not have to exist in db to be added
        room_number = input(f"Enter adjacent room number for {direction} exit:")
        exit_dict[direction] = room_number
    inventory_list = input("Enter comma delimited list of item numbers:").split(",")
    room_num = ''
    with mongo:
        #items have to exist in the db to be attached to room
        room_num = mongo.db["Rooms"].count() + 1
        collection = mongo.db["Items"]
        for item_num in inventory_list:
            item = collection.find_one({'number': item_num})
            if item is None:
                print(f"{item_num} does not exist. Removing from inventory")
                inventory_list.remove(item_num)
        
    room = Room(room_num, description, exits=exit_dict)
    if len(inventory_list) > 0:
        #TODO: update room.save to attach inventory numbers instead of objects
        room.inventory = inventory_list
    room.save()

def create_item():
    description = input("Enter a description:")
    stat_dict = {}
    for stat in stats_list: #stats_list is defined in Items.py
        stat_dict[stat] = input(f"Enter value to add to {stat}:")
    item_type = input(f"What type of item is this? Select from: {item_types}")
    new_item = ''
    with mongo:
        id = mongo.db["Items"].count() + 1
        if item_type.lower() == "item":
            new_item = Item(id, description, **stat_dict)
        elif item_type.lower() == "container":
            inventory = input("Enter comma delimited list of object numbers:").split(",")
            for number in inventory:
                query = mongo.db["Items"].find_one({"number": number})
                if not query:
                    print(f"{number} does not exist. Removing from inventory.")
                    inventory.remove(number)
            new_item = Container(id, description, inventory_items=inventory, **stat_dict)
        elif item_type.lower() == "equipment":
            slot = input("Enter equipment slot:")
            skill = input("Enter associated skill:")
            new_item = Equipment(id, description, slot, associated_skill=skill, **stat_dict)
        elif item_type.lower() == "book":
            print("Not implemented")
            return
        else:
            print(f"{item_type} does not exist.")
            return
        new_item.save()

def create_character(character_name, password, **kwargs):
    with mongo:
        #check that character name doesn't exist
        #create character
        #save character
        pass

def verify_password(character_name, password):
    with mongo:
        #get character password
        doc = mongo.Players.find_one({"username": character_name})
        if doc and password == doc["password"]:
            return True
        return False

def character_exists(character_name):
    with mongo:
        existing_character = mongo.Players.find_one({"name": character_name.lower().capitalize()})
        if existing_character:
            return True
        return False

