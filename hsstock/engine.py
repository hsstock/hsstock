# -*- coding: UTF-8 -*-

import pandas as pd
import futuquant as ft
from futuquant.constant import MKT_MAP


from hsstock.web.app_logging import setup_logging
from hsstock.utils.app_config import AppConfig
from hsstock.service.quote_service import LF
from hsstock.service.quote_service import HF
from hsstock.service.quote_service import Subscribe
from hsstock.service.trade_service import HKTrade
from hsstock.service.trade_service import USTrade
from hsstock.service.query_history_service import QueryHistory


class Engine(object):
    def __init__(self):
        '''
        QE Engine Init
        '''
        config = AppConfig.get_config()
        self.config = config
        quote_ctx = ft.OpenQuoteContext(config.get('ftserver', 'host'), int(config.get('ftserver', 'port')))
        self.quote_ctx = quote_ctx
        self.tradehk_ctx = ft.OpenHKTradeContext(config.get('ftserver', 'host'), int(config.get('ftserver', 'port')))
        self.tradeus_ctx = ft.OpenUSTradeContext(config.get('ftserver', 'host'), int(config.get('ftserver', 'port')))
        self.decipher = config.get('ftserver', 'decipher')

        total = config.get('quota', 'total')
        kline = config.get('quota', 'kline')
        tiker = config.get('quota', 'ticker')
        quote = config.get('quota', 'quote')
        order_book = config.get('quota', 'order_book')
        rt_data = config.get('quota', 'rt_data')
        broker = config.get('quota', 'broker')

        quote_ctx.start()
        self.lf = LF(quote_ctx)
        self.sub = Subscribe(quote_ctx, total, kline, tiker, quote, order_book, rt_data, broker)
        self.hf = HF(quote_ctx, self.sub)
        self.hktrade = HKTrade(self.tradehk_ctx)
        self.hktrade.unlock_trade(self.decipher)
        self.ustrade = USTrade(self.tradeus_ctx)
        self.ustrade.unlock_trade(self.decipher)
        self.queryhistory = QueryHistory(quote_ctx)

    def stop(self):
        self.quote_ctx.stop()
        self.tradehk_ctx.stop()
        self.tradeus_ctx.stop()

    def get_queryhistory(self):
        return self.queryhistory