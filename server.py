#!/usr/bin/env python3

import os
import sys

def main():
    # INITIALIZING LOG FOLDERS
    try:
        os.mkdir('logs')
    except Exception as e:
        pass

    try:
        os.mkdir('logs/server')
    except Exception as e:
        pass

    if len(sys.argv) != 2:
        print('Usage:', sys.argv[0], '<port>')
        return

    

if __name__ == '__main__':
    main()