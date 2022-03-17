import queue

actQueue = queue.Queue()


def get():
    return actQueue.get()


def put(msg):
    actQueue.put(msg)


def isEmpty():
    return actQueue.empty()


def emptyQueue():
    with actQueue.mutex:
        actQueue.queue.clear()
