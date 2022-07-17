from objects.RRequestQueue import RRequestQueue, with_lock


class RHandler:

    def __init__(self, request_queue: RRequestQueue):
        self.request_queue = request_queue

    @with_lock
    def handle(self):
        while not self.request_queue.is_empty():
            self.operate(self.request_queue.front())
            self.request_queue.dequeue()

    def operate(self, obj):
        pass


class RImageHandler(RHandler):
    def __init__(self, request_queue: RRequestQueue):
        RHandler.__init__(request_queue)
