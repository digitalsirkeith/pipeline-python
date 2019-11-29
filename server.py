#!/usr/bin/env python3

import os, sys, dotenv
dotenv.load_dotenv()
from library.transmission.server import Server
from library.compression.decompressor import Decompressor
from library.encryption.decryptor import Decryptor
from library.logger.server import measurement_logger
from queue import Queue

def main():
    if len(sys.argv) != 2:
        print('Usage:', sys.argv[0], '<port>')
        return
    measurement_logger.info('Layer, Filename, Start Time, End Time')

    ce_bufsize = int(os.getenv('CE_BUFSIZE'))
    et_bufsize = int(os.getenv('ET_BUFSIZE'))

    ce_queue = Queue(ce_bufsize)
    et_queue = Queue(et_bufsize)
    
    server = Server(int(sys.argv[1]), et_queue)
    decryptor = Decryptor(ce_queue, et_queue)
    decompressor = Decompressor(ce_queue)

    server.start()
    decryptor.start()
    decompressor.start()
    
    server.join()
    decryptor.join()
    decompressor.join()

if __name__ == '__main__':
    main()