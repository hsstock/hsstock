# -*- coding: UTF-8 -*-
import signal
import time
import random
import datetime
# from apscheduler.schedulers.blocking import BlockingScheduler

import hsstock.utils.logger as logger
import hsstock.utils.decorator  as tick
from hsstock.utils.date_util import DateUtil
from hsstock.utils.threadutil import MyThread
from hsstock.utils.threadutil import MyThread2
from hsstock.common.freqlimit import FreqLimit
from hsstock.common.constant import *
from hsstock.utils.lang_util import *
from hsstock.service.mysql_service import MysqlService
from hsstock.utils.mongodbutil import MongodbUtil
from hsstock.service.sinanews_service import SinanewsService
from hsstock.utils.app_config import AppConfig


# sched = BlockingScheduler()

is_closing = False

def job_once_global(*_args):
    '''
    :return:
    '''
    global is_closing

    store = _args[0][0]
    arr = _args[0][1]
    sinanewshistory = _args[0][2]

    while not is_closing:
        begin = time.time()
        ret_arr = arr

        total = len(ret_arr)
        curr = 0
        for code in ret_arr:
            curr += 1

            logger.info("current fetching entry progress {}/{} code:{} ".format(curr,total,code))
            if curr < 4:
                continue

            market = code[0:2]
            symbol = code[3:]

            sinanewshistory.clear_item_array()
            logger.info('Current Time:{}, code:{}, market:{}'.format(datetime.datetime.now(), symbol, market))

            page = 1
            type = '1'
            while page != -1:
                if is_closing:
                    break
                try:
                    if market == 'HK':
                        page,_ = sinanewshistory.get_hk_page(market, symbol, page)
                    if market == 'US':
                        page, type = sinanewshistory.get_us_page(market, symbol, page, type)
                    if market == 'SZ' or market == 'SH':
                        page,_ = sinanewshistory.get_chn_page(market, symbol, page)

                    items = sinanewshistory.get_item_array()
                    if len(items) > 0:
                        sinanewshistory.mongodbutil.insertItems(items)
                        # time.sleep(4 * random.random())
                        logger.info("store items to mongodb ...")
                    else:
                        logger.info("all items exists")
                except Exception as err:
                    time.sleep(4 * random.random())
                    logger.warning('my err:{}'.format(err))
                    page = -1

            if is_closing is True:
                break

        end = time.time()
        logger.info("fetching for one  period , cost time: {}".format((end - begin)))

        signal_int_handler(0,0)
        break



def signal_int_handler(signum, frame):
    global is_closing
    logger.info('exiting...')
    is_closing = True
    # sched.shutdown(True)


#SIGKILL 不可被捕获
# def signal_kill_handler():
#     global is_closing
#     logger.info('killed, exiting...')
#     is_closing = True
#     sched.shutdown(True)

def signal_term_handler(*args):
    global is_closing
    logger.info('killed, exiting...')
    is_closing = True
    # sched.shutdown(True)

def try_exit():
    global is_closing
    if is_closing:
        # clean up here
        logger.info('exit success')

def once_global_task(thread_name,arr,store,sinanewshistory):
    tfn = MyThread2(thread_name,job_once_global,store,arr,sinanewshistory)
    tfn.start()


def catch_all_entry_urls():
    storeservice = MysqlService()
    mongodbutil = MongodbUtil(AppConfig.mongodb_ip, AppConfig.mongodb_port, AppConfig.mongodb_collection)
    sinanewshistory = SinanewsService(mongodbutil)
    ret_arr = storeservice.find_all_stockcodes_exclude_nodata()
    thread_name = 'catch all stock entry url'
    once_global_task(thread_name,ret_arr, storeservice,sinanewshistory)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_int_handler)
    #signal.signal(signal.SIGKILL, signal_term_handler)
    signal.signal(signal.SIGTERM, signal_term_handler)
    catch_all_entry_urls()
    #sched.start()

