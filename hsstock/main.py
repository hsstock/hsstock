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
    quote_ctx.start()
    lf = LF(quote_ctx)
    lf.get_trading_days('US')


    app = make_app()
    setup_logging()
    app.listen(AppConfig.get_config().get('web','port'))
    tornado.ioloop.IOLoop.current().start()

    quote_ctx.stop()