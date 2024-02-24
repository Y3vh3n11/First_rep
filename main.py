from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse
import mimetypes 
from pathlib import Path
import logging
from colorama import Fore, Style
from threading import Thread
import socket
import json
from datetime import datetime

BASE_DIR = Path()
HOST = 'localhost'
SOCKET_PORT = 5000
HTTP_PORT = 3000

class HttpHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        route = urllib.parse.urlparse(self.path)
        match route.path:
            case '/': self.send_html('index.html')
            case '/message': self.send_html('message.html')
            case _:
                file = BASE_DIR.joinpath(route.path[1:])
                if file.exists():
                    self.send_static(file)
                else:
                    self.send_static('error.html', 404)

    def do_POST(self):
        data = self.rfile.read(int(self.headers['Content-Length'])) 
        
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        client_socket.sendto(data, (HOST, SOCKET_PORT))
        client_socket.close()

        self.send_response(302)
        self.send_header('Location', '/') 
        self.end_headers() 


    def send_html(self, filename, status_code=200):
        self.send_response(status_code)
        self.send_header('Content-Type', 'text/html')
        self.end_headers()
        
        with open(filename, 'rb') as file:
            self.wfile.write(file.read())


    def send_static(self, filename, status_code=200):
        self.send_response(status_code)
        mime_type, *_ = mimetypes.guess_type(filename)
        
        if mime_type:
            self.send_header('Content-Type', mime_type)
        else:
            self.send_header('Content-Type', 'text/plain')
        self.end_headers()
        
        with open(filename, 'rb') as file:
            self.wfile.write(file.read())

def save_data(data):
    data_parse = urllib.parse.unquote_plus(data.decode()) 
    try:
        data_dict = {key:value for key, value in [el.split('=') for el in data_parse.split('&')]} 
        with open('storage/data.json', 'r', encoding='utf-8') as file:
            read = json.load(file)                     
            
        with open('storage/data.json', 'w', encoding='utf-8') as file:
            logging.debug(data_dict)
            read[str(datetime.now())] = data_dict
            json.dump(read, file, ensure_ascii=False, indent=4) 
    
    except ValueError as err:
        logging.error(err)
    except OSError as err:
        logging.error(err)

def run_server_http():
    address = (HOST, HTTP_PORT)
    http_server = HTTPServer(address, HttpHandler)
    try:
        logging.debug('Start HTTP server')
        http_server.serve_forever()
    except KeyboardInterrupt as err:
        logging.debug(err)
    finally:
        http_server.server_close()

def run_server_socket():
    address = (HOST, SOCKET_PORT)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(address)
    logging.debug('Start socket server')
    try:
        while True:
            data, addr = server_socket.recvfrom(1024)
            save_data(data)            
    except KeyboardInterrupt:
        pass
    finally:
        server_socket.close()

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format=f'{Fore.GREEN} %(threadName)s%(message)s {Style.RESET_ALL}')
    
    http_server_thread = Thread(target=run_server_http)
    http_server_thread.start()

    socket_server_thread = Thread(target=run_server_socket)    
    socket_server_thread.start()



