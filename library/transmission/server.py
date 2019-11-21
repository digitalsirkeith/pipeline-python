from socket import socket, gethostname, AF_INET, SOCK_STREAM
from library.logger.server import general_logger, measurement_logger
from threading import Thread
import os

class Server(Thread):
    def __init__(self, port):
        super(Server, self).__init__()
        
        self.port = port
        self.conn = None

        try:
            self.socket = socket(AF_INET, SOCK_STREAM)
            self.socket.bind((gethostname(), port))
            self.socket.listen()

            general_logger.info("Server started at %s with port %s.", gethostname(), port)

        except:
            general_logger.error("Server Initialization Exception", exc_info=True)
    
    def run(self):
        general_logger.info('Server Thread now running.')
        self.accept()
        self.receive()

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

            with open(f'sample/server/{file_name}', 'wb') as f:
                general_logger.info(f'File created with name: sample/server/{file_name}')

                while True:
                    data = self.conn.recv(data_len)

                    if not data:
                        general_logger.info("Client disconnected.")
                        break

                    else:
                        f.write(data)
                        general_logger.debug('Receiving data (%d bytes).', len(data))
                        general_logger.debug('Message: %s', data)

                general_logger.info("Saving file.")

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