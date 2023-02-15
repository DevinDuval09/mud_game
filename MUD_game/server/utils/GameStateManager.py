from .ObjectGenerator import create_character, verify_password
class GameStateManager:
    _STATES = ["LOGGED_OUT", "ACTIVE", "CHARACTER_CREATION"]
    def __init__(self):
        self._users = {}
    def change_state(self, user, state):
        if state.upper() not in GameStateManager._STATES:
            raise TypeError(f"{state} is not a valid state.")
        self._users[user] = state
    def users(self):
        return self._users.keys()
    def add_user(self, user):
        if user in self._users.keys():
            raise KeyError(f"{user} is already in GameStateManager")
        self._users[user] = "LOGGED_OUT"
    def get_status(self, user):
        if user not in self._users.keys():
            raise KeyError(f"{user} is not in GameStateManager")
        return self._users[user]
    def login(self, character, password):
        #hash password
        with mongo:
            #get character and password and verify password
            #if password matches, toggle status to Active
            pass
    def create_character(self, character, password, **kwargs):
        #hash password
        hashed = None
        create_character(character, hashed, **kwargs)