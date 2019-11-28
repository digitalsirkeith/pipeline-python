from threading import Thread
from library.logger.server import general_logger, measurement_logger
import os, hashlib
from Crypto import Random
from Crypto.Cipher import AES

class Decryptor(Thread):
    def __init__(self, ce_queue, et_queue):
        super(Decryptor, self).__init__()

        self.key = hashlib.sha256(os.getenv('KEY').encode()).digest()
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
        iv = encrypted_data[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        padded_data = cipher.decrypt(encrypted_data[AES.block_size:])
        
        return self.unpad(padded_data)

    def read_from_transmission(self):
        return self.et_queue.get(block=True)

    def send_to_decompression(self, compressed_data):
        self.ce_queue.put(compressed_data, block=True)

    @staticmethod
    def unpad(data):
        return data[:-ord(data[len(data)-1:])]