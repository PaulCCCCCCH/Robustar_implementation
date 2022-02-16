'''
Author: Jingcheng Wu (wu_jingcheng@qq.com)
Last Modified: Feb 6, 2022

Brief: A Task Panel Class that Monitor all classes
'''
from time import time
from datetime import timedelta
from threading import Lock
# from utils.train import start_train
# from utils.test import start_test
from flask_socketio import emit
from objects.RServer import RServer

'''
TODO: make all thread apis create here
'''
class TaskType:
    Training = 0
    Test = 1
    Influence = 2

    mapping = ['Training', 'Test', 'Influence']
    # start_funcs = [start_train, start_test]

def with_lock(func):
    def wrapper(*wargs, **kwargs):
        RTask.lock.acquire()
        res = func(*wargs, **kwargs)
        RTask.lock.release()
        return res
    return wrapper

class RTask:
    tasks = []
    lock = Lock()
    tid = 0

    # This one should not be locked because it's purely a low-level implementation
    # otherwise may have deadlock
    @staticmethod
    # @with_lock
    def generate_tid():
        RTask.tid += 1
        return RTask.tid

    @staticmethod
    def find_task(tid):
        for task in RTask.tasks:
            if task.tid == tid:
                return task
        return None

    @staticmethod
    # @with_lock
    def create_task(task):
        # start_func = TaskType.start_funcs[task_type]
        # thread = start_func(*kargs, **kwargs)
        # if thread is None:
        #     return
        tid = task.tid
        assert tid not in [t.tid for t in RTask.tasks], "Duplicate tid in task"
        RTask.tasks.append(task)
        return task
    
    @staticmethod
    # @with_lock
    def exit_task(tid):
        task = RTask.find_task(tid)
        if not task:
            raise Exception("Task not found")
        RTask.tasks.remove(task)
    
    @staticmethod
    # @with_lock
    def update_task(tid):
        task = RTask.find_task(tid)
        task._update()
        digest = RTask.get_tasks_digest()
        socket = RServer.getSocket()
        socket.emit("digest", {
            "digest": digest
        })
        print()
        print(digest, flush=True)

    @staticmethod
    # @with_lock
    def get_tasks_digest():
        digest = []
        for task in RTask.tasks:
            digest.append((task.get_readable_label(), task.get_percentage(), task.get_readable_time()))
        return digest

    def __init__(self, task_type, total):
        # id
        self.task_type = task_type

        # fields
        self.tid = RTask.generate_tid()
        self.n = 0
        self.total = total
        self.start_time = time()
        self.remaining_time = float('inf')
        self.remaining_readable_time = 'Unknown'
        self.elapsed_time = 0
        self.elapsed_readable_time = 'Unknown'
        RTask.create_task(self)

    def start(self):
        self.__init__(self.task_type, self.total)

    def make_time_readable(self, t):
        try:
            assert t>=0
            res = str(timedelta(seconds=int(t)))
        except:
            res = 'Unknown'
        return res

    def exit(self):
        RTask.exit_task(self.tid)

    def update(self):
        RTask.update_task(self.tid)
    
    def _update(self):
        self.n += 1
        self.elapsed_time = time()-self.start_time
        rate = self.elapsed_time/self.n
        self.remaining_time = (self.total-self.n)*rate

        self.elapsed_readable_time = self.make_time_readable(self.elapsed_time)
        self.remaining_readable_time = self.make_time_readable(self.remaining_time)
    
    def get_percentage(self):
        return self.n/self.total if self.total else 'Invalid'
    
    def get_readable_label(self):
        return f"{TaskType.mapping[self.task_type]}({self.tid})"
    
    def get_readable_time(self):
        return f"{self.n}/{self.total}[{self.elapsed_readable_time}<<{self.remaining_readable_time}]"

