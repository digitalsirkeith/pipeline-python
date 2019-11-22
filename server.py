#!/usr/bin/env python3

import os, sys, dotenv
dotenv.load_dotenv()
from library.transmission.server import Server

def main():
    if len(sys.argv) != 2:
        print('Usage:', sys.argv[0], '<port>')
        return
    
    server = Server(int(sys.argv[1]), None)
    server.start()
    server.join()

if __name__ == '__main__':
    main()