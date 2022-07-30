import os.path as osp

from flask import send_file

from objects.RRequestQueue import RRequestQueue, GetImageRequestQueue
from objects.RResponse import RResponse
from utils.path_utils import to_unix


class RHandler:
    def __init__(self, request_queue: RRequestQueue):
        self.request_queue = request_queue

    def loop(self):
        while True:
            while self.request_queue.is_empty():
                pass
            self.handle(self.request_queue.dequeue())

    def handle(self, data):  # for subclasses to override and extend
        pass


class GetImageHandler(RHandler):
    def __init__(self, request_queue: GetImageRequestQueue):
        super().__init__(request_queue)

    def handle(self, data):
        normal_path = to_unix(data)
        if osp.exists(normal_path):
            return send_file(normal_path)
        else:
            return RResponse.fail()
