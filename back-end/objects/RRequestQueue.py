from threading import Lock


def with_lock(func):
    def wrapper(*wargs, **kwargs):
        RRequestQueue.lock.acquire()
        res = func(*wargs, **kwargs)
        RRequestQueue.lock.release()
        return res

    return wrapper


class RRequestQueue:
    lock = Lock()
    request_queue = []
    request_limit = 0

    def __init__(self, request_limit=20):
        self.request_limit = request_limit

    @with_lock
    def enqueue(self, obj):
        self.request_queue.append(obj)
        if self.size() > self.request_limit:
            self.request_queue.remove(0)

    @with_lock
    def dequeue(self):
        if not self.is_empty():
            self.request_queue.pop(0)

    @with_lock
    def front(self):
        if not self.is_empty():
            return self.request_queue[0]

    @with_lock
    def size(self):
        return len(self.request_queue)

    @with_lock
    def is_empty(self):
        return self.size() == 0

    def set_request_limit(self, request_limit):
        self.request_limit = request_limit


class GetImageRequestQueue(RRequestQueue):
    def __init__(self, request_limit):
        super().__init__(request_limit)
