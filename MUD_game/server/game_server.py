import os.path
import socketserver as sserv
import json
from .utils.MudGameEngine import MudGameEngine
from .utils.GameStateManager import GameStateManager

class Router(sserv.StreamRequestHandler):
    def _create_header(self, http_code:int, file_path:str, content_type=None)->str:
        header = "HTTP/1.1 "
        if not content_type:
            content_type = file_path[file_path.rfind(".") + 1: len(file_path)]
        if http_code == 200:
            header = header + '200 OK\r\n'
        header = header + f'Content-Type: text/{content_type}\r\n'
        header = header + f'Connection: keep-alive\r\n\r\n'

        return header

    def _send_file(self, header:str, filepath:str)->None:
        response = ''
        header = self._create_header(200, filepath)
        dir = os.path.abspath(os.path.dirname(__file__))
        file_path = os.path.join(dir, filepath)
        with open(file_path) as file:
            lines = file.readlines()
            encoded_lines = "".join(lines)
            response = (header +  encoded_lines + '\r\n').encode("utf-8")
        self.request.sendall(response)
        #print(response.decode("utf-8"))

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
        if url == "/" and self.server.state_manager.get_status(self.client_address) == "LOGGED_OUT":
            print("Sending login page")
            file_path = "../client/html/login.html"
            header = self._create_header(200, file_path)
            self._send_file(header, file_path)
        elif url == "/character_creation":
            print("Sending character creation page")
            file_path = "../client/html/character_creation.html"
            header = self._create_header(200, file_path)
            self._send_file(header, file_path)
        elif url.find("command:") > -1:
            self.process_command(url[url.find(":") + 1:])
        elif os.path.isfile(f"{filepath}"):
            print(f"Sending {url}")
            file_path = f"../{url}"
            header = self._create_header(200, file_path)
            self._send_file(header, file_path)
        #else 404 error
    
    def _read_lines(self):
        data = []
        if self.rfile.readable():
            while True:
                chunk = self.rfile.readline().decode("utf-8")
                #print("chunk:\n", chunk)
                if len(chunk) > 0 and chunk != '\r\n':
                    data.append(chunk.strip())
                if chunk == '\r\n':
                    break
        return data
    
    def handle_post(self, data):
        header = {}
        top_line = data.pop(0).split()

        header["request"] = top_line[0]
        header["resource"] = top_line[1]
        header["protocal"] = top_line[2]

        for line in data:
            key, value = line.split(":", 1)
            header[key.lower()] = value.lower().strip()
        
        body = ''
        if "content-length" in header.keys():
            size = int(header["content-length"])
            body = self.rfile.read(size).decode("utf-8")
        else:
            body = "Not implemented"
        
        print(header)
        print(body)

    def handle(self):
        header = self._read_lines()
        request = header[0].split()
        #print(request)
        method = request[0]
        url = request[1]
        protocol = request[2]
        if self.client_address not in self.server.state_manager.users():
            self.server.state_manager.add_user(self.client_address)

        if "HTTP" in protocol:
            if method.upper() == "GET":
                self.handle_get(url)
            if method.upper() == "POST":
                self.handle_post(header)
    
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
    def __init__(self, server:str, port:int=50000):
        super().__init__((server, port), Router)
        self.engine = MudGameEngine()
        self.state_manager = GameStateManager()
        self.server = server
        self.port = port
        self.html = "../index.html"
        self.stylesheet = "../client/css/stylesheet.css"
    
def startServer():
    server = Server('127.0.0.1', 50000)
    server.serve_forever()