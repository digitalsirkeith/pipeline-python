#!/usr/bin/env python3

import os, sys, dotenv
dotenv.load_dotenv()
from library.transmission.client import Client

def main():
    if len(sys.argv) != 4:
        print('Usage:', sys.argv[0], '<ip> <port> <filename>')
        return

    client = Client(*tuple(sys.argv[1:]))
    client.start()
    client.join()

if __name__ == '__main__':
    main()