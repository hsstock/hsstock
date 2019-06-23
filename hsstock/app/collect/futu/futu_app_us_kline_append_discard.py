# -*- coding: UTF-8 -*-
import logging
import signal
import time

from apscheduler.schedulers.blocking import BlockingScheduler

from hsstock.utils.app_logging import setup_logging
from hsstock.utils.date_util import DateUtil
from hsstock.utils.threadutil import MyThread2
from hsstock.utils.app_config import AppConfig
from hsstock.service.trade_service import *

from hsstock.service.tx_service import TXService

sched = BlockingScheduler()

is_closing = False

def append_one_stock(service,code,dtype,listing_date):
    '''

    :param worker:
    :param code:
    :param dtype:
    :param last_fetchdate:
    :param listing_date:
    :return:
    '''
    global is_closing
    todayStr = DateUtil.getTodayStr()
    last_fetchdate = DateUtil.string_toDate('2018-08-02')

    start = None
    ld, tindex = service.storeservice.find_lastdate_and_tindex(code, dtype)
    lastdate = last_fetchdate if ld == None else ld
    if lastdate is not None and lastdate.date() > listing_date:
        start = DateUtil.getDatetimeFutureStr(lastdate.date(), 1)
    else:
        # if listing_date.year == 1970:
        #     listing_date = listing_date.replace(year=1997)
        # start = DateUtil.date_toString(listing_date)
        start = DateUtil.date_toString(last_fetchdate)
    end = todayStr
    gen = DateUtil.getNextHalfYear(DateUtil.string_toDate(start), DateUtil.string_toDate(end))
    while True:
        try:
            end = next(gen)

            if is_closing is True:
                break

            b2 = time.time()
            service.get_history_data('.' + code[3:], 100)

            # _, _, lastest_date = service.get_history_data('TSLA',100)
            # if lastest_date is not None:
            #     service.storeservice.update_lastdate(code, dtype, DateUtil.string_toDatetime(lastest_date))
            # e2 = time.time()
            # logging.info(
            #     "fetching {} dtype {}  listing_date: {} start: {} end:{} cost time {}".format(code, dtype, listing_date, start,
            #                                                                               end, e2 - b2))

            start = DateUtil.getDatetimeFutureStr(DateUtil.string_toDate(end), 1)
        except StopIteration as e:
            print(e)
            break

def job_history_append(*_args):
    '''
    线程工作：低频数据接口
    :return:
    '''
    global is_closing

    service = _args[0][0]
    arr = _args[0][1]

    while not is_closing:
        begin = time.time()
        ret_arr = arr

        total = len(ret_arr)
        curr = 0
        for code, listing_date in ret_arr:
            curr += 1

            logging.info("current fetching progress {}/{} code:{} ".format(curr,total,code))
            if curr < 1:
                continue

            b = time.time()

            # KLType.K_DAY
            append_one_stock(service,code,'hk', listing_date)


            e = time.time()
            logging.info("position {} fetching {} const time {}".format(curr, code, e - b))

            time.sleep(1)
            if is_closing is True:
                break

        end = time.time()
        logging.info("fetching for one  period , cost time: {}".format((end - begin)))

        break

# def job_setup_lastdate(*_args):
#     '''
#     线程工作：init the field lastdate in sys_sharding
#     :return:
#     '''
#     global is_closing
#
#     worker = _args[0][0]
#     arr = _args[0][1]
#
#     while not is_closing:
#         begin = time.time()
#         ret_arr = arr
#
#         total = len(ret_arr)
#         curr = 0
#         for code, listing_date in ret_arr:
#             curr += 1
#
#             logging.info("current fetching progress {}/{} code:{} ".format(curr,total,code))
#             if curr < 2584:
#                 continue
#
#             # KLType.K_DAY
#             ld = worker.storeservice.find_lastdate_from_origin(code,'hk')
#             worker.storeservice.update_lastdate(code, 'hk', ld)
#
#             ld = worker.storeservice.find_lastdate_from_origin(code,'hk_5m')
#             worker.storeservice.update_lastdate(code, 'hk_5m', ld)
#
#             ld = worker.storeservice.find_lastdate_from_origin(code, 'hk_1m')
#             worker.storeservice.update_lastdate(code, 'hk_1m', ld)
#
#
#         end = time.time()
#         logging.info("fetching for one  period , cost time: {}".format((end - begin)))
#
#         break



def signal_int_handler(signum, frame):
    global is_closing
    logging.info('exiting...')
    is_closing = True
    sched.shutdown(True)


#SIGKILL 不可被捕获
# def signal_kill_handler():
#     global is_closing
#     logging.info('killed, exiting...')
#     is_closing = True
#     sched.shutdown(True)

def signal_term_handler(*args):
    global is_closing
    logging.info('killed, exiting...')
    is_closing = True
    sched.shutdown(True)

def try_exit():
    global is_closing
    if is_closing:
        # clean up here
        logging.info('exit success')

def once_task(thread_name, arr, service):
    tfn = MyThread2(thread_name,job_history_append,service,arr)
    tfn.start()


@sched.scheduled_job('cron',day_of_week='mon-fri',hour='17', minute='05',second='00')
def download_chs():
    worker = gen_one_worker()
    ret_arr = worker.storeservice.find_chs_stocks(True)
    thread_name = 'crawler for chs market'
    once_task(thread_name, ret_arr, worker)

hour='09'
minute='05'
@sched.scheduled_job('cron',day_of_week='tue-sat',hour=hour, minute=minute,second='00')
def download_us():
    tx = TXService()
    ret_arr = tx.storeservice.find_chs_stocks(False)
    thread_name = 'crawler for us market'
    once_task(thread_name, ret_arr, tx)

# def setup_lastdate():
#     tx = TXService()
#     ret_arr = tx.storeservice.find_all_stocks()
#
#     thread_name = 'setup lastdate thread...'
#     once_task(thread_name, ret_arr, worker)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_int_handler)
    #signal.signal(signal.SIGKILL, signal_term_handler)
    signal.signal(signal.SIGTERM, signal_term_handler)
    setup_logging()
    download_us()
    sched.start()

    #setup_lastdate()

