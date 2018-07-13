import unittest

import hsstock.futuquant as ft

from hsstock.futuquant.common.constant import *
from hsstock.utils.app_config import AppConfig
from hsstock.service.quote_service import LF
from hsstock.service.quote_service import HF
from hsstock.common.freqlimit import FreqLimit
from hsstock.common.constant import *
from hsstock.service.quote_service import Subscribe


class QuoteServiceTestCase(unittest.TestCase):

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
        cls.sub = Subscribe(cls.ctx,total, kline, tiker, quote, order_book, rt_data, broker)
        cls.ctx.start()
        cls.lf = LF(cls.ctx)
        cls.hf = HF(cls.ctx,cls.sub)

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
        ret_code, ret_data = QuoteServiceTestCase.lf.get_trading_days('US')
        self.assertEqual( ret_code, RET_OK )

    def test_get_stock_basicinfo(self):
        ret_code, ret_data = QuoteServiceTestCase.lf.get_stock_basicinfo('US','STOCK')
        self.assertTrue(ret_code == RET_OK)

    def test_get_multiple_history_kline(self):
        ret_code, ret_data = QuoteServiceTestCase.lf.get_multiple_history_kline(['US.NTES'], '2018-06-20', '2018-06-25',  KLType.K_DAY, AuType.QFQ)
        self.assertTrue(ret_code == RET_OK)

        ret_code, ret_data = QuoteServiceTestCase.lf.get_multiple_history_kline(['HK.00700'], '2018-06-20', '2018-06-25',
                                                                                KLType.K_DAY, AuType.QFQ)
        self.assertTrue(ret_code == RET_OK)

    def test_get_history_kline(self):
        ret_code, ret_data = QuoteServiceTestCase.lf.get_history_kline('US.AAPL','2018-06-20', '2018-06-25')
        self.assertTrue(ret_code == RET_OK)

        ret_code, ret_data = QuoteServiceTestCase.lf.get_history_kline('HK.00700', '2018-06-20', '2018-06-25')
        self.assertTrue(ret_code == RET_OK)

    def test_get_autype_list(self):
        ret_code, ret_data = QuoteServiceTestCase.lf.get_autype_list(['US.AAPL'])
        self.assertTrue(ret_code == RET_OK)

        ret_code, ret_data = QuoteServiceTestCase.lf.get_autype_list(['HK.00700'])
        self.assertTrue(ret_code == RET_OK)

    def test_get_market_snapshot(self):
        ret_code, ret_data = QuoteServiceTestCase.lf.get_market_snapshot(['HK.00700', 'US.AAPL'])
        self.assertTrue(ret_code == RET_OK)

    def test_get_plate_list(self):
        ret_code, ret_data = QuoteServiceTestCase.lf.get_plate_list(Market.US)
        self.assertTrue(ret_code == RET_OK)

        ret_code, ret_data = QuoteServiceTestCase.lf.get_plate_list(Market.HK)
        self.assertTrue(ret_code == RET_OK)

        ret_code, ret_data = QuoteServiceTestCase.lf.get_plate_list(Market.SH)
        self.assertTrue(ret_code == RET_OK)

        ret_code, ret_data = QuoteServiceTestCase.lf.get_plate_list(Market.SZ)
        self.assertTrue(ret_code == RET_OK)

    def test_get_plate_stock(self):
        ret_code, ret_data = QuoteServiceTestCase.lf.get_plate_stock('US.BK2004')
        self.assertTrue(ret_code == RET_OK)

    def test_get_global_state(self):
        ret_code, ret_data = QuoteServiceTestCase.lf.get_global_state()
        self.assertTrue(ret_code == RET_OK)

    def test_get_broker_queue(self):
        ret_code, ret_data = QuoteServiceTestCase.sub.subscribe(['HK.00700'], ["BROKER"])
        ret_code, ret_data = QuoteServiceTestCase.sub.subscribe(['HK.00241'], ["BROKER"])
        ret_code, bid_data, ask_data = QuoteServiceTestCase.hf.get_broker_queue('HK.00700')
        self.assertTrue(ret_code == RET_OK)

        ret_code, ret_data = QuoteServiceTestCase.sub.subscribe(['HK.00700','HK.00241'], ["BROKER"])
        self.assertTrue(ret_code == RET_OK)

    def test_subscribe(self):

        ret_code, ret_data = QuoteServiceTestCase.sub.subscribe('HK.00700', 'TICKER')
        ret_code, ret_data = QuoteServiceTestCase.sub.subscribe('HK.00700', 'RT_DATA')
        ret_code, ret_data = QuoteServiceTestCase.sub.subscribe('HK.00700', 'K_DAY')
        ret_code, ret_data = QuoteServiceTestCase.sub.subscribe('HK.00700', 'ORDER_BOOK')
        ret_code, ret_data = QuoteServiceTestCase.sub.subscribe('HK.00700', 'RT_DATA')
        ret_code, ret_data = QuoteServiceTestCase.sub.subscribe('HK.00700', 'BROKER')
        ret_code, ret_data = QuoteServiceTestCase.sub.subscribe('HK.00241', 'BROKER')
        self.assertTrue(ret_code == RET_OK)

        ret_code, ret_data = QuoteServiceTestCase.sub.subscribe(['HK.00241','HK.00700'], ['TICKER','RT_DATA','K_DAY','ORDER_BOOK','RT_DATA','BROKER'])
        self.assertTrue(ret_code == RET_OK)

    def test_query_subscription(self):
        ret_code, ret_data = QuoteServiceTestCase.sub.query_subscription()
        self.assertTrue(ret_code == RET_OK)


    def test_get_stock_quote(self):
        ret_code, ret_data = QuoteServiceTestCase.sub.subscribe('HK.00700', "QUOTE")
        ret_code, ret_data = QuoteServiceTestCase.sub.subscribe('US.AAPL', 'QUOTE')
        ret_code, ret_data = QuoteServiceTestCase.hf.get_stock_quote(['US.AAPL','HK.00700'])
        self.assertTrue(ret_code == RET_OK)

    def test_get_rt_data(self):
        # ret_code, ret_data = QuoteServiceTestCase.sub.subscribe('HK.00700', "RT_DATA")
        ret_code, ret_data = QuoteServiceTestCase.hf.get_rt_data('HK.00700')
        self.assertTrue(ret_code == RET_OK)

        ret_code, ret_data = QuoteServiceTestCase.hf.get_rt_data('US.AAPL')
        self.assertTrue(ret_code == RET_OK)


    def test_get_rt_ticker(self):
        ret_code, ret_data = QuoteServiceTestCase.sub.subscribe('HK.00700', "TICKER")
        ret_code, ret_data = QuoteServiceTestCase.hf.get_rt_ticker('HK.00700',500)
        self.assertTrue(ret_code == RET_OK)

    def test_get_cur_kline(self):
        ret_code, ret_data = QuoteServiceTestCase.sub.subscribe('HK.00700', "K_DAY")
        ret_code, ret_data = QuoteServiceTestCase.hf.get_cur_kline('HK.00700',1000)
        self.assertTrue(ret_code == RET_OK)

    def test_get_order_book(self):
        ret_code, ret_data = QuoteServiceTestCase.sub.subscribe('HK.00700', "ORDER_BOOK")
        ret_code, ret_data = QuoteServiceTestCase.hf.get_order_book('HK.00700')
        self.assertTrue(ret_code == RET_OK)

    def test_rate_limit(self):
        freqlimit = FreqLimit()
        freqlimit2 = FreqLimit()
        self.assertTrue( freqlimit == freqlimit2)
        for n in range(1, 40, 1):
            ret = freqlimit.rate_limit(FREQ.UNLOCK_TRADE)
            if n > FREQLIMIT[FREQ.UNLOCK_TRADE]:
                self.assertTrue(ret == True)
                break

unittest.main