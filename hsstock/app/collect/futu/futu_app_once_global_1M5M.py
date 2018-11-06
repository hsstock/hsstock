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
    MAX_COUNT_ONE_TABLE = 8000000

    while not is_closing:
        begin = time.time()
        ret_arr = worker.storeservice.find_all_stocks()
        todayStr = DateUtil.getTodayStr()
        total = len(ret_arr)
        curr = 0

        tindex_kline = 1
        tindex_5M = 1
        tindex_1M = 1
        tindex_kline_count = 4207054
        tindex_5M_count = 4933842
        tindex_1M_count = 1990438

        for code, listing_date in ret_arr:
            curr += 1

            logging.info("current fetching progress {}/{} tindex_kline={} tindex_5M={} tindex_1M={} tindex_kline_count={} tindex_5M_count={} tindex_1M_count={}".format(curr,total, tindex_kline,tindex_5M,tindex_1M,tindex_kline_count,tindex_5M_count,tindex_1M_count))
            if curr < 2353:
                continue


            if listing_date.year == 1970:
                listing_date = listing_date.replace(year=1997)
            start = DateUtil.date_toString(listing_date)
            end = todayStr
            gen = DateUtil.getNextHalfYear(DateUtil.string_toDate(start), DateUtil.string_toDate(end))
            b = time.time()
            while True:
                try:
                    end = next(gen)

                    if is_closing is True:
                        break

                    b1 = time.time()
                    _,ret_data,_ = worker.get_history_kline(code,tindex_5M, start, end, ktype=KLType.K_5M)
                    if not isinstance(ret_data, str):
                        if len(ret_data) > 0:
                            tindex_5M_count += len(ret_data)
                    e1 = time.time()
                    logging.info(
                        "fetching {} K_5M_LINE listing_date:{} start: {} end:{} cost time {}".format(code, listing_date, start, end,e1-b1))

                    if is_closing is True:
                        break

                    b1 = time.time()
                    _, ret_data, _ = worker.get_history_kline(code, tindex_1M, start, end, ktype=KLType.K_1M)
                    if not isinstance(ret_data, str):
                        if len(ret_data) > 0:
                            tindex_1M_count += len(ret_data)
                    e1 = time.time()
                    logging.info(
                        "fetching {} K_1M_LINE listing_date:{} start: {} end:{} cost time {}".format(code, listing_date,
                                                                                                     start, end,
                                                                                                     e1 - b1))

                    if is_closing is True:
                        break

                    b2 = time.time()
                    _, ret_data, _ = worker.get_history_kline(code,tindex_kline, start, end, ktype=KLType.K_DAY)
                    if not isinstance(ret_data, str):
                        if len(ret_data) > 0:
                            tindex_kline_count += len(ret_data)
                    e2 = time.time()
                    logging.info(
                        "fetching {} K_DAY listing_date: {} start: {} end:{} cost time {}".format(code, listing_date, start, end, e2-b2))

                    start = DateUtil.getDatetimeFutureStr(DateUtil.string_toDate(end),1)
                except StopIteration as e:
                    print(e)
                    if tindex_5M_count > MAX_COUNT_ONE_TABLE:
                        tindex_5M += 1
                        tindex_5M_count = 0
                    if tindex_1M_count > MAX_COUNT_ONE_TABLE:
                        tindex_1M += 1
                        tindex_1M_count = 0
                    if tindex_kline_count > MAX_COUNT_ONE_TABLE:
                        tindex_kline += 1
                        tindex_kline_count = 0
                    break
                # if is_closing is True:
                #     break

            e = time.time()
            logging.info("position {} fetching {} const time {}".format(curr, code, e - b))

            if is_closing is True:
                break

        end = time.time()
        logging.info("fetching for one  period , cost time: {}".format((end - begin)))

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