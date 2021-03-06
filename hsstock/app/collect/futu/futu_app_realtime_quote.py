# -*- coding: UTF-8 -*-
import logging
import signal
import time

from apscheduler.schedulers.blocking import BlockingScheduler

from hsstock.utils.app_logging import setup_logging
import hsstock.utils.decorator  as tick
from hsstock.utils.date_util import DateUtil
from hsstock.utils.threadutil import MyThread
from hsstock.utils.app_config import AppConfig
import hsstock.futuquant as ft
from hsstock.futuquant.common.constant import *
from hsstock.utils.app_config import AppConfig
from hsstock.service.quote_service import LF
from hsstock.service.quote_service import HF
from hsstock.common.freqlimit import FreqLimit
from hsstock.common.constant import *
from hsstock.service.quote_service import Subscribe
from hsstock.service.trade_service import *
from hsstock.utils.lang_util import *
from hsstock.utils.app_config import AppConfig


sched = BlockingScheduler()

is_closing = False
ctx  = None

def job_realtime_quote(worker):
    '''
    线程工作：高频数据接口
    :return:
    '''
    global is_closing


    worker.subservice.subscribe(AppConfig.custom_ft_stocks, [SubType.TICKER, SubType.QUOTE, SubType.ORDER_BOOK, SubType.RT_DATA, SubType.BROKER])

    worker.ctx.set_handler(HSStockQuoteHandler())
    worker.ctx.set_handler(HSOrderBookHandler())
    worker.ctx.set_handler(HSCurKlineHandler())
    worker.ctx.set_handler(HSTickerHandler())
    worker.ctx.set_handler(HSRTDataHandler())
    worker.ctx.set_handler(HSBrokerHandler())


def signal_int_handler(signum, frame):
    global is_closing
    global ctx
    logging.info('exiting...')
    is_closing = True
    ctx.stop()
    ctx.close()
    sched.shutdown(True)


#SIGKILL 不可被捕获
# def signal_kill_handler():
#     global is_closing
#     logging.info('killed, exiting...')
#     is_closing = True
#     sched.shutdown(True)

def signal_term_handler(*args):
    global is_closing
    global ctx
    logging.info('killed, exiting...')
    is_closing = True
    ctx.stop()
    ctx.close()
    sched.shutdown(True)

def try_exit():
    global is_closing
    if is_closing:
        # clean up here
        logging.info('exit success')

def realtime_quote_task(worker):
    tfn = MyThread('realtime_quote_task', job_realtime_quote,worker)
    tfn.start()


def main():
    global ctx
    config = AppConfig.get_config()
    total = config.get('quota', 'total')
    kline = config.get('quota', 'kline')
    tiker = config.get('quota', 'ticker')
    quote = config.get('quota', 'quote')
    order_book = config.get('quota', 'order_book')
    rt_data = config.get('quota', 'rt_data')
    broker = config.get('quota', 'broker')

    ctx = ft.OpenQuoteContext(config.get('ftserver', 'host'), int(config.get('ftserver', 'port')))
    ctx.start()
    sub = Subscribe(ctx, total, kline, tiker, quote, order_book, rt_data, broker)
    hf = HF(ctx, sub)
    realtime_quote_task(hf)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_int_handler)
    #signal.signal(signal.SIGKILL, signal_term_handler)
    signal.signal(signal.SIGTERM, signal_term_handler)
    setup_logging()
    main()
    sched.start()