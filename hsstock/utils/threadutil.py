# -*- coding: UTF-8 -*-
import logging
import threading

class MyThread(threading.Thread):
    def __init__(self, threadname,job_func,ts=None):
        threading.Thread.__init__(self)
        self.threadname = threadname
        self.ts = ts
        self.job_func = job_func

    def run(self):
        logging.info ("开始线程：" + self.threadname)
        self.job_func(self.ts)
        logging.info ("退出线程：" + self.threadname)