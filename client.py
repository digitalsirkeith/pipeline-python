#!/usr/bin/env python3

import os, sys, dotenv, time
dotenv.load_dotenv()
from library.transmission.client import Client
from library.compression.compressor import Compressor
from library.encryption.encryptor import Encryptor
from library.logger.client import measurement_logger
from queue import Queue

def main():
    if len(sys.argv) != 2:
        print('Usage:', sys.argv[0], '<ip>')
        return
    measurement_logger.info('Generation, Filename, Latency (seconds), Throughput(Bytes / second)')

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

            compressor = Compressor(ce_queue, filename)
            encryptor = Encryptor(ce_queue, et_queue)
            client = Client(et_queue, sys.argv[1], port, filename)

            start = time.time()
            compressor.start()
            encryptor.start()
            client.start()

            compressor.join()
            encryptor.join()
            client.join()
            end = time.time()

            port = port + 1
            time.sleep(0.5)
            measurement_logger.info('%d, %s, %lf, %lf', gen_num, filename, end-start, filesize/(end-start))

if __name__ == '__main__':
    main()