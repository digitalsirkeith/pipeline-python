from threading import Thread
from library.logger.server import general_logger, measurement_logger
import os, zlib

class Decompressor(Thread):
    def __init__(self, ce_queue):
        super(Decompressor, self).__init__()
        self.ce_queue = ce_queue
        
    def run(self):
        general_logger.info('Decompressor Thread Started')
        file_name = self.read_from_decryption()

        with open(f'sample/server/{file_name}', 'wb') as f:
            general_logger.info('File created with name: %s', file_name)
            while True:
                compressed_data = self.read_from_decryption()
                if compressed_data is None:
                    break
                decompressed_data = self.decompress(compressed_data)
                f.write(decompressed_data)
        
        general_logger.info('File saved.')
        general_logger.info('Decompressor Thread Exited')

    def decompress(self, data):
        return zlib.decompress(data)

    def read_from_decryption(self):
        return self.ce_queue.get(block=True)