from socket import socket, gethostname, AF_INET, SOCK_STREAM
from library import 

class Server:
    def __init__(self, port, logger):
        self.port = port
        self.logger = logger
        self.conn = None

        try:
            self.socket = socket(AF_INET, SOCK_STREAM)
            self.socket.bind((gethostname(), port))
            self.socket.listen()

            self.logger.info("Server started at %s with port %s.", gethostname(), port)

        except:
            self.logger.error("Server Initialization Exception", exc_info=True)

    def accept(self):
        try:
            self.conn, addr = self.socket.accept()
            self.logger.info("Server accepted connection from %s", addr)
        except:
            self.logger.error("Server accepting client failed", exc_info=True)

    def receive(self):
        pass

class Client:
    def __init__(self, server_ip, server_port, logger=None):
        self.server_ip = server_ip
        self.server_port = server_port

    def send(self):
        pass