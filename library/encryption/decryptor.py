from threading import Thread
from library.logger.server import general_logger, measurement_logger
import os

class Decryptor(Thread):
    def __init__(self, ce_queue, et_queue):
        super(Decryptor, self).__init__()

        self.key = os.getenv('KEY')
        self.ce_queue = ce_queue
        self.et_queue = et_queue

    def run(self):
        general_logger.info('Decryptor Thread Started')
        file_name = self.read_from_transmission()
        self.send_to_decompression(file_name)

        while True:
            encrypted_data = self.read_from_transmission()
            if encrypted_data is None:
                break
            decrypted_data = self.decrypt(encrypted_data)
            self.send_to_decompression(decrypted_data)

        self.send_to_decompression(None)
        general_logger.info('Decryptor Thread Exited')

    def decrypt(self, encrypted_data):
        return encrypted_data

    def read_from_transmission(self):
        return self.et_queue.get(block=True)

    def send_to_decompression(self, compressed_data):
        self.ce_queue.put(compressed_data, block=True)