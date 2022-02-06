'''
Author: Jingcheng Wu (wu_jingcheng@qq.com)
Last Modified: Feb 6, 2022

Brief: A Task Panel Class that Monitor all classes
'''
from time import time
from datetime import timedelta
from threading import Loack
class TaskType:
    Training = 0
    Test = 1
    Influence = 2

    mapping = ['Training', 'Test', 'Influence']

class RTask:
    tasks = []

    @staticmethod
    def create_task(pid, task_type, total):
        RTask.tasks.append(RTask(pid, task_type, total))
    
    @staticmethod
    def exit_task(pid):
        for task in 

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

        # add to field
        RTask.tasks.append()


    def start(self):
        self.__init__(self.pid, self.task_type, self.total)

    def make_time_readable(self, t):
        try:
            res = str(timedelta(seconds=t))
        except:
            res = 'Unknown'
        return res
    
    def update(self):
        self.n += 1
        self.elapsed_time = time()-self.start_time
        rate = self.elapsed_time/self.n
        self.remaining_time = (self.total-self.n)/rate
        self.remaining_readable_time = self.make_time_readable(self.remaining_time)
    
    def get_readable_label(self):
        return f"{TaskType.mapping[self.task_type]}({self.pid})"
    
    def get_readable_time(self):
        return f"{self.n}/{self.total}[{self.elapsed_readable_time<<self.remaining_readable_time}]"

