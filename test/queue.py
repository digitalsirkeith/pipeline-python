from queue import Queue

queue = Queue(1024)

queue.put(None)
print(queue.get(block=True))