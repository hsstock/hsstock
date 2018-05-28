# encoding: UTF-8

import unittest

import sys
from time import sleep
from datetime import datetime
from qtpy.QtCore import QCoreApplication

from hsstock.vnpy.event.event_engine import EventEngine2
from hsstock.vnpy.event.event_type import *

class EventEngineTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print('setUpClass')

    @classmethod
    def tearDownClass(cls):
        print('tearDownClass')

    def setUp(self):
        print('setUp')

    def tearDown(self):
        print('tearDown')

    @unittest.skip("demonstrating skipping")
    def test_event_engine2_registerGeneralHandler(self):

        def simpletest(event):
            print(u'registerGeneralHandler处理每秒触发的计时器事件：{}'.format(str(datetime.now())))

        app = QCoreApplication(sys.argv)

        ee = EventEngine2()
        ee.registerGeneralHandler(simpletest)
        ee.start()

        sleep(3)
        ee.stop()
        app.exit(0)

    @unittest.skip("demonstrating skipping")
    def test_event_engine2_unregisterGeneralHandler(self):

        def simpletest(event):
            print(u'unregisterGeneralHandler处理每秒触发的计时器事件：{}'.format(str(datetime.now())))

        app = QCoreApplication(sys.argv)

        ee = EventEngine2()
        ee.registerGeneralHandler(simpletest)
        ee.unregisterGeneralHandler(simpletest)
        ee.start()

        sleep(3)
        ee.stop()
        app.exit(0)


    def test_event_engine2_register(self):

        def simpletest(event):
            print(u'eventEngine2处理每秒触发的计时器事件：{}'.format(str(datetime.now())))

        app = QCoreApplication(sys.argv)

        ee = EventEngine2()
        # 不触发定时器
        # ee.register(1, simpletest)
        ee.register(EVENT_TIMER,simpletest)
        ee.start()

        sleep(3)
        ee.stop()
        app.exit(0)

unittest.main