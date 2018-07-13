import unittest
import time

import hsstock.futuquant as ft
from hsstock.futuquant import *
from hsstock.utils.app_config import AppConfig
from hsstock.service.trade_service import *

class TradeServiceTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        config = AppConfig.get_config()
        cls.hk_ctx = ft.OpenHKTradeContext(config.get('ftserver', 'host'), int(config.get('ftserver', 'port')))
        cls.us_ctx = ft.OpenUSTradeContext(config.get('ftserver', 'host'), int(config.get('ftserver', 'port')))
        cls.hk_trade = Trade(cls.hk_ctx)
        cls.us_trade = Trade(cls.us_ctx)
        cls.hk_trade.unlock_trade(None,config.get('ftserver','decipher'))
        cls.us_trade.unlock_trade(None,config.get('ftserver', 'decipher'))

    @classmethod
    def tearDownClass(cls):
        cls.hk_ctx.stop()
        cls.hk_ctx.close()
        cls.us_ctx.stop()
        cls.us_ctx.close()
        print('tearDownClass, testTradeService')

    def setUp(self):
        print('setUp')

    def tearDown(self):
        print('tearDown')

    @unittest.skip("demonstrating skipping")
    def test_skip(self):
        print("test skip")

    def test_get_acc_list(self):
        ret_code, ret_data = TradeServiceTestCase.hk_trade.get_acc_list()
        self.assertTrue(ret_code == RET_OK)

        ret_code, ret_data = TradeServiceTestCase.us_trade.get_acc_list()
        self.assertTrue(ret_code == RET_OK)


    def test_accinfo_query(self):
        ret_code, ret_data = TradeServiceTestCase.hk_trade.accinfo_query(TrdEnv.REAL)
        self.assertTrue(ret_code == RET_OK)

        ret_code, ret_data = TradeServiceTestCase.hk_trade.accinfo_query(TrdEnv.SIMULATE)
        self.assertTrue(ret_code == RET_ERROR)

        ret_code, ret_data = TradeServiceTestCase.us_trade.accinfo_query(TrdEnv.REAL)
        self.assertTrue(ret_code == RET_OK)

        # US don't support simulation envoriment
        ret_code, ret_data = TradeServiceTestCase.us_trade.accinfo_query(TrdEnv.SIMULATE)
        self.assertTrue(ret_code == RET_ERROR)

    def test_position_list_query(self):
        ret_code, ret_data = TradeServiceTestCase.hk_trade.position_list_query()
        self.assertTrue(ret_code == RET_OK)

        ret_code, ret_data = TradeServiceTestCase.us_trade.position_list_query()
        self.assertTrue(ret_code == RET_OK)

    def test_place_order(self):
        pass
        # TODO
        # ret_code, ret_data = TradeServiceTestCase.hk_trade.place_order(0.1, 1000, 'HK.01060')
        # print(ret_data)
        # self.assertTrue(ret_code == RET_ERROR)
        #
        # ret_code, ret_data = TradeServiceTestCase.us_trade.place_order(1.88, 100, 'US.JMEI')
        # print(ret_data)
        # self.assertTrue(ret_code == RET_ERROR)

    def test_order_list_query(self):
        ret_code, ret_data = TradeServiceTestCase.hk_trade.order_list_query()
        self.assertTrue(ret_code == RET_OK)

        ret_code, ret_data = TradeServiceTestCase.us_trade.order_list_query()
        self.assertTrue(ret_code == RET_OK)
        print(ret_data)

    def test_modify_order(self):
        #ret_code, ret_data = TradeServiceTestCase.hk_trade.modify_order( modify_order_op, order_id, qty,price, adjust_limit, trd_env, acc_id)
        pass

    def test_deal_list_query(self):
        ret_code, ret_data = TradeServiceTestCase.hk_trade.deal_list_query()
        self.assertTrue(ret_code == RET_OK)
        ret_code, ret_data = TradeServiceTestCase.us_trade.deal_list_query()
        self.assertTrue(ret_code == RET_OK)

    def test_history_order_list_query(self):
        ret_code, ret_data = TradeServiceTestCase.hk_trade.history_order_list_query()
        self.assertTrue(ret_code == RET_OK)

        ret_code, ret_data = TradeServiceTestCase.us_trade.history_order_list_query()
        self.assertTrue(ret_code == RET_OK)

    def test_history_deal_list_query(self):
        ret_code, ret_data = TradeServiceTestCase.hk_trade.history_deal_list_query('HK.00700','2018-06-01 00:00:00','2018-07-10 00:00:00',TrdEnv.REAL)
        self.assertTrue(ret_code == RET_OK)

        ret_code, ret_data = TradeServiceTestCase.us_trade.history_deal_list_query('US.AAPL','2018-06-01 00:00:00','2018-07-10 00:00:00',TrdEnv.REAL)
        self.assertTrue(ret_code == RET_OK)

    def test_order_handler(self):
        TradeServiceTestCase.hk_ctx.set_handler(HSTradeOrder())
        TradeServiceTestCase.hk_trade.place_order(300, 100, "HK.00700", TrdSide.BUY)
        time.sleep(3)

        TradeServiceTestCase.us_ctx.set_handler(HSTradeOrder())
        TradeServiceTestCase.us_trade.place_order(150, 100, "US.AAPL", TrdSide.BUY)
        time.sleep(3)

    def test_deal_handler(self):
        TradeServiceTestCase.hk_ctx.set_handler(HSTradeDeal())
        TradeServiceTestCase.hk_trade.place_order(300, 100, "HK.00700", TrdSide.BUY)
        time.sleep(3)

        TradeServiceTestCase.us_ctx.set_handler(HSTradeDeal())
        TradeServiceTestCase.us_trade.place_order(150, 100, "US.AAPL", TrdSide.BUY)
        time.sleep(3)

unittest.main