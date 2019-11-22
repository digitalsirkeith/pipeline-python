from threading import Thread
from library.logger.client import general_logger, measurement_logger
import os

class Encryptor(Thread):
    def __init__(self, ce_queue, et_queue):
        super(Encryptor, self).__init__()

        self.key = os.getenv('KEY')
        self.ce_queue = ce_queue
        self.et_queue = et_queue

    def run(self):
        general_logger.info('Encryptor Thread Started')
        while True:
            compressed_data = self.read_from_compression()
            if compressed_data is None:
                break
            self.send_to_transmission(compressed_data)
        self.send_to_transmission(None)
        general_logger.info('Encryptor Thread Exited')


    def read_from_compression(self):
        return self.ce_queue.get(block=True)

    def send_to_transmission(self, compressed_data):
        self.et_queue.put(compressed_data, block=True)