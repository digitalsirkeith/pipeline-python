from socket import socket, gethostname, AF_INET, SOCK_STREAM
from library.logger.client import general_logger, measurement_logger
import os

class Client:
    def __init__(self, server_ip, server_port):
        self.server_ip = server_ip
        self.server_port = int(server_port)

        try:
            self.socket = socket(AF_INET, SOCK_STREAM)
            self.socket.connect((
                self.server_ip,
                self.server_port
            ))
            general_logger.info('Client now connected to: %s with port %s', self.server_ip, self.server_port)

        except:
            general_logger.error('Client Initialization Failed.', exc_info=True)

    def send(self, filename):
        try:
            data_len = int(os.getenv('ENCRYPTION_BLOCKLEN'))
            self.send_filename(filename)

            # with open(f'sample/client/{filename}') as f:
            #     f.read(data_len)

        except:
            general_logger.error('Sending File failed', exc_info=True)

    def send_filename(self, filename):
        try:
            length = len(filename)
            self.socket.send(format(length, "08").encode())
            self.socket.send(filename.encode())
            general_logger.info('Filename sent.')
        except:
            general_logger.error('Sending filename failed.', exc_info=True)