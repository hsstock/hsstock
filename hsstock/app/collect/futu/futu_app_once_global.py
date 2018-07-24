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

def job_once_global(worker):
    '''
    功能：获取一次性的全局数据
    :param worker:
    :return:
    '''
    global is_closing

    while not is_closing:
        begin = time.time()

        logging.info("fetching trading_days")
        # markets = enumclass_to_list(Market)
        # for market in markets:
        #     ret_code, ret_data = worker.get_trading_days(market)
        #     env.trading_days[market] = ret_data
        # if is_closing is True:
        #     break
        #
        # securitytypes = enumclass_to_list(SecurityType)
        # for market in markets:
        #     for securitytype in securitytypes:
        #         if is_closing is True:
        #             break
        #         ret_code, ret_data = worker.get_stock_basicinfo(market, securitytype)
        #         env.stock_basicinfos[market+'_'+securitytype]  = ret_data
        #         logging.info("fetching stock_baseinfo {}-{}".format(market,securitytype))
        # if is_closing is True:
        #     break

            # 多个的网关返回有问题？
            # worker.get_multiple_history_kline(['US.NTES','US.BABA'], '2018-06-20', '2018-06-25', KLType.K_DAY, AuType.QFQ)
            # if is_closing is True:
            #     break
            # worker.get_multiple_history_kline(['HK.00771','HK.00700'], '2018-06-20', '2018-06-25',
            #                                                           KLType.K_DAY, AuType.QFQ)
            # if is_closing is True:
            #      break
            #

        # plate_list = []
        # for market in markets:
        #     ret_code, ret_data = worker.get_plate_list(market)
        #     if ret_code is RET_OK:
        #         plate_list.append(ret_data)
        #         env.plates[market] = ret_data
        #         logging.info("fetching plate for {} market".format(market))
        # if is_closing is True:
        #     break
        #
        # for i in range(0,len(plate_list),1):
        #     for j in range(0, len(plate_list[i]), 1):
        #         plat_code = plate_list[i].iloc[j].code
        #         ret_code, ret_data = worker.get_plate_stock(plat_code)
        #         env.plate_stocks[plat_code]  = ret_data
        #         logging.info("fetching plate stock , currrent progress: {}-{}-{}".format(plat_code,i,j))
        #         time.sleep(FREQLIMIT[FREQ.TOTAL_SECONDS]/FREQLIMIT[FREQ.GET_PLATE_STOCK])
        # if is_closing is True:
        #     break
        #
        # ret_code, ret_data = worker.get_global_state()
        # env.global_state = ret_data
        # logging.info("fetching global state")
        # if is_closing is True:
        #     break

        codes = worker.storeservice.find_all_stockcodes()

        offset = 0
        limit = 200
        total = len(codes)
        while offset < total:
            print("offet:{} limit:{} partial codes:{}".format(offset, limit, codes[offset:offset + limit]))
            offset += limit
            worker.get_market_snapshot(codes[offset:offset + limit])
            if is_closing is True:
                break
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

def once_global_task(worker):
    tfn = MyThread('job_once_global',job_once_global,worker)
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
    once_global_task(lf)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_int_handler)
    #signal.signal(signal.SIGKILL, signal_term_handler)
    signal.signal(signal.SIGTERM, signal_term_handler)
    setup_logging()
    main()
    sched.start()


