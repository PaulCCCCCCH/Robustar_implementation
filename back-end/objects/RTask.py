'''
Author: Jingcheng Wu (wu_jingcheng@qq.com)
Last Modified: Feb 6, 2022

Brief: A Task Panel Class that Monitor all classes
'''
from time import time
from datetime import timedelta
from threading import Lock
from utils.train import start_train
from utils.test import start_test

'''
TODO: make all thread apis create here
'''
class TaskType:
    Training = 0
    Test = 1
    Influence = 2

    mapping = ['Training', 'Test', 'Influence']
    start_funcs = [start_train, start_test]

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

    # This one should not be locked because it's purely a low-level implementation
    # otherwise may have deadlock
    @staticmethod
    def find_task(pid):
        for task in RTask.tasks:
            if task.pid == pid:
                return task
        return None

    @staticmethod
    @with_lock
    def create_task(task_type, *kargs, **kwargs):
        start_func = TaskType.start_funcs[task_type]
        thread = start_func(*kargs, **kwargs)
        if thread is None:
            return
        pid = thread.get_ident()
        task = RTask(pid, task_type)
        RTask.tasks.append(task)
        return task
    
    @staticmethod
    @with_lock
    def exit_task(pid):
        task = RTask.find_task(pid)
        if not task:
            raise Exception("Task not found")
        RTask.tasks.remove(task)
    
    @staticmethod
    @with_lock
    def update_task(pid):
        task = RTask.find_task(pid)
        task._update()

    @staticmethod
    @with_lock
    def get_tasks_digest():
        digest = []
        for task in RTask.tasks:
            digest.append((task.get_readable_label(), task.get_readable_time()))
        return digest

    def __init__(self, pid, task_type, total):
        # id
        self.pid = pid
        self.task_type = task_type

        # fields
        self.n = 0
        self.total = total
        self.start_time = time()
        self.remaining_time = float('inf')
        self.remaining_readable_time = 'Unknown'
        self.elapsed_time = 0
        self.elapsed_readable_time = 'Unknown'

    def start(self):
        self.__init__(self.pid, self.task_type, self.total)

    def make_time_readable(self, t):
        try:
            assert t>=0
            res = str(timedelta(seconds=int(t)))
        except:
            res = 'Unknown'
        return res

    def exit(self):
        RTask.exit_task(self.pid)

    def update(self):
        RTask.update_task(self.pid)
    
    def _update(self):
        self.n += 1
        self.elapsed_time = time()-self.start_time
        rate = self.elapsed_time/self.n
        self.remaining_time = (self.total-self.n)*rate

        self.elapsed_readable_time = self.make_time_readable(self.elapsed_time)
        self.remaining_readable_time = self.make_time_readable(self.remaining_time)
    
    def get_readable_label(self):
        return f"{TaskType.mapping[self.task_type]}({self.pid})"
    
    def get_readable_time(self):
        return f"{self.n}/{self.total}[{self.elapsed_readable_time}<<{self.remaining_readable_time}]"

