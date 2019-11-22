#!/usr/bin/env python3

import os, sys, dotenv
dotenv.load_dotenv()
from library.transmission.client import Client
from library.compression.compressor import Compressor
from library.encryption.encryptor import Encryptor
from queue import Queue

def main():
    if len(sys.argv) != 4:
        print('Usage:', sys.argv[0], '<ip> <port> <filename>')
        return

    ce_bufsize = int(os.getenv('CE_BUFSIZE'))
    et_bufsize = int(os.getenv('ET_BUFSIZE'))

    ce_queue = Queue(ce_bufsize)
    et_queue = Queue(et_bufsize)

    compressor = Compressor(ce_queue, sys.argv[3])
    encryptor = Encryptor(ce_queue, et_queue)
    client = Client(et_queue, *tuple(sys.argv[1:]))

    compressor.start()
    encryptor.start()
    client.start()

    compressor.join()
    encryptor.join()
    client.join()

if __name__ == '__main__':
    main()