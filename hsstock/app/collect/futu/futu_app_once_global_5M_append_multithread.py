# -*- coding: UTF-8 -*-
import logging
import signal
import time

from apscheduler.schedulers.blocking import BlockingScheduler

from hsstock.utils.app_logging import setup_logging
import hsstock.utils.decorator  as tick
from hsstock.utils.date_util import DateUtil
from hsstock.utils.threadutil import MyThread
from hsstock.utils.threadutil import MyThread2
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
from hsstock.model.mysql.ft_history_kline import FTHistoryKline


sched = BlockingScheduler()

is_closing = False
ctx  = None

def job_once_global_m5_append_multithread(*_args):
    '''
    线程工作：低频数据接口
    :return:
    '''
    global is_closing

    worker = _args[0][0]
    arr = _args[0][1]

    while not is_closing:
        begin = time.time()
        ret_arr = arr
        todayStr = DateUtil.getTodayStr()
        total = len(ret_arr)
        curr = 0
        for code, listing_date in ret_arr:
            curr += 1
            #1 - (1~2998包含)
            #2 - (2999~15918不含）
            #3 - （15918~18986不含）
            #4 - （18986~19430不含）default InnoDB,
            #5 -  (19430~21898不含) MyISAM engine,ft_history_kline_5
            #6 - (21898~24768不含) MyISAM engine,ft_history_kline_6
            #7 - (24768~26347不含） MyISAM engine, ft_history_kline_7
            #8 - (26347~27096不含) MyISAM engine, ft_history_kline_8， trigged by docker upgrade
            #9 - (27096~28123不含) MyISAM engine, ft_history_kline_9
            #10 - (28123~31918) MyISAM engine, ft_history_kline_10
            # ft_history_kline tale as the mrg_myisam

            logging.info("current fetching progress {}/{} ".format(curr,total))
            if curr < 1:
                continue



            # KLType.K_DAY
            start = None
            lastdate = worker.storeservice.find_lastdate(code)
            if lastdate is not None and lastdate.date() > listing_date:
                start = DateUtil.getDatetimeFutureStr( lastdate.date(),1 )
            else:
                start = DateUtil.date_toString(listing_date)
            end = todayStr
            gen = DateUtil.getNextHalfYear(DateUtil.string_toDate(start), DateUtil.string_toDate(end))
            b = time.time()
            while True:
                try:
                    end = next(gen)

                    if is_closing is True:
                        break

                    b2 = time.time()
                    worker.get_history_kline(code, start, end, ktype=KLType.K_DAY)
                    e2 = time.time()
                    logging.info(
                        "fetching {} K_DAY listing_date: {} start: {} end:{} cost time {}".format(code, listing_date, start, end, e2-b2))

                    start = DateUtil.getDatetimeFutureStr(DateUtil.string_toDate(end),1)
                    time.sleep(0.1)
                except StopIteration as e:
                    print(e)
                    break

            # KLType.K_5M
            start = None
            lastdate = worker.storeservice.find_lastdate_5M(code)

            if lastdate is not None and lastdate.date() > listing_date:
                start = DateUtil.getDatetimeFutureStr(lastdate.date(), 1)
            else:
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
                    worker.get_history_kline(code, start, end, ktype=KLType.K_5M)
                    e1 = time.time()
                    logging.info(
                        "fetching {} K_5M_LINE listing_date:{} start: {} end:{} cost time {}".format(code,
                                                                                                     listing_date,
                                                                                                     start, end,
                                                                                                     e1 - b1))
                    start = DateUtil.getDatetimeFutureStr(DateUtil.string_toDate(end), 1)
                    time.sleep(0.1)
                except StopIteration as e:
                    print(e)
                    break


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

def once_global_m5_task(thread_name,arr,worker):
    tfn = MyThread2(thread_name,job_once_global_m5_append_multithread,worker,arr)
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

    ret_arr = lf.storeservice.find_all_stocks()
    total_threads = 10
    step_length = int(len(ret_arr)/total_threads)
    mode = len(ret_arr)%total_threads
    for i in range(0,total_threads,1):
        lf = LF(ctx)
        thread_name = 'job_lf_{}'.format(i)

        start = i*step_length
        if i == (total_threads-1):
            end = start+step_length+mode
        else:
            end = start + step_length
        arr = ret_arr[start:end]

        once_global_m5_task(thread_name,arr,lf)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_int_handler)
    #signal.signal(signal.SIGKILL, signal_term_handler)
    signal.signal(signal.SIGTERM, signal_term_handler)
    setup_logging()
    main()
    sched.start()

    # ret_arr = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
    # total_threads = 6
    # step_length = int(len(ret_arr)/total_threads)
    # mode = len(ret_arr)%total_threads
    # for i in range(0,total_threads,1):
    #     start = i*step_length
    #     if i == (total_threads-1):
    #         end = start+step_length+mode
    #     else:
    #         end = start + step_length
    #     arr = ret_arr[start:end]
    #     print('index-{} arr:{}'.format(i,arr))