#!/usr/bin/env python3

import os, sys, dotenv, time
dotenv.load_dotenv()
from library.transmission.client import Client
from library.compression.compressor import Compressor
from library.encryption.encryptor import Encryptor
from library.logger.client import measurement_logger, score_logger
from library.genetic import Population
from queue import Queue

def main():
    if len(sys.argv) != 2:
        print('Usage:', sys.argv[0], '<ip>')
        return
    measurement_logger.info('Generation, Sample ID, Latency (seconds), Throughput(Bytes / second)')
    score_logger.warn('Generation, Filename, Sample ID, Latency (seconds),' + 
                                ' Throughput(Bytes / second), Compression Level, CE_Queue Size, ET_Queue Size, Queue Block Length')

    port = int(os.getenv('INITIAL_PORT'))

    path = lambda f: (os.path.join('sample/client', f))

    files = [(f, os.stat(path(f)).st_size) for f in os.listdir('sample/client') if os.path.isfile(path(f)) and f != '.DS_Store']
    gen_count = int(os.getenv('GEN_CNT'))
    population = Population()

    for gen_num in range(gen_count):
        print(f'Generation {gen_num} started.')
        for sample_id, sample in enumerate(population.samples):
            total_filesize = 0
            total_time = 0
            for filename, filesize in files:
                ce_queue = Queue(sample.ce_bufsize)
                et_queue = Queue(sample.et_bufsize)

                compressor = Compressor(ce_queue, filename, sample.compression_level, sample.block_size)
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
                time.sleep(2)
                measurement_logger.info('%d, %d, %s, %lf, %lf', gen_num, sample_id, filename, end-start, filesize/(end-start))
                total_filesize = total_filesize + filesize
                total_time = total_time + end - start

            sample.set_score(total_filesize / total_time)
            score_logger.warn('%d, %d, %lf, %lf, %d, %d, %d, %d', 
                gen_num, sample_id, total_time, total_filesize/total_time,
                    sample.compression_level, sample.ce_bufsize, sample.et_bufsize, sample.block_size)
                    
        population.generate_next()

if __name__ == '__main__':
    main()