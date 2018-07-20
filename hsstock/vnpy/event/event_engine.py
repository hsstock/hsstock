# encoding: UTF-8

# 系统模块

from queue import Queue, Empty
from threading import Thread, RLock
from time import sleep
from collections import defaultdict

# 第三方模块
from qtpy.QtCore import QTimer

# 自已开发的模块
from .event_type import *

class EventEngine(object):
    '''
     事件驱动引擎
    事件驱动引擎中所有的变量都设置为了私有，这是为了防止不小心
    从外部修改了这些变量的值或状态，导致bug。

    变量说明
    __queue：私有变量，事件队列
    __active：私有变量，事件引擎开关
    __thread：私有变量，事件处理线程
    __timer：私有变量，计时器
    __handlers：私有变量，事件处理函数字典


    方法说明
    __run: 私有方法，事件处理线程连续运行用
    __process: 私有方法，处理事件，调用注册在引擎中的监听函数
    __onTimer：私有方法，计时器固定事件间隔触发后，向事件队列中存入计时器事件
    start: 公共方法，启动引擎
    stop：公共方法，停止引擎
    register：公共方法，向引擎中注册监听函数
    unregister：公共方法，向引擎中注销监听函数
    put：公共方法，向事件队列中存入新的事件

    事件监听函数必须定义为输入参数仅为一个event对象，即：

    函数
    def func(event)
        ...

    对象方法
    def method(self, event)
        ...
    '''


    def __init__(self):
        """初始化事件引擎"""
        # 事件队列
        self.__queue = Queue()

        # 事件引擎开关
        self.__active = False

        # 事件处理线程
        self.__thread = Thread(target=self.__run)

        # 计时器，用于触发计时器事件
        self.__timer = QTimer()
        self.__timer.timeout.connect(self.__onTimer)

        # 这里的__handlers是一个字典，用来保存对应的事件调用关系
        # 其中每个键对应的值是一个列表，列表中保存了对该事件进行监听的函数功能
        self.__handlers = defaultdict(list)

        # __generalHandlers是一个列表，用来保存通用回调函数（所有事件均调用）
        self.__generalHandlers = []

        # ----------------------------------------------------------------------

    def __run(self):
        """引擎运行"""
        while self.__active == True:
            try:
                event = self.__queue.get(block=True, timeout=1)  # 获取事件的阻塞时间设为1秒
                self.__process(event)
            except Empty:
                pass

        # ----------------------------------------------------------------------

    def __process(self, event):
        """处理事件"""
        # 检查是否存在对该事件进行监听的处理函数
        if event.type_ in self.__handlers:
            # 若存在，则按顺序将事件传递给处理函数执行
            [handler(event) for handler in self.__handlers[event.type_]]

            # 以上语句为Python列表解析方式的写法，对应的常规循环写法为：
            # for handler in self.__handlers[event.type_]:
            # handler(event)

        # 调用通用处理函数进行处理
        if self.__generalHandlers:
            [handler(event) for handler in self.__generalHandlers]

        # ----------------------------------------------------------------------

    def __onTimer(self):
        """向事件队列中存入计时器事件"""
        # 创建计时器事件
        event = Event(type_=EVENT_TIMER)

        # 向队列中存入计时器事件
        self.put(event)

        # ----------------------------------------------------------------------

    def start(self, timer=True):
        """
        引擎启动
        timer：是否要启动计时器
        """
        # 将引擎设为启动
        self.__active = True

        # 启动事件处理线程
        self.__thread.start()

        # 启动计时器，计时器事件间隔默认设定为1秒
        if timer:
            self.__timer.start(1000)

        # ----------------------------------------------------------------------

    def stop(self):
        """停止引擎"""
        # 将引擎设为停止
        self.__active = False

        # 停止计时器
        self.__timer.stop()

        # 等待事件处理线程退出
        self.__thread.join()

        # ----------------------------------------------------------------------

    def register(self, type_, handler):
        """注册事件处理函数监听"""
        # 尝试获取该事件类型对应的处理函数列表，若无defaultDict会自动创建新的list
        handlerList = self.__handlers[type_]

        # 若要注册的处理器不在该事件的处理器列表中，则注册该事件
        if handler not in handlerList:
            handlerList.append(handler)

        # ----------------------------------------------------------------------

    def unregister(self, type_, handler):
        """注销事件处理函数监听"""
        # 尝试获取该事件类型对应的处理函数列表，若无则忽略该次注销请求
        handlerList = self.__handlers[type_]

        # 如果该函数存在于列表中，则移除
        if handler in handlerList:
            handlerList.remove(handler)

        # 如果函数列表为空，则从引擎中移除该事件类型
        if not handlerList:
            del self.__handlers[type_]

        # ----------------------------------------------------------------------

    def put(self, event):
        """向事件队列中存入事件"""
        self.__queue.put(event)

        # ----------------------------------------------------------------------

    def registerGeneralHandler(self, handler):
        """注册通用事件处理函数监听"""
        if handler not in self.__generalHandlers:
            self.__generalHandlers.append(handler)

        # ----------------------------------------------------------------------

    def unregisterGeneralHandler(self, handler):
        """注销通用事件处理函数监听"""
        if handler in self.__generalHandlers:
            self.__generalHandlers.remove(handler)

########################################################################
class EventEngine2(object):
    """
    计时器使用python线程的事件驱动引擎
    """

    # ----------------------------------------------------------------------
    def __init__(self):
        """初始化事件引擎"""
        # 事件队列
        self.__queue = Queue()

        # 事件引擎开关
        self.__active = False

        # 事件处理线程
        self.__thread = Thread(target=self.__run)

        # 计时器，用于触发计时器事件
        # 与EventEngine的区别？
        self.__timer = Thread(target=self.__runTimer)
        self.__timerActive = False  # 计时器工作状态
        self.__timerSleep = 0.01  # 计时器触发间隔（默认1秒）

        # 这里的__handlers是一个字典，用来保存对应的事件调用关系
        # 其中每个键对应的值是一个列表，列表中保存了对该事件进行监听的函数功能
        self.__handlers = defaultdict(list)

        # __generalHandlers是一个列表，用来保存通用回调函数（所有事件均调用）
        self.__generalHandlers = []

        # ----------------------------------------------------------------------

    def __run(self):
        """引擎运行"""
        while self.__active == True:
            try:
                event = self.__queue.get(block=True, timeout=1)  # 获取事件的阻塞时间设为1秒
                self.__process(event)
            except Empty:
                pass

    # ----------------------------------------------------------------------
    def __process(self, event):
        """处理事件"""
        # 检查是否存在对该事件进行监听的处理函数
        if event.type_ in self.__handlers:
            # 若存在，则按顺序将事件传递给处理函数执行
            [handler(event) for handler in self.__handlers[event.type_]]

            # 以上语句为Python列表解析方式的写法，对应的常规循环写法为：
            # for handler in self.__handlers[event.type_]:
            # handler(event)

        # 调用通用处理函数进行处理
        if self.__generalHandlers:
            [handler(event) for handler in self.__generalHandlers]

            # ----------------------------------------------------------------------

    def __runTimer(self):
        """运行在计时器线程中的循环函数"""
        while self.__timerActive:
            # 创建计时器事件
            event = Event(type_=EVENT_TIMER)

            # 向队列中存入计时器事件
            self.put(event)

            # 等待
            sleep(self.__timerSleep)

    # ----------------------------------------------------------------------
    def start(self, timer=True):
        """
        引擎启动
        timer：是否要启动计时器
        """
        # 将引擎设为启动
        self.__active = True

        # 启动事件处理线程
        self.__thread.start()

        # 启动计时器，计时器事件间隔默认设定为1秒
        if timer:
            self.__timerActive = True
            self.__timer.start()

    # ----------------------------------------------------------------------
    def stop(self):
        """停止引擎"""
        # 将引擎设为停止
        self.__active = False

        # 停止计时器
        self.__timerActive = False
        self.__timer.join()

        # 等待事件处理线程退出
        self.__thread.join()

    # ----------------------------------------------------------------------
    def register(self, type_, handler):
        """注册事件处理函数监听"""
        # 尝试获取该事件类型对应的处理函数列表，若无defaultDict会自动创建新的list
        handlerList = self.__handlers[type_]

        # 若要注册的处理器不在该事件的处理器列表中，则注册该事件
        if handler not in handlerList:
            handlerList.append(handler)

    # ----------------------------------------------------------------------
    def unregister(self, type_, handler):
        """注销事件处理函数监听"""
        # 尝试获取该事件类型对应的处理函数列表，若无则忽略该次注销请求
        handlerList = self.__handlers[type_]

        # 如果该函数存在于列表中，则移除
        if handler in handlerList:
            handlerList.remove(handler)

        # 如果函数列表为空，则从引擎中移除该事件类型
        if not handlerList:
            del self.__handlers[type_]

            # ----------------------------------------------------------------------

    def put(self, event):
        """向事件队列中存入事件"""
        self.__queue.put(event)

    # ----------------------------------------------------------------------
    def registerGeneralHandler(self, handler):
        """注册通用事件处理函数监听"""
        if handler not in self.__generalHandlers:
            self.__generalHandlers.append(handler)

    # ----------------------------------------------------------------------
    def unregisterGeneralHandler(self, handler):
        """注销通用事件处理函数监听"""
        if handler in self.__generalHandlers:
            self.__generalHandlers.remove(handler)

########################################################################
class EventEngine3(object):
    """
    变量说明
    _queue：私有变量，事件队列
    _active：私有变量，事件引擎开关
    _thread：私有变量，事件处理线程
    _timer：私有变量，计时器
    _handlers：私有变量，事件处理函数字典


    方法说明
    _run: 私有方法，事件处理线程连续运行用
    _process: 私有方法，处理事件，调用注册在引擎中的监听函数
    start: 公共方法，启动引擎
    stop：公共方法，停止引擎
    register：公共方法，向引擎中注册监听函数
    unregister：公共方法，向引擎中注销监听函数
    put：公共方法，向事件队列中存入新的事件
    """

    def __init__(self):
        # 事件队列
        self._queue = Queue()

        # 事件引擎开关
        self._active = False

        # 事件处理线程
        self._thread = Thread(target=self._run)

        # 线程锁
        self._lock = RLock()

        # 计时器，用于触发计时器事件
        self._timer = Thread(target=self._run_timer)
        self._timer_active = False  # 计时器工作状态
        self._timer_sleep = 1  # 计时器触发间隔（默认1秒）

        # 这里的_handlers是一个字典，用来保存对应的事件调用关系
        # 其中每个键对应的值是一个列表，列表中保存了对该事件进行监听的函数功能
        self._handlers = defaultdict(list)

        # _general_handlers是一个列表，用来保存通用回调函数（所有事件均调用）
        self._general_handlers = []

    def _run(self):
        """引擎运行"""
        while self._active:
            try:
                event = self._queue.get(block=False, timeout=0)  # 获取事件设为非阻塞
                self._lock.acquire()
                self._process(event)
                self._lock.release()
            except Empty:
                break

    def _process(self, event):
        """处理事件"""
        # 检查是否存在对该事件进行监听的处理函数
        if event.type_ in self._handlers:
            # 若存在，则按顺序将事件传递给处理函数执行
            [handler(event) for handler in self._handlers[event.type_]]

        # 调用通用处理函数进行处理
        if self._general_handlers:
            [handler(event) for handler in self._general_handlers]

    def _run_timer(self):
        """运行在计时器线程中的循环函数"""
        while self._timer_active:
            # 创建计时器事件
            event = Event(type_=EVENT_TIMER3)

            # 向队列中存入计时器事件
            self.put(event)

            # 等待
            sleep(self._timer_sleep)

    def start(self, timer=True):
        """
        引擎启动
        timer：是否要启动计时器
        """
        # 将引擎设为启动
        self._active = True

        # 启动事件处理线程
        self._thread.start()

        # 启动计时器，计时器事件间隔默认设定为1秒
        if timer:
            self._timer_active = True
            self._timer.start()

    def stop(self):
        """停止引擎"""

        # 停止计时器
        if self._timer_active:
            self._timer_active = False
            self._timer.join()

        # 等待事件处理线程退出
        self._thread.join()

    def register(self, event_type, handler):
        """注册事件处理函数监听"""
        # 尝试获取该事件类型对应的处理函数列表，若无defaultDict会自动创建新的list
        handler_list = self._handlers[event_type]

        # 若要注册的处理器不在该事件的处理器列表中，则注册该事件
        if handler not in handler_list:
            handler_list.append(handler)

    def unregister(self, event_type, handler):
        """注销事件处理函数监听"""
        # 尝试获取该事件类型对应的处理函数列表，若无则忽略该次注销请求
        handler_list = self._handlers[event_type]

        # 如果该函数存在于列表中，则移除
        if handler in handler_list:
            handler_list.remove(handler)

        # 如果函数列表为空，则从引擎中移除该事件类型
        if not handler_list:
            del self._handlers[event_type]

    def put(self, event):
        """向事件队列中存入事件"""
        self._queue.put(event)

    def registerGeneralHandler(self, handler):
        """注册通用事件处理函数监听"""
        if handler not in self._general_handlers:
            self._general_handlers.append(handler)

    def unregisterGeneralHandler(self, handler):
        """注销通用事件处理函数监听"""
        if handler in self._general_handlers:
            self._general_handlers.remove(handler)

########################################################################
class Event:
    """事件对象"""

    # ----------------------------------------------------------------------
    def __init__(self, type_=None):
        """Constructor"""
        self.type_ = type_  # 事件类型
        self.dict_ = {}  # 字典用于保存具体的事件数据


class TestOne(object):
    def test(self):
        """测试函数"""
        from datetime import datetime

        def simpletest(event):
            print(u'处理每秒触发的计时器事件：{}'.format(str(datetime.now())))

        ee = EventEngine3()
        ee.put(Event("aaa"))
        ee.put(Event("aaa"))
        ee.put(Event("aaa"))
        # ee.register(EventType.EVENT_TIMER.value, simpletest)
        ee.register("aaa", simpletest)
        # ee.registerGeneralHandler(simpletest)
        ee.start()
        ee.stop()


if __name__ == "__main__":
    aa = TestOne()
    aa.test()
