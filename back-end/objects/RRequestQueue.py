import collections
from threading import Lock


class RRequestQueue:
    lock = Lock()
    request_queue = collections.deque()

    def __init__(self, request_limit=30):
        self.request_limit = request_limit

    def enqueue(self, data):
        self.lock.acquire()
        self.request_queue.append(data)
        self.lock.release()
        if self.size() > self.request_limit:
            self.lock.acquire()
            self.request_queue.popleft()
            self.lock.release()

    def dequeue(self):
        if not self.is_empty():
            self.lock.acquire()
            obj = self.request_queue.popleft()
            self.lock.release()
            return obj

    def size(self):
        self.lock.acquire()
        size = len(self.request_queue)
        self.lock.release()
        return size

    def is_empty(self):
        return self.size() == 0

    def set_request_limit(self, request_limit):
        self.request_limit = request_limit


class GetImageRequestQueue(RRequestQueue):
    def __init__(self, request_limit=30):
        super().__init__(request_limit)
