with open('sample/client/1.txt', 'rb') as f:
    while True:
        data = f.read(1)
        if (len(data) != 1):
            break
        print(data)
    print('done')