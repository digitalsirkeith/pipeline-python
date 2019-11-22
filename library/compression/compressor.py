from zlib import compress
from threading import Thread
from library.logger.client import general_logger, measurement_logger
import os

class Compressor(Thread):
    def __init__(self, ce_queue, filename):
        super(Compressor, self).__init__()
        self.filename = filename
        self.ce_queue = ce_queue
        
    def run(self):
        general_logger.info('Compressor Thread Started')
        data_len = int(os.getenv('COMPRESSION_BLOCKLEN'))

        with open(f'sample/client/{self.filename}', 'rb') as f:
            while True:
                data = f.read(data_len)
                if len(data) < data_len:
                    if len(data):
                        compressed_data = self.compress(data)
                        self.send_to_encryption(compressed_data)
                    break
                else:
                    compressed_data = self.compress(data)
                    self.send_to_encryption(compressed_data)

        self.send_to_encryption(None)
        general_logger.info('Compressor Thread Exited')

    def compress(self, data):
        return data

    def send_to_encryption(self, compressed_data):
        self.ce_queue.put(compressed_data, block=True)