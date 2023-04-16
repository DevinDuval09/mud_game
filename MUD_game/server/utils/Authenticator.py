from .DatabaseConnection import DatabaseConnect
from .GameStateManager import GameStateManager
from http.cookies import SimpleCookie
import datetime as dt

'''
Class for authenticating players. This class will:
    -Handle logins by authenticating the provided password against the database
    -Give out session id's
    -manage session id's
    -when a player is authenticated and logged in, pass their request back to the game_server
'''
class Authenticator:
    def __init__(self,
                database_connection: DatabaseConnect,
                state_manager: GameStateManager,
                ):
        self.db = database_connection
        self.state_manager = state_manager
        self.sessions = {}
    def handle_login(self, request):
        pass
    '''
    Checks that the given cookies have all the proper credentials
    '''
    def is_authenticated(self, cookies:dict) -> bool:
        print(f"Authenticator received cookies: {cookies}")
        cookie_keys = cookies.keys()
        #if user in self.server.sessions, validate session id
        if ("user" not in cookie_keys) or ("session" not in cookie_keys):
            return False
        user = cookies["user"]
        session = cookies["session"]
        if user not in self.sessions.keys():
            return False
        if session != self.sessions[user]:
            return False
        return True

    def valid_credentials(self, data):
        print(f"body sent to Authenticator: {data}")
        user = data["username"]
        password = data["password"]
        return self.db.verify_password(user, password)
    def assign_session(self):
        pass
    def get_credentials(self, user):
        biscuits = SimpleCookie()
        biscuits["user"] = user
        session_id = self.db._salt_generator(12)
        biscuits["session"] = session_id
        expiration = dt.datetime.utcnow() + dt.timedelta(minutes=5)
        biscuits["session"]["expires"] = expiration.strftime("%a, %d %b %Y %H:%M:%S GMT")
        self.state_manager.add_user(user)
        self.state_manager.change_state(user, "ACTIVE")
        self.sessions[user] = session_id
        return biscuits
