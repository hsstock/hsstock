import unittest

import futuquant as ft
from futuquant.constant import MKT_MAP

from hsstock.utils.app_config import AppConfig
from hsstock.service.trade_service import HKTrade
from hsstock.service.trade_service import USTrade
from hsstock.utils.tick_deco import clock

from futuquant.constant import RET_ERROR
from futuquant.constant import RET_OK

class TradeServiceTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        config = AppConfig.get_config()
        cls.hk_ctx = ft.OpenHKTradeContext(config.get('ftserver', 'host'), int(config.get('ftserver', 'port')))
        cls.us_ctx = ft.OpenUSTradeContext(config.get('ftserver', 'host'), int(config.get('ftserver', 'port')))
        cls.hk_ctx.unlock_trade(config.get('ftserver','decipher'))
        cls.us_ctx.unlock_trade(config.get('ftserver', 'decipher'))

    @classmethod
    def tearDownClass(cls):
        cls.hk_ctx.stop()
        cls.us_ctx.stop()
        print('tearDownClass, testTradeService')

    def setUp(self):
        print('setUp')

    def tearDown(self):
        print('tearDown')

    @unittest.skip("demonstrating skipping")
    def test_skip(self):
        print("test skip")

    def test_accinfo_query(self):
        ret_code, ret_data = TradeServiceTestCase.hk_ctx.accinfo_query(0)
        self.assertTrue(ret_code == RET_OK)

        ret_code, ret_data = TradeServiceTestCase.hk_ctx.accinfo_query(1)
        self.assertTrue(ret_code == RET_OK)

        ret_code, ret_data = TradeServiceTestCase.us_ctx.accinfo_query(0)
        self.assertTrue(ret_code == RET_OK)

        # US don't support simulation envoriment
        ret_code, ret_data = TradeServiceTestCase.us_ctx.accinfo_query(1)
        self.assertTrue(ret_code == RET_ERROR)

    def test_position_list_query(self):
        ret_code, ret_data = TradeServiceTestCase.hk_ctx.position_list_query()
        self.assertTrue(ret_code == RET_OK)

        ret_code, ret_data = TradeServiceTestCase.us_ctx.position_list_query()
        self.assertTrue(ret_code == RET_OK)

    def test_order_list_query(self):
        ret_code, ret_data = TradeServiceTestCase.hk_ctx.order_list_query()
        self.assertTrue(ret_code == RET_OK)

        ret_code, ret_data = TradeServiceTestCase.us_ctx.order_list_query()
        self.assertTrue(ret_code == RET_OK)
        print(ret_data)

    def test_deal_list_query(self):
        ret_code, ret_data = TradeServiceTestCase.hk_ctx.deal_list_query()
        self.assertTrue(ret_code == RET_OK)
        ret_code, ret_data = TradeServiceTestCase.us_ctx.deal_list_query()
        self.assertTrue(ret_code == RET_OK)

    def test_history_order_list_query(self):
        ret_code, ret_data = TradeServiceTestCase.hk_ctx.history_order_list_query()
        self.assertTrue(ret_code == RET_OK)

        ret_code, ret_data = TradeServiceTestCase.us_ctx.history_order_list_query()
        self.assertTrue(ret_code == RET_OK)

    def test_history_deal_list_query(self):
        ret_code, ret_data = TradeServiceTestCase.hk_ctx.history_deal_list_query('','','',0)
        self.assertTrue(ret_code == RET_OK)

        ret_code, ret_data = TradeServiceTestCase.us_ctx.history_deal_list_query('','','',0)
        self.assertTrue(ret_code == RET_OK)


    def test_subscribe_order_deal_push(self):
        ret_code = TradeServiceTestCase.hk_ctx.subscribe_order_deal_push(['HK.00700'])
        self.assertTrue(ret_code == RET_OK)

        ret_code = TradeServiceTestCase.us_ctx.subscribe_order_deal_push(['HK.00700'])
        self.assertTrue(ret_code == RET_OK)


    # def test_change_order(self):
    #     # ToDo
    #     ret_code, ret_data = TradeServiceTestCase.hk_ctx.change_order(0.89, 40000, 117343447)
    #     print(ret_code)
    #     print(ret_data)
    #     self.assertTrue(ret_code == RET_ERROR)
    #     # ToDo
    #     ret_code, ret_data = TradeServiceTestCase.us_ctx.change_order(0.89, 40000, 117343447)
    #     self.assertTrue(ret_code == RET_ERROR)
    #
    # def test_set_order_status(self):
    #     # ToDo
    #     ret_code, ret_data = TradeServiceTestCase.hk_ctx.set_order_status(0,117343447)
    #     self.assertTrue(ret_code == RET_ERROR)
    #     ret_code, ret_data = TradeServiceTestCase.hk_ctx.set_order_status(3, 117343447)
    #     self.assertTrue(ret_code == RET_ERROR)
    #
    #     # ToDo
    #     ret_code, ret_data = TradeServiceTestCase.us_ctx.set_order_status(0,117343447)
    #     self.assertTrue(ret_code == RET_ERROR)
    #     ret_code, ret_data = TradeServiceTestCase.us_ctx.set_order_status(3, 117343447)
    #     self.assertTrue(ret_code == RET_ERROR)

    def test_1_place_order(self):
        # ToDo
        ret_code, ret_data = TradeServiceTestCase.hk_ctx.place_order(0.1, 1000, 'HK.01060', 0, 0)
        print(ret_data)
        self.assertTrue(ret_code == RET_ERROR)

        # ToDo
        ret_code, ret_data = TradeServiceTestCase.us_ctx.place_order(1.88, 100, 'US.JMEI', 0, 0)
        self.assertTrue(ret_code == RET_ERROR)




unittest.main