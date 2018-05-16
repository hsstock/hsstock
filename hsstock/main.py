# -*- coding: UTF-8 -*-

import tornado.ioloop
import tornado.web
from tornado.web import RequestHandler
import os
import json

import pandas as pd
import futuquant as ft
from futuquant.constant import MKT_MAP



from hsstock.web.app_logging import setup_logging
from hsstock.utils.app_config import  AppConfig
from hsstock.service.quote_service import LF
from hsstock.service.quote_service import HF
from hsstock.service.quote_service import Subscribe
from hsstock.service.trade_service import HKTrade
from hsstock.service.trade_service import USTrade

class MainHandler(RequestHandler):
    def get(self):
        self.write('Hello,World!')

def path():
    return os.path.dirname(__file__)

def make_app():
    return tornado.web.Application([
        (r"/hs",MainHandler)
    ])


if __name__ == "__main__":
    '''
    1. Start QE Engine
    2. Start Web Server
    '''
    config = AppConfig.get_config()
    quote_ctx = ft.OpenQuoteContext(config.get('ftserver','host'),int(config.get('ftserver','port')))
    tradehk_ctx = ft.OpenHKTradeContext(config.get('ftserver','host'),int(config.get('ftserver','port')))
    tradeus_ctx = ft.OpenUSTradeContext(config.get('ftserver', 'host'), int(config.get('ftserver', 'port')))

    decipher = config.get('ftserver', 'decipher')
    total = config.get('quota', 'total')
    kline = config.get('quota', 'kline')
    tiker = config.get('quota', 'ticker')
    quote = config.get('quota', 'quote')
    order_book = config.get('quota', 'order_book')
    rt_data = config.get('quota', 'rt_data')
    broker = config.get('quota', 'broker')



    quote_ctx.start()
    lf = LF(quote_ctx)
    # lf.get_trading_days('US')
    # lf.get_stock_basicinfo('US','STOCK')
    # lf.get_autype_list(['HK.00700','US.AAPL'])
    # lf.get_history_kline('US.AAPL')
    # lf.get_market_snapshot(['HK.00700', 'US.AAPL'])
    # lf.get_plate_list('US')
    # lf.get_plate_stock('US.BK2004')
    # lf.get_global_state()
    lf.get_multi_points_history_kline( ['HK.00700','HK.00241'],['2017-01-01', '2017-01-28'])
    #
    sub = Subscribe(quote_ctx,total, kline, tiker, quote, order_book, rt_data, broker)
    # sub.subscribe('HK.00700', "QUOTE", push=True)
    # sub.subscribe('US.AAPL', 'QUOTE')
    # sub.subscribe('HK.00700', 'TICKER')
    # sub.subscribe('HK.00700', 'RT_DATA')
    # sub.subscribe('HK.00700', 'K_DAY')
    # sub.subscribe('HK.00700', 'ORDER_BOOK')
    # sub.subscribe('HK.00700', 'RT_DATA')
    # sub.subscribe('HK.00700', 'BROKER')
    # sub.subscribe('HK.00241', 'BROKER')
    #
    # sub.query_subscription()
    #
    hf = HF(quote_ctx,sub)
    #hf.get_stock_quote(['US.AAPL','HK.00700'])
    #hf.get_rt_ticker('HK.00700',500)
    #hf.get_cur_kline('HK.00700',1000)
    #hf.get_order_book('HK.00700')
    #hf.get_rt_data('HK.00700')
    #hf.get_broker_queue('HK.00700')
    # hf.get_broker_queue('HK.00241')


    # hktrade = HKTrade(tradehk_ctx)
    # hktrade.unlock_trade(decipher)
    # ustrade = USTrade(tradeus_ctx)
    # ustrade.unlock_trade(decipher)

    # hktrade.accinfo_query(0)
    # hktrade.accinfo_query(1)
    # ustrade.accinfo_query(0)
    # ustrade.accinfo_query(1)
    # hktrade.position_list_query()
    # ustrade.position_list_query()
    # hktrade.order_list_query()  # alyy 117343447
    # ustrade.order_list_query()
    # hktrade.deal_list_query()
    # ustrade.deal_list_query()
    # hktrade.history_order_list_query()
    # ustrade.history_order_list_query()
    # hktrade.history_deal_list_query()
    # ustrade.history_deal_list_query()
    # hktrade.subscribe_order_deal_push(['HK.00700'])
    # ustrade.subscribe_order_deal_push(['US.AAPL'])
    # hktrade.change_order(0.89, 40000, 117343447)
    # ustrade.change_order(0.89, 40000, 117343447)
    # hktrade.set_order_status(0,117343447)
    # hktrade.set_order_status(3, 117343447)
    # ustrade.set_order_status(0, 117343447)
    # ustrade.set_order_status(3, 117343447)
    # hktrade.place_order(0.88, 10000, 'HK.01060', 0, 0)
    # ustrade.place_order(2.88, 10000, 'US.JMEI', 0, 0)


app = make_app()
setup_logging()
# app.listen(AppConfig.get_config().get('web','port'))
# tornado.ioloop.IOLoop.current().start()

quote_ctx.stop()
tradehk_ctx.stop()
tradeus_ctx.stop()