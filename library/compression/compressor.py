from threading import Thread
from library.logger.client import general_logger, measurement_logger
import os, zlib

class Compressor(Thread):
    def __init__(self, ce_queue, filename, compression_level, block_size):
        super(Compressor, self).__init__()
        self.filename = filename
        self.ce_queue = ce_queue
        self.compression_level = compression_level
        self.block_size = block_size
        
    def run(self):
        general_logger.info('Compressor Thread Started')
        original_size = 0
        compressed_size = 0

        with open(f'sample/client/{self.filename}', 'rb') as f:
            while True:
                data = f.read(self.block_size)
                original_size += len(data)
                if len(data) < self.block_size:
                    if len(data):
                        compressed_data = self.compress(data)
                        compressed_size += len(compressed_data)
                        self.send_to_encryption(compressed_data)
                    break
                else:
                    compressed_data = self.compress(data)
                    compressed_size += len(compressed_data)
                    self.send_to_encryption(compressed_data)

        self.send_to_encryption(None)
        general_logger.info('Original Size: %s bytes', original_size)
        general_logger.info('Compressed Size: %s bytes', compressed_size)
        general_logger.info('Compression Ratio: %lf', compressed_size / original_size)
        general_logger.info('Compressor Thread Exited')

    def compress(self, data):
        return zlib.compress(data, level=self.compression_level)

    def send_to_encryption(self, compressed_data):
        self.ce_queue.put(compressed_data, block=True)