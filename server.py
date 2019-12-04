#!/usr/bin/env python3

import os, sys, dotenv
dotenv.load_dotenv()
from library.transmission.server import Server
from library.compression.decompressor import Decompressor
from library.encryption.decryptor import Decryptor
from library.logger.server import measurement_logger
from queue import Queue

def main():
    if len(sys.argv) != 1:
        print('Usage:', sys.argv[0])
        return
    measurement_logger.info('Layer, Filename, Start Time, End Time')

    port = int(os.getenv('INITIAL_PORT'))

    path = lambda f: (os.path.join('sample/client', f))

    files = [(f, os.stat(path(f)).st_size) for f in os.listdir('sample/client') if os.path.isfile(path(f)) and f != '.DS_Store']
    gen_count = int(os.getenv('GEN_CNT'))

    for gen_num in range(gen_count):
        for filename, filesize in files:
            ce_bufsize = int(os.getenv('CE_BUFSIZE'))
            et_bufsize = int(os.getenv('ET_BUFSIZE'))

            ce_queue = Queue(ce_bufsize)
            et_queue = Queue(et_bufsize)
            
            server = Server(port, et_queue)
            decryptor = Decryptor(ce_queue, et_queue)
            decompressor = Decompressor(ce_queue)

            server.start()
            decryptor.start()
            decompressor.start()
            
            server.join()
            decryptor.join()
            decompressor.join()

            port = port + 1

if __name__ == '__main__':
    main()