from socket import socket, gethostname, AF_INET, SOCK_STREAM
from library.logger.server import general_logger, measurement_logger
import os

class Server:
    def __init__(self, port):
        self.port = port
        self.conn = None

        try:
            self.socket = socket(AF_INET, SOCK_STREAM)
            self.socket.bind((gethostname(), port))
            self.socket.listen()

            general_logger.info("Server started at %s with port %s.", gethostname(), port)

        except:
            general_logger.error("Server Initialization Exception", exc_info=True)

    def accept(self):
        try:
            self.conn, addr = self.socket.accept()
            general_logger.info("Server accepted connection from %s", addr)
        except:
            general_logger.error("Server accepting client failed.", exc_info=True)

    def receive(self):
        try:
            os.mkdir('sample/server')
        except:
            pass
        try:
            data_len = int(os.getenv('ENCRYPTION_BLOCKLEN'))
            file_name = self.recv_filename()

            with open(f'sample/server/{file_name}', 'w+') as f:
                general_logger.info(f'File created with name: sample/server/{file_name}')

                while True:
                    data = self.conn.recv(data_len)
                    if not data:
                        general_logger.info("Client disconnected.")
                        break
                    else:
                        general_logger.debug('Receiving data (%d bytes).', len(data))
                        general_logger.debug('Message: %s', data)
        except:
            general_logger.error("Failed to receive file.", exc_info=True)

    def recv_filename(self):
        try:
            length = int(self.conn.recv(8).decode())
            file_name = self.conn.recv(length).decode()

            general_logger.info('Filename received (%d bytes): %s', length, file_name)
            return file_name
            
        except:
            general_logger.error("Failed to receive filename", exc_info=True)