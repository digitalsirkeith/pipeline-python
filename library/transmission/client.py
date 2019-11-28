from socket import socket, gethostname, AF_INET, SOCK_STREAM
from library.logger.client import general_logger, measurement_logger
from threading import Thread
import os

class Client(Thread):
    def __init__(self, et_queue, server_ip, server_port, filename):
        super(Client, self).__init__()

        self.server_ip = server_ip
        self.server_port = int(server_port)
        self.filename = filename
        self.et_queue = et_queue

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
        general_logger.info('Client Thread now exited.')

    def send(self):
        try:
            self.send_filename()
            self.send_file()
            general_logger.info('File (%s) sent.', self.filename)

        except:
            general_logger.error('Sending File failed', exc_info=True)

    def send_filename(self):
        try:
            self.send_data(self.filename.encode())
            general_logger.info('Filename sent.')
        except:
            general_logger.error('Sending filename failed.', exc_info=True)

    def send_file(self):
        try:
            total_size = 0
            while True:
                encrypted_data = self.read_from_encryption()
                if encrypted_data is None:
                    break
                total_size += len(encrypted_data)
                self.send_data(encrypted_data)
            general_logger.info('Total encrypted file size: %s', total_size)

        except:
            general_logger.error('Sending file failed.', exc_info=True)

    def read_from_encryption(self):
        return self.et_queue.get(block=True)

    def send_data(self, data):
        length = len(data)
        self.socket.send(format(length, "08").encode())
        self.socket.send(data)