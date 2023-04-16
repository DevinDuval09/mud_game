import os.path
import socketserver as sserv
import json
import re
from http import cookies
from .utils.MudGameEngine import MudGameEngine
from .utils.GameStateManager import GameStateManager
from .utils.DatabaseConnection import DatabaseConnect
from .utils.MongoConnection import MongoConnection
from .utils.Authenticator import Authenticator

class Router(sserv.StreamRequestHandler):
    _http_codes = {
        200: "OK",
        201: "Created",
        308: "Permanent Redirect",
        404: "Not Found"
    }
    def _create_header(self, http_code:int, file_path:str, content_type=None, _cookies:cookies.SimpleCookie=None, **kwargs)->str:
        header = "HTTP/1.1 "
        if not content_type:
            content_type = "text/" + file_path[file_path.rfind(".") + 1: len(file_path)]
        header = header + f'{http_code} {Router._http_codes[http_code]}\r\n'
        header = header + f'Content-Type: {content_type}\r\n'
        header = header + f'Connection: keep-alive\r\n'
        if kwargs:
            for key, val in kwargs.items():
                header = header + f"{key}: {val}\r\n"
        if _cookies:
            header = header + _cookies.output()
        header = header + "\r\n"
        #print("printing header:\n\n")
        #print(header)

        return header

    def _send_file(self, header:str, filepath:str, _cookies:cookies.SimpleCookie=None, **kwargs)->None:
        response = ''
        encoded_lines = ''
        if not header:
            header = self._create_header(200, filepath, _cookies, **kwargs)
        if filepath:
            dir = os.path.abspath(os.path.dirname(__file__))
            file_path = os.path.join(dir, filepath)
            with open(file_path) as file:
                lines = file.readlines()
                encoded_lines = "".join(lines)
        response = (header +  encoded_lines + '\r\n').encode("utf-8")
        self.request.sendall(response)
        #print(response.decode("utf-8"))

    def _send_json(self, dict)->None:
        header = self._create_header(200, None, "application/json")
        print(f"Sending json of: {dict}")
        response = (header + json.dumps(dict) + '\r\n').encode("utf-8")
        self.request.sendall(response)

    def process_command(self, command):
        print("processing command " + command)
        updated_state = self.engine.execute_player_input(command)
        response = self._create_header(200, None, "json") + json.dumps(updated_state) + "\r\n"
        print(response)
        response = response.encode("utf-8")
        self.request.sendall(response)

    def handle_get(self, url):
        dir = os.path.abspath(os.path.dirname(__file__))
        filepath = os.path.join(dir, f"../{url}")
        if (url == "/login"):
            print("Sending login page")
            file_path = "../client/html/login.html"
            header = self._create_header(200, file_path)
            self._send_file(header, file_path)
        elif url == "/" and self.server.server_manager.get_status(self.client_address) == "ACTIVE":
            print("Sending game page")
            file_path = "../index.html"
            header = self._create_header(200, None, "text/html")
            self._send_file(header, filepath)
        elif url == "/character_creation":
            print("Sending character creation page")
            file_path = "../client/html/character_creation.html"
            header = self._create_header(200, file_path)
            self._send_file(header, file_path)
        elif url.find("verify:") > -1:
            print("Verifying name availability")
            _, name = url.split(":")
            response = {"name_available": not self.server.db.verify_character(name.strip())}
            self._send_json(response)
        elif url.find("command:") > -1:
            self.process_command(url[url.find(":") + 1:])
        elif os.path.isfile(f"{filepath}"):
            print(f"Sending {url}")
            file_path = f"../{url}"
            header = self._create_header(200, file_path)
            self._send_file(header, file_path)
    def _read_body(self, size):
        num_bytes = int(size)
        _bytes = self.rfile.read(num_bytes)
        body = _bytes.decode("utf-8")
        return body
    def _split_delineated_kv_pairs(self, pairs, delineator=";"):
        kv_pairs = {}
        split_pairs = pairs.split(delineator)
        for line in split_pairs:
            key, value = line.strip().split("=")
            kv_pairs[key.strip()] = value.strip()
        return kv_pairs

    def _read_headers(self):
        headers = {}
        if self.rfile.readable():
            while True:
                chunk = self.rfile.readline().decode("utf-8")
                #print(f"chunk: {chunk}")
                if len(chunk) > 0 and chunk != '\r\n':
                    header, values = chunk.split(":", 1)
                    if header.strip() == "Cookie":
                        self.biscuits = self._split_delineated_kv_pairs(values)
                    else:
                        headers[header.strip()] = values.strip()
                if chunk == '\r\n':
                    break
        return headers
    
    def _parse_urlencoded_form(self, form_data):
        for key, val in self.headers.items():
            print("Header: " + key + " val: " + val)
        split_data = form_data.split("&")
        form_dict = {}
        for user_input in split_data:
            key, val = user_input.split("=")
            form_dict[key] = val
        return form_dict

    def _parse_multipart_form(self, form_data):
        form_dict = {}
        boundary = self.headers["Content-Type"].split("boundary=")[1].strip()
        chunks = form_data.split(boundary)
        for chunk in chunks:
            #print("chunk\n:" + chunk)
            key_obj = re.search(r'(?<=name=")([a-z]+)(?="\s)', chunk)
            value_obj = re.search(r'(?<=\s)([A-Za-z0-9]+)(?=\s)', chunk)
            if key_obj and value_obj:
                form_dict[key_obj.group()] = value_obj.group()
        return form_dict

    def _parse_form(self, form):
        if self.headers["Content-Type"] == "application/x-www-form-urlencoded":
            return self._parse_urlencoded_form(form)
        elif "multipart/form-data" in self.headers["Content-Type"]:
            return self._parse_multipart_form(form)
        else:
            print(f"Unable to decode Content-Type {self.headers['Content-Type']}")
            return None
    
    def handle_post(self, url):
        if(url == "/character_creation"):
            character_data = self._parse_form(self.body)
            if self.server.db.verify_character(character_data["name"]):
                raise AttributeError(f"{character_data['name']} already exists in database.")
            #have engine create new character
            #engine needs to add starting inventory, equipment, skills, proficiences, e
            new_character = self.server.engine.create_new_character(character_data)
            self.server.db.create_new_character(new_character, character_data["password"])
            #header needs to send character name and session ID cookies
            #character name needs to be stored by GameStateManager
            biscuits = cookies.SimpleCookie()
            biscuits["user"] = new_character.name
            biscuits["session"] = self.server.db._salt_generator(12)
            #update state manager
            self.server.state_manager.add_user(new_character.name)
            self.server.state_manager.change_state(new_character.name, "ACTIVE")
            self._send_file(self._create_header(201, None, "text/html", biscuits, Location="/"), None)

    '''
    First thing that handles a request. It starts by reading it.
    '''
    def handle(self):
        self.biscuits = {}#cookies that will be set in self._read_headers
        self.startline = self.rfile.readline().decode("utf-8")
        self.headers = self._read_headers()
        if "Content-Length" in self.headers.keys():
            self.body = self._read_body(self.headers["Content-Length"])
        else:
            self.body = []
        request = self.startline.split()
        method = request[0]
        url = request[1]
        protocol = request[2]
        print(f"Received {method} request for {url} endpoint.")
        #if request is for a valid file, send the file
        dir = os.path.abspath(os.path.dirname(__file__))
        filepath = os.path.join(dir, f"../{url}")
        if os.path.isfile(f"{filepath}") and method.upper() == "GET":
            print(f"Sending requested file {url}")
            file_path = f"../{url}"
            header = self._create_header(200, file_path)
            self._send_file(header, file_path)
            return
        #authenticate request
        if not self.server.authenticator.is_authenticated(self.biscuits):
            if method.upper() == "GET":
                print(f"Authentication failed; rerouting to login in page.")
                #redirect to login page
                self.handle_get("/login")
            elif method.upper() == "POST" and url == "/login":
                data = self._parse_form(self.body)
                if self.server.authenticator.valid_credentials(data):
                    #get cookies from authenticator
                    print(f"{data['username']} has logged in.")
                    biscuits = self.server.authenticator.get_credentials(data["username"])
                    #redirect to main page
                    header = self._create_header(200, "../index.html", "text/html", biscuits)
                    self._send_file(header, None)
                else:
                    #return 401 error
                    self.handle_get("/login")

        else:
            print(f"Received {method} request from {self.biscuits['user']} for {url}")
            if "HTTP" in protocol:
                if method.upper() == "GET":
                    self.handle_get(url)
                if method.upper() == "POST":
                    self.handle_post(url)
    
    @staticmethod
    def _request_to_dict(request:str)->dict:
        request_dict = {}
        request_lines = request.split("\r\n")
        top_line_items = request_lines.pop(0).split()
        #print("top line: ", top_line_items)
        if len(top_line_items) > 0:
            request_dict[top_line_items[0]] = top_line_items[1]
            request_dict[top_line_items[2]] = None
        for line in request_lines:
            if ":" in line:
                key, value = line.split(":", 1)
                request_dict[key] = value.strip() 
            else:
                request_dict[line] = None
        #print('request: ', request_dict)
        return request_dict


class Server(sserv.TCPServer):
    def __init__(self,
                server:str,
                port:int=50000,
                database_server="127.0.0.1",
                database_port=27017,
                db_name="Realms_MUD",
                db_tables=["Players", "Items", "Rooms", "Npcs"]):
        super().__init__((server, port), Router)
        print(f"Serving at {server} on port {port}...")
        self.state_manager = GameStateManager()
        self.db = DatabaseConnect(database_server, database_port, db_name=db_name, table_names=db_tables, interface=MongoConnection)
        print(f"Connected to database {db_name}...")
        self.engine = MudGameEngine(self.db)
        print(f"GameEngine started...")
        self.server = server
        self.port = port
        self.html = "../index.html"
        self.stylesheet = "../client/css/stylesheet.css"
        self.authenticator = Authenticator(self.db, self.state_manager)
        print(f"Authenticator started...")
        self.sessions = {} #key: player character name; value: randomly generated session id
    
def startServer():
    server = Server("127.0.0.1", 50000)
    server.serve_forever()