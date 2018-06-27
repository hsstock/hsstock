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
        self.write(pd_frame.to_html())

def path():
    return os.path.dirname(__file__)

#http://127.0.0.1:8888/queryhistory?markets=HK&start=2018-02-01&end=2018-05-30&change_min=1.0&change_max=100.0&stock_type=STOCK&ascend=True， 为什么没有数据
# http://127.0.0.1:8888/queryhistory?markets=HK&start=2017-01-05&end=2017-12-30&change_min=5.0&change_max=10.0&stock_type=STOCK&ascend=True
def make_app():
    return tornado.web.Application([
        (r"/hs",MainHandler),
        (r"/queryhistory",QueryHistoryHandler)
    ])


is_closing = False
engine = None

def signal_handler(signum, frame):
    global is_closing
    logging.info('exiting...')
    is_closing = True

def try_exit():
    global is_closing
    if is_closing:
        # clean up here
        tornado.ioloop.IOLoop.current().stop()
        logging.info('exit success')

def main():
    global engine
    engine = QEEngine()

    app = make_app()
    setup_logging()
    signal.signal(signal.SIGINT, signal_handler)
    server = tornado.httpserver.HTTPServer(app)
    server.bind(AppConfig.get_config().get('web', 'port'))
    server.start(0) # forks one process per cpu
    tornado.ioloop.PeriodicCallback(try_exit, 100).start()
    tornado.ioloop.IOLoop.current().start()

    engine.stop()


if __name__ == "__main__":
    main()