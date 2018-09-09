# -*- coding: UTF-8 -*-

import tornado.ioloop
import tornado.httpserver
import signal
import logging
import tornado.web
from tornado.web import RequestHandler
import os

from hsstock.utils.app_logging import setup_logging
from hsstock.utils.app_config import  AppConfig
from hsstock.service.engine.qeengine import QEEngine
import pandas as pd

class MainHandler(RequestHandler):
    def get(self):
        self.write('Hello,World!')

'''
    def query_history_change_stocks(markets=['HK'], start='2017-01-05', end='2017-12-30', change_min=5.0,
                                change_max=None, stock_type='STOCK', ascend=True):
'''
class QueryHistoryHandler(RequestHandler):
    def get(self):
        markets = self.get_argument('markets')
        start = self.get_argument('start')
        end = self.get_argument('end')
        change_min = self.get_argument('change_min')
        change_max = self.get_argument('change_max')
        stock_type = self.get_argument('stock_type')
        ascend = self.get_argument('ascend')
        ret, pd_frame = engine.get_queryhistory().query_history_change_stocks(markets,start, end, change_min, change_max, stock_type, ascend)
        print(ret)
        print(pd_frame)
        self.write(pd_frame.to_html())

class FTHistoryKlineHandler(RequestHandler):
    def set_default_headers(self):
        print("setting headers!!!")
        self.set_header("Access-Control-Allow-Origin", "*")  # 这个地方可以写域名
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

    def get(self):
        code = self.get_argument('code')
        start = self.get_argument('start')
        end = self.get_argument('end')
        dtype = self.get_argument('dtype')
        ret_list  = engine.get_mysqlservice().find_history_kline(code,dtype,start,end)
        col_list = ['code', 'time_key','open', 'close', 'high', 'low', 'pe_ratio', 'turnover_rate', 'volume', 'turnover', 'change_rate', 'last_close']
        pd_frame = pd.DataFrame(ret_list, columns=col_list)
        self.write(pd_frame.to_json())

class FTPlateListHandler(RequestHandler):
    def get(self):
        col_list = ['code', 'plate_name', 'plate_id']
        ret_list = engine.get_mysqlservice().find_plate_list()
        pd_frame = pd.DataFrame(ret_list, columns=col_list)
        self.write(pd_frame.to_json())

class FTPlateStockHandler(RequestHandler):
    def get(self):
        col_list = ['code', 'lot_size', 'stock_name','stock_owner','stock_child_type','stock_type','list_time','stock_id']
        ret_list = engine.get_mysqlservice().find_plate_stock()
        pd_frame = pd.DataFrame(ret_list, columns=col_list)
        self.write(pd_frame.to_json())


def path():
    return os.path.dirname(__file__)

#http://127.0.0.1:8888/queryhistory?markets=HK&start=2018-02-01&end=2018-05-30&change_min=1.0&change_max=100.0&stock_type=STOCK&ascend=True， 为什么没有数据
# http://127.0.0.1:8888/queryhistory?markets=HK&start=2017-01-05&end=2017-12-30&change_min=5.0&change_max=10.0&stock_type=STOCK&ascend=True
# http://127.0.0.1:8888/hk?code=US.NTES&dtype=hk&start=2017-01-05&end=2017-12-30
def make_app():
    return tornado.web.Application([
        (r"/hs",MainHandler),
        (r"/queryhistory",QueryHistoryHandler),
        (r"/hk",FTHistoryKlineHandler),
        (r"/plate", FTPlateListHandler),
        (r"/platestock", FTPlateStockHandler),
    ])


is_closing = False
engine = None

def signal_handler(signum, frame):
    global is_closing
    logging.info('exiting...')
    is_closing = True
    try_exit()


def signal_term_handler(*args):
    global is_closing
    logging.info('killed, exiting...')
    is_closing = True
    try_exit()

def try_exit():
    global is_closing
    if is_closing:
        # clean up here
        tornado.ioloop.IOLoop.current().stop()
        engine.stop()
        logging.info('exit success')

def main():
    global engine
    engine = QEEngine()

    app = make_app()
    setup_logging()
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_term_handler)
    server = tornado.httpserver.HTTPServer(app)
    server.bind(AppConfig.get_config().get('web', 'port'))
    server.start(0) # forks one process per cpu
    tornado.ioloop.PeriodicCallback(try_exit, 100).start()
    tornado.ioloop.IOLoop.current().start()

    engine.stop()


if __name__ == "__main__":
    main()