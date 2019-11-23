from threading import Thread
from library.logger.client import general_logger, measurement_logger
import os, hashlib
from Crypto import Random
from Crypto.Cipher import AES

class Encryptor(Thread):
    def __init__(self, ce_queue, et_queue):
        super(Encryptor, self).__init__()

        self.key = hashlib.sha256(os.getenv('KEY').encode()).digest()
        self.ce_queue = ce_queue
        self.et_queue = et_queue

    def run(self):
        general_logger.info('Encryptor Thread Started')
        
        while True:
            compressed_data = self.read_from_compression()
            if compressed_data is None:
                break
            encrypted_data = self.encrypt(compressed_data)
            self.send_to_transmission(encrypted_data)

        self.send_to_transmission(None)
        general_logger.info('Encryptor Thread Exited')

    def encrypt(self, data):
        raw_data = self.pad(data)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)

        return iv + cipher.encrypt(raw_data)

    def read_from_compression(self):
        return self.ce_queue.get(block=True)

    def send_to_transmission(self, compressed_data):
        self.et_queue.put(compressed_data, block=True)

    @staticmethod
    def pad(data):
        return data + ((AES.block_size - len(data) % AES.block_size) * chr(AES.block_size - len(data) % AES.block_size)).encode()