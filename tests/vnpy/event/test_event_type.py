# encoding: UTF-8

import unittest
from hsstock.vnpy.event.event_type import *

class EventTypeTestCase(unittest.TestCase):

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


    def test_duplicate_global_constant(self):
        ''' 检查是否存在内容重复的常量定义
        :return:
        '''
        check_dict = {}

        global_dict = globals()

        for key, value in global_dict.items():
            if '__' not in key:  # 不检查python内置对象
                if value in check_dict:
                    check_dict[value].append(key)
                else:
                    check_dict[value] = [key]

        for key, value in check_dict.items():
            self.assertTrue( len(value) == 1, u'存在重复的常量定义:{}'.format(str(key)) )

        print(u'测试完毕')


unittest.main