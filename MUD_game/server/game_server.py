import os.path
import socketserver as sserv
from .utils.ServerStateManager import ServerStateManager

class Router(sserv.StreamRequestHandler):
    def __init__(self):
        super().__init__()
        self.manager = ServerStateManager()
    def _create_header(self, http_code:int, file_path:str)->str:
        header = "HTTP/1.1 "
        content_type = file_path[file_path.rfind(".") + 1: len(file_path)]
        if http_code == 200:
            header = header + '200 OK\r\n'
        header = header + f'Content-Type: text/{content_type}\r\n'
        header = header + f'Connection: keep-alive\r\n\r\n'

        return header

    def _send_file(self, header:str, filepath:str)->None:
        response = ''
        header = self._create_header(200, filepath)
        with open(filepath) as file:
            lines = file.readlines()
            encoded_lines = "".join(lines)
            response = (header +  encoded_lines + '\r\n').encode("utf-8")
        self.request.sendall(response)
        print(response.decode("utf-8"))


    def handle_get(self, url):
        if url == "/":
            print("Sending main page")
            file_path = "../mud_client.html"
            header = self._create_header(200, file_path)
            self._send_file(header, "../mud_client.html")
        elif os.path.isfile(f"../{url}"):
            print(f"Sending {url}")
            file_path = f"../{url}"
            header = self._create_header(200, file_path)
            self._send_file(header, file_path)
    
    def _read_lines(self):
        data = []
        if self.rfile.readable():
            while True:
                chunk = self.rfile.readline().decode("utf-8")
                print("chunk:\n", chunk)
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
        print(request)
        method = request[0]
        url = request[1]
        protocol = request[2]

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
        self.server = server
        self.port = port
        self.html = "../index.html"
        self.stylesheet = "../client/css/stylesheet.css"

    
def startServer():
    server = Server('127.0.0.1')
    server.serve_forever()