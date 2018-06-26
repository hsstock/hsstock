import unittest
import tushare as ts

from hsstock.service.store_service import StoreService

class StoreServiceTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.storeservice = StoreService()

    @classmethod
    def tearDownClass(cls):
        print('tearDownClass')

    def setUp(self):
        print('setUp')

    def tearDown(self):
        print('tearDown')


    def test_insert_many(self):
        code='002049'
        df = ts.get_tick_data(code, date='2018-06-13')
        engine = StoreServiceTestCase.storeservice.insert_many(code,df)


unittest.main