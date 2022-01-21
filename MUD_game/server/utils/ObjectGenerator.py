from .mongo import mongo
from MUD_game.server.python_classes.Room import Room

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
