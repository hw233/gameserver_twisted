# coding=utf-8
import time
class Timer(object):

    def __init__(self):
        self._time = time.time()
        self._tasks = []
        self._done_tasks = []

    def update(self):
        self._time = time.time()
        # 先清空已完成的任务
        self.clear()
        # 执行任务
        self.process()

    def process(self):
        for task in self._tasks:
            # 是否到执行时间
            if task["time"] > self._time:
                continue
            # 执行任务
            task["func"]()
            # 计数器减1
            if task["count"] > 0:
                task["count"] -= 1
            # 完成是否任务
            if task["count"] == 0:
                self._done_tasks.append(task)
            else:
                task["time"] = self.time + task["interval"]

    @property
    def time(self):
        return self._time

    @property
    def delta_time(self):
        return time.time() - self.time

    def clear(self):
        for task in self._done_tasks:
            self._tasks.remove(task)
        self._done_tasks = []

    def delay(self, time, func):
        self.schedule(time, func, 1)

    def schedule(self, interval, func, count=-1):
        self._tasks.append({
            "interval": interval,
            "time": self.time + interval,
            "count": count,
            "func": func
        })
        self._tasks = sorted(self._tasks, key=lambda x: x["time"])
