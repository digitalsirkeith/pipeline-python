from socket import socket, gethostname, AF_INET, SOCK_STREAM
from library.logger.client import general_logger, measurement_logger
from threading import Thread
import os

class Client(Thread):
    def __init__(self, server_ip, server_port, filename):
        super(Client, self).__init__()

        self.server_ip = server_ip
        self.server_port = int(server_port)
        self.filename = filename

        try:
            self.socket = socket(AF_INET, SOCK_STREAM)
            self.socket.connect((
                self.server_ip,
                self.server_port
            ))
            general_logger.info('Client now connected to: %s with port %s', self.server_ip, self.server_port)

        except:
            general_logger.error('Client Initialization Failed.', exc_info=True)
    
    def run(self):
        general_logger.info('Client Thread now running.')
        self.send()
        pass

    def send(self):
        try:
            self.send_filename()
            self.send_file()
            general_logger.info('File (%s) sent.', self.filename)

        except:
            general_logger.error('Sending File failed', exc_info=True)

    def send_filename(self):
        try:
            length = len(self.filename)
            self.socket.send(format(length, "08").encode())
            self.socket.send(self.filename.encode())
            general_logger.info('Filename sent.')
        except:
            general_logger.error('Sending filename failed.', exc_info=True)

    def send_file(self):
        data_len = int(os.getenv('ENCRYPTION_BLOCKLEN'))
        
        try:
            with open(f'sample/client/{self.filename}', 'rb') as f:
                while True:
                    data = f.read(data_len)
                    if len(data) < data_len:
                        if len(data):
                            self.socket.send(data)
                        break
                    else:
                        self.socket.send(data)
        except:
            general_logger.error('Sending file failed.', exc_info=True)