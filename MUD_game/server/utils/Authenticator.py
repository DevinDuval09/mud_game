from .DatabaseConnection import DatabaseConnect
from .GameStateManager import GameStateManager

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
            cookie_keys = cookies.keys()
            #if user in self.server.sessions, validate session id
            if ("user" not in cookie_keys) or ("session" not in cookie_keys):
                return False
            user = cookies["user"]
            session = cookies["session"]
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
    def generate_cookies(self):
        pass