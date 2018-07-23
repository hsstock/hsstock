import unittest
import hsstock.tushare as ts

from hsstock.service.mysql_service import MysqlService

class StoreServiceTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.storeservice = MysqlService()

    @classmethod
    def tearDownClass(cls):
        print('tearDownClass')

    def setUp(self):
        print('setUp')

    def tearDown(self):
        print('tearDown')


    # def test_insert_many(self):
    #     code='002049'
    #     df = ts.get_tick_data(code, date='2018-06-13')
    #     StoreServiceTestCase.storeservice.insert_many(code,df)

    def test_find(self):
        StoreServiceTestCase.storeservice.find('')

unittest.main