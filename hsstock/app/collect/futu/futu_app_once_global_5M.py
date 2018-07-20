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


sched = BlockingScheduler()

is_closing = False
ctx  = None

def job_once_global_m5(worker):
    '''
    线程工作：低频数据接口
    :return:
    '''
    global is_closing

    while not is_closing:
        markets = enumclass_to_list(Market)
        plate_list = []
        for market in markets:
            ret_code, ret_data = worker.get_plate_list(market)
            if ret_code is RET_OK:
                plate_list.append(ret_data)
        if is_closing is True:
            break

        plate_stock = []
        for i in range(0,len(plate_list),1):
            if is_closing is True:
                break
            for j in range(0, len(plate_list[i]), 1):
                print(plate_list[i].iloc[j].code)
                ret_code, ret_data = worker.get_plate_stock(plate_list[i].iloc[j].code)
                if ret_code is RET_OK:
                    plate_stock.append(ret_data)
                if is_closing is True:
                    break
                print('get_plate_stock current progress - {}.{}'.format(i,j))
                time.sleep(FREQLIMIT[FREQ.TOTAL_SECONDS] / FREQLIMIT[FREQ.GET_PLATE_LIST])

        for i in range(0,len(plate_stock),1):
            if is_closing is True:
                break
            for j in range(0, len(plate_stock[i]), 1):
                print(plate_stock[i].iloc[j].code)
                worker.get_history_kline(plate_stock[i].iloc[j].code, '2018-01-01','2018-07-17',ktype=KLType.K_5M)
                if is_closing is True:
                    break
                print('get_history_kline current progress - {}.{}'.format(i,j))
        break



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

def once_global_m5_task(worker):
    tfn = MyThread('job_lf',job_once_global_m5,worker)
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
    once_global_m5_task(lf)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_int_handler)
    #signal.signal(signal.SIGKILL, signal_term_handler)
    signal.signal(signal.SIGTERM, signal_term_handler)
    setup_logging()
    main()
    sched.start()