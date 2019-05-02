# -*- coding: GBK -*-
import sys
import importlib
importlib.reload(sys)

import signal
import time
import random
import datetime
from apscheduler.schedulers.blocking import BlockingScheduler

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
from hsstock.service.futunews_service import FutunnService
from hsstock.utils.app_config import AppConfig



sched = BlockingScheduler()

is_closing = False
working = False
timerid = 'my_job_id'

def job_appender(*_args):
    '''
    :return:
    '''
    global is_closing
    global working
    global timerid

    working = True

    store = _args[0][0]
    arr = _args[0][1]
    sinanews = _args[0][2]

    logger.info('start crawl current news...')

    while not is_closing:
        begin = time.time()
        ret_arr = arr

        total = len(ret_arr)
        curr = 0
        for code in ret_arr:
            if is_closing:
                break

            curr += 1

            logger.info("current fetching entry progress {}/{} code:{} ".format(curr,total,code))
            if curr < 3061:
                continue

            market = code[0:2]
            symbol = code[3:]
            url = sinanews.generate_url(market, symbol)

            logger.info('Current Time:{}, code:{}, market:{}'.format(datetime.datetime.now(), symbol, market))

            try:
                sinanews.get_page(market,symbol, url)
                items = sinanews.get_item_array()
                if len(items) > 0:
                    sinanews.mongodbutil.insertItems(items)
                    logger.info("store items to mongodb ...")
                else:
                    logger.info("all items exists")
            except Exception as err:
                time.sleep(4 * random.random())
                logger.warning(err)

            if is_closing is True:
                break

        working = False
        if not is_closing:
            sched.add_job(scheduled_job, 'interval', seconds=1, id=timerid)

        end = time.time()
        logger.info("fetching for one  period , cost time: {}".format((end - begin)))

        break


def job_info_appender(*_args):
    '''
    :return:
    '''
    global is_closing
    global working
    global timerid

    working = True

    store = _args[0][0]
    arr = _args[0][1]
    futunews = _args[0][2]

    logger.info('start crawl current futu news...')

    while not is_closing:
        if is_closing:
            break

        begin = time.time()

        logger.info('Current Time:{}, info'.format(datetime.datetime.now()))

        try:
            ret_code, ret_data = futunews.get_info()
            items = futunews.get_item_array()
            if len(items) > 0:
                futunews.mongodbutil.insertItems(items)
                logger.info("store items to mongodb ...")
            else:
                logger.info("all items exists")
        except Exception as err:
            time.sleep(4 * random.random())
            logger.warning(err)

        if is_closing is True:
            break

        working = False
        if not is_closing:
            sched.add_job(scheduled_job, 'interval', seconds=random.randint(10,20), id=timerid)

        end = time.time()
        logger.info("fetching for one  period , cost time: {}".format((end - begin)))

        break

def job_info_byapi_appender(*_args):
    '''
    :return:
    '''
    global is_closing
    global working
    global timerid

    working = True

    store = _args[0][0]
    arr = _args[0][1]
    futunews = _args[0][2]

    logger.info('start crawl current futu news...')

    while not is_closing:
        if is_closing:
            break

        begin = time.time()

        logger.info('Current Time:{}, info'.format(datetime.datetime.now()))

        try:
            ret_code, ret_data = futunews.get_futunn_news()

        except Exception as err:
            time.sleep(4 * random.random())
            logger.warning(err)

        if is_closing is True:
            break


        end = time.time()
        logger.info("fetching for one  period , cost time: {}".format((end - begin)))

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

def once_appender_task(thread_name,arr,store,futunewsshistory):
    tfn = MyThread2(thread_name,job_info_appender,store,arr,futunewsshistory)
    tfn.start()

def once_appender_byapi_task(thread_name,arr,store,futunewsshistory):
    tfn = MyThread2(thread_name,job_info_byapi_appender,store,arr,futunewsshistory)
    tfn.start()



storeservice = MysqlService()
mongodbutil = MongodbUtil(AppConfig.mongodb_ip, AppConfig.mongodb_port, AppConfig.mongodb_collection)
futunews = FutunnService(mongodbutil)
ret_arr = storeservice.find_all_stockcodes_exclude_nodata()
thread_name = 'catch all stock entry url'

def catch_lastest_news():
    ret_arr = storeservice.find_all_stockcodes_exclude_nodata()
    once_appender_task(thread_name,ret_arr, storeservice,futunews)

def catch_futunn_news():
    ret_arr = storeservice.find_all_stockcodes_exclude_nodata()
    once_appender_byapi_task(thread_name, ret_arr, storeservice, futunews)


def scheduled_job():
    logger.info('scheduled_job..')
    if working == False:
        sched.remove_job(timerid)
        catch_lastest_news()
        #catch_futunn_news()
    else:
        logger.info('pre-timer is working')



if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_int_handler)
    #signal.signal(signal.SIGKILL, signal_term_handler)

    logger.info('Starting time: {}'.format(datetime.datetime.now()))
    sched.add_job(scheduled_job, 'interval', max_instances=2, seconds=1, id=timerid)
    signal.signal(signal.SIGTERM, signal_term_handler)
    sched.start()
    logger.info('Ending time: {}'.format(datetime.datetime.now()))
