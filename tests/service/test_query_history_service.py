import unittest

import hsstock.futuquant as ft
from hsstock.futuquant.common.constant import MKT_MAP

from hsstock.utils.app_config import AppConfig
from hsstock.service.quote_service import LF
from hsstock.service.quote_service import HF
from hsstock.service.quote_service import Subscribe
from hsstock.service.query_history_service import QueryHistory

from hsstock.futuquant.common.constant import RET_ERROR
from hsstock.futuquant.common.constant import RET_OK

class QueryHistoryServiceTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        config = AppConfig.get_config()
        total = config.get('quota', 'total')
        kline = config.get('quota', 'kline')
        tiker = config.get('quota', 'ticker')
        quote = config.get('quota', 'quote')
        order_book = config.get('quota', 'order_book')
        rt_data = config.get('quota', 'rt_data')
        broker = config.get('quota', 'broker')
        cls.ctx = ft.OpenQuoteContext(config.get('ftserver', 'host'), int(config.get('ftserver', 'port')))
        cls.ctx.start()
        cls.qh = QueryHistory(cls.ctx)

    @classmethod
    def tearDownClass(cls):
        cls.ctx.stop()
        cls.ctx.close()
        print('tearDownClass')

    def setUp(self):
        print('setUp')

    def tearDown(self):
        print('tearDown')


    def test_get_trading_days(self):
        change_min = 10
        change_max = 30

        ret_code, ret_data = QueryHistoryServiceTestCase.qh.query_history_change_stocks(['SH'], '2017-01-10', '2017-12-01', change_min, change_max,  'STOCK')
        self.assertEqual( ret_code, RET_OK )



unittest.main