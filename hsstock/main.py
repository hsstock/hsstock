# -*- coding: UTF-8 -*-

import tornado.ioloop
import tornado.web
from tornado.web import RequestHandler
import os
import json

from hsstock.web.app_logging import setup_logging

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
    app = make_app()
    setup_logging()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
