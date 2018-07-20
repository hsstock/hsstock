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
from hsstock.app.collect.environment import Environment


sched = BlockingScheduler()

is_closing = False
ctx  = None
env = Environment()

def job_once_custom(worker):
    '''
    功能：获取一次性的全局数据
    :param worker:
    :return:
    '''
    global is_closing

    while not is_closing:
        begin = time.time()

        # TODO , date as a para
        # 有问题，内部也是单个遍历
        # logging.info("fetching multiple history kline: {}".format(AppConfig.custom_ft_stocks))
        # worker.get_multiple_history_kline(AppConfig.custom_ft_stocks, '2018-06-20', '2018-07-20', KLType.K_DAY,AuType.NONE)
        # if is_closing is True:
        #     break

        for symbol in AppConfig.custom_ft_stocks:
            worker.get_history_kline(symbol, '2018-01-01', '2018-07-20', KLType.K_5M)
            worker.get_history_kline(symbol, '2018-01-01', '2018-07-20', KLType.K_DAY)
            if is_closing is True:
                break

        # 有问题， 网关要升级
        # logging.info("fetching autype: {}".format(AppConfig.custom_ft_stocks))
        # worker.get_autype_list(AppConfig.custom_ft_stocks)

        logging.info("fetching market snapshot: {}".format(AppConfig.custom_ft_stocks))
        worker.get_market_snapshot(AppConfig.custom_ft_stocks)
        if is_closing is True:
            break

        end = time.time()
        logging.info("fetching for one  period , cost time: {}".format((end-begin)))
        left = FREQLIMIT[FREQ.TOTAL_SECONDS] - end + begin
        if left > 0:
            time.sleep(left)

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

def once_custom_task(worker):
    tfn = MyThread('job_once_global',job_once_custom,worker)
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
    lf = LF(ctx)
    once_custom_task(lf)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_int_handler)
    #signal.signal(signal.SIGKILL, signal_term_handler)
    signal.signal(signal.SIGTERM, signal_term_handler)
    setup_logging()
    main()
    sched.start()