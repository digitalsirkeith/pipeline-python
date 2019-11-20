#!/usr/bin/env python3

import os, sys

def main():
    # INITIALIZING LOG FOLDERS
    try:
        os.mkdir('logs')
    except Exception as e:
        pass

    if len(sys.argv) != 3:
        print('Usage:', sys.argv[0], '<ip> <port>')
        return

if __name__ == '__main__':
    main()