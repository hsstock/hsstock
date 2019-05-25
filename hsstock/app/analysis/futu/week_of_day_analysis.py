# -*- coding: UTF-8 -*-
import logging
import signal
import time
import numpy as np

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


sched = BlockingScheduler()

is_closing = False
ctx  = None

# def job_once_global_day_analysis(*_args):
#     '''
#     线程工作：低频数据接口
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
#         todayStr = DateUtil.getTodayStr()
#         for code, listing_date in ret_arr:
#             curr += 1
#
#             logging.info("current fetching progress {}/{} code:{} ".format(curr, total, code))
#             if curr <  0:
#                 continue
#
#             b1 = time.time()
#
#             ret_list = worker.storeservice.find_history_kline(code, 'hk', listing_date, todayStr)
#             if len(ret_list) <= 0:
#                 logging.info(
#                     "fetching {} K_LINE, but no data".format(code))
#                 continue
#
#             col_list = ['code', 'time_key', 'open', 'close', 'high', 'low', 'pe_ratio', 'turnover_rate', 'volume',
#                         'turnover', 'change_rate', 'last_close']
#             data = pd.DataFrame(ret_list, columns=col_list)
#             data['position']=np.where( data.change_rate > 0.0, 1, 0)
#             #data['ups_downs'] = np.where(data.change_rate > 0.0, data.close-data.open, data.open-data.close)
#             data.insert(loc=0, column='date_week', value=data.apply(lambda x: DateUtil.week_of_date(x['time_key']), axis='columns'))
#             xt = pd.crosstab(data.date_week,data.position)
#             xt_pct = xt.div(xt.sum(1).astype(float), axis=0)
#
#             #xt2 = pd.crosstab(data.date_week,data.ups_downs)
#             #xt_pct2 = xt2.div(xt2.sum(1).astype(float), axis=0)
#
#             add_list = []
#             #col_list = ['code','up_count','down_count','total_ups','total_downs','up_probability','down_probability','week_of_day']
#             col_list = ['code', 'up_count', 'down_count', 'up_probability', 'down_probability', 'week_of_day']
#             count =  0
#             for item in xt:
#                 count += 1
#             if count == 2:
#                 for week_of_day in range(0,5,1):
#                     try:
#                         if xt[0][week_of_day] is None or xt[1] is None or xt[1][week_of_day] is None:
#                             continue
#                     except KeyError as err:
#                         logging.error("OS|error: {0}".format(err))
#                         continue
#
#                     # try:
#                     #     if xt2[0][week_of_day] is None or xt2[1] is None or xt2[1][week_of_day] is None:
#                     #         continue
#                     # except KeyError as err:
#                     #     logging.error("OS|error: {0}".format(err))
#                     #     continue
#                     up_count = xt[1][week_of_day]
#                     down_count = xt[0][week_of_day]
#                     up_probability = xt_pct[1][week_of_day]
#                     down_probability = xt_pct[0][week_of_day]
#
#                     # total_ups = xt_pct2[1][week_of_day]
#                     # total_downs = xt_pct2[0][week_of_day]
#
#                     #add_list.append((code,up_count,down_count,up_probability,down_probability,total_ups,total_downs,week_of_day))
#                     add_list.append((code, up_count, down_count, up_probability, down_probability, week_of_day))
#                 table = 'ft_stat_week_probability2'
#                 worker.storeservice.insert_many(table, pd.DataFrame(add_list, columns=col_list))
#
#
#             e1 = time.time()
#             logging.info(
#                 "fetching {} K_LINE listing_date:{} start: {} end:{} cost time {}".format(code, listing_date, listing_date,
#                                                                                            todayStr, e1 - b1))
#
#             if is_closing is True:
#                 break
#
#         end = time.time()
#         logging.info("fetching for one  period , cost time: {}".format((end - begin)))
#         break


def job_once_global_quater_analysis(*_args):
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

        total = len(ret_arr)
        curr = 0
        todayStr = DateUtil.getTodayStr()
        for code, listing_date in ret_arr:
            curr += 1

            logging.info("current fetching progress {}/{} code:{} ".format(curr, total, code))
            if curr <  0:
                continue

            b1 = time.time()

            ret_list = worker.storeservice.find_history_kline(code, 'hk', listing_date, todayStr)
            if len(ret_list) <= 0:
                logging.info(
                    "fetching {} K_LINE, but no data".format(code))
                continue

            col_list = ['code', 'time_key', 'open', 'close', 'high', 'low', 'pe_ratio', 'turnover_rate', 'volume',
                        'turnover', 'change_rate', 'last_close']
            data = pd.DataFrame(ret_list)
            data = pd.DataFrame(ret_list, index=data[1], columns=col_list)
            data = data.resample('91D').mean()
            data['position'] = np.where(data.change_rate > 0.0, 1,0)
            data['period'] = data.index.quarter

            xt = pd.crosstab(data.period,data.position)
            xt_pct = xt.div(xt.sum(1).astype(float), axis=0)

            add_list = []
            col_list = ['code', 'up_count', 'down_count', 'up_probability', 'down_probability', 'period','ptype']
            count =  0
            for item in xt:
                count += 1
            if count == 2:
                for p in range(1,5,1):
                    try:
                        if xt[0][p] is None or xt[1] is None or xt[1][p] is None:
                            continue
                    except KeyError as err:
                        logging.error("OS|error: {0}".format(err))
                        continue

                    up_count = xt[1][p]
                    down_count = xt[0][p]
                    up_probability = xt_pct[1][p]
                    down_probability = xt_pct[0][p]

                    add_list.append((code, up_count, down_count, up_probability, down_probability, p,'quarter'))
                table = 'ft_stat_probability'
                worker.storeservice.insert_many(table, pd.DataFrame(add_list, columns=col_list))


            e1 = time.time()
            logging.info(
                "fetching {} K_LINE listing_date:{} start: {} end:{} cost time {}".format(code, listing_date, listing_date,
                                                                                           todayStr, e1 - b1))

            if is_closing is True:
                break

        end = time.time()
        logging.info("fetching for one  period , cost time: {}".format((end - begin)))
        break


def job_once_global_month_analysis(*_args):
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

        total = len(ret_arr)
        curr = 0
        todayStr = DateUtil.getTodayStr()
        for code, listing_date in ret_arr:
            curr += 1

            logging.info("current fetching progress {}/{} code:{} ".format(curr, total, code))
            if curr <  9608:
                continue

            b1 = time.time()

            ret_list = worker.storeservice.find_history_kline(code, 'hk', listing_date, todayStr)
            if len(ret_list) <= 0:
                logging.info(
                    "fetching {} K_LINE, but no data".format(code))
                continue

            col_list = ['code', 'time_key', 'open', 'close', 'high', 'low', 'pe_ratio', 'turnover_rate', 'volume',
                        'turnover', 'change_rate', 'last_close']
            data = pd.DataFrame(ret_list)
            data = pd.DataFrame(ret_list, index=data[1], columns=col_list)
            data = data.resample('31D').mean()
            data['position'] = np.where(data.change_rate > 0.0, 1,0)
            data['period'] = data.index.month

            xt = pd.crosstab(data.period,data.position)
            xt_pct = xt.div(xt.sum(1).astype(float), axis=0)

            add_list = []
            col_list = ['code', 'up_count', 'down_count', 'up_probability', 'down_probability', 'period','ptype']
            count =  0
            for item in xt:
                count += 1
            if count == 2:
                for p in range(1,13,1):
                    try:
                        if xt[0][p] is None or xt[1] is None or xt[1][p] is None:
                            continue
                    except KeyError as err:
                        logging.error("OS|error: {0}".format(err))
                        continue

                    up_count = xt[1][p]
                    down_count = xt[0][p]
                    up_probability = xt_pct[1][p]
                    down_probability = xt_pct[0][p]

                    add_list.append((code, up_count, down_count, up_probability, down_probability, p,'month'))
                table = 'ft_stat_probability'
                worker.storeservice.insert_many(table, pd.DataFrame(add_list, columns=col_list))


            e1 = time.time()
            logging.info(
                "fetching {} K_LINE listing_date:{} start: {} end:{} cost time {}".format(code, listing_date, listing_date,
                                                                                           todayStr, e1 - b1))

            if is_closing is True:
                break

        end = time.time()
        logging.info("fetching for one  period , cost time: {}".format((end - begin)))
        break


def job_once_global_week_analysis(*_args):
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

        total = len(ret_arr)
        curr = 0
        todayStr = DateUtil.getTodayStr()
        for code, listing_date in ret_arr:
            curr += 1

            logging.info("current fetching progress {}/{} code:{} ".format(curr, total, code))
            if curr <  0:
                continue

            b1 = time.time()

            ret_list = worker.storeservice.find_history_kline(code, 'hk', listing_date, todayStr)
            if len(ret_list) <= 0:
                logging.info(
                    "fetching {} K_LINE, but no data".format(code))
                continue

            col_list = ['code', 'time_key', 'open', 'close', 'high', 'low', 'pe_ratio', 'turnover_rate', 'volume',
                        'turnover', 'change_rate', 'last_close']
            data = pd.DataFrame(ret_list)
            data = pd.DataFrame(ret_list, index=data[1], columns=col_list)
            data = data.resample('7D').mean()
            data['position'] = np.where(data.change_rate > 0.0, 1,0)
            data['period'] = data.index.week

            xt = pd.crosstab(data.period,data.position)
            xt_pct = xt.div(xt.sum(1).astype(float), axis=0)

            add_list = []
            col_list = ['code', 'up_count', 'down_count', 'up_probability', 'down_probability', 'period','ptype']
            count =  0
            for item in xt:
                count += 1
            if count == 2:
                for p in range(1,53,1):
                    try:
                        if xt[0][p] is None or xt[1] is None or xt[1][p] is None:
                            continue
                    except KeyError as err:
                        logging.error("OS|error: {0}".format(err))
                        continue

                    up_count = xt[1][p]
                    down_count = xt[0][p]
                    up_probability = xt_pct[1][p]
                    down_probability = xt_pct[0][p]

                    add_list.append((code, up_count, down_count, up_probability, down_probability, p,'week'))
                table = 'ft_stat_probability'
                worker.storeservice.insert_many(table, pd.DataFrame(add_list, columns=col_list))


            e1 = time.time()
            logging.info(
                "fetching {} K_LINE listing_date:{} start: {} end:{} cost time {}".format(code, listing_date, listing_date,
                                                                                           todayStr, e1 - b1))

            if is_closing is True:
                break

        end = time.time()
        logging.info("fetching for one  period , cost time: {}".format((end - begin)))
        break

def job_once_global_day_analysis(*_args):
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

        total = len(ret_arr)
        curr = 0
        todayStr = DateUtil.getTodayStr()
        for code, listing_date in ret_arr:
            curr += 1

            logging.info("current fetching progress {}/{} code:{} ".format(curr, total, code))
            if curr <  0:
                continue

            b1 = time.time()

            ret_list = worker.storeservice.find_history_kline(code, 'hk', listing_date, todayStr)
            if len(ret_list) <= 0:
                logging.info(
                    "fetching {} K_LINE, but no data".format(code))
                continue

            col_list = ['code', 'time_key', 'open', 'close', 'high', 'low', 'pe_ratio', 'turnover_rate', 'volume',
                        'turnover', 'change_rate', 'last_close']
            data = pd.DataFrame(ret_list, columns=col_list)
            data['position']=np.where( data.change_rate > 0.0, 1, 0)
            data.insert(loc=0, column='period', value=data.apply(lambda x: x['time_key'].dayofweek, axis='columns'))
            xt = pd.crosstab(data.period,data.position)
            xt_pct = xt.div(xt.sum(1).astype(float), axis=0)

            add_list = []
            col_list = ['code', 'up_count', 'down_count', 'up_probability', 'down_probability', 'period','ptype']
            count =  0
            for item in xt:
                count += 1
            if count == 2:
                for week_of_day in range(0,5,1):
                    try:
                        if xt[0][week_of_day] is None or xt[1] is None or xt[1][week_of_day] is None:
                            continue
                    except KeyError as err:
                        logging.error("OS|error: {0}".format(err))
                        continue

                    up_count = xt[1][week_of_day]
                    down_count = xt[0][week_of_day]
                    up_probability = xt_pct[1][week_of_day]
                    down_probability = xt_pct[0][week_of_day]

                    add_list.append((code, up_count, down_count, up_probability, down_probability, week_of_day,'day'))
                table = 'ft_stat_probability'
                worker.storeservice.insert_many(table, pd.DataFrame(add_list, columns=col_list))


            e1 = time.time()
            logging.info(
                "fetching {} K_LINE listing_date:{} start: {} end:{} cost time {}".format(code, listing_date, listing_date,
                                                                                           todayStr, e1 - b1))

            if is_closing is True:
                break

        end = time.time()
        logging.info("fetching for one  period , cost time: {}".format((end - begin)))
        break


def get_minute_index(dt,period):
    d = dt.date()
    t = dt.time()
    hour = dt.time().hour
    minute = dt.time().minute

    return (hour - 9) * 60/period + minute/period

def job_once_global_5m_analysis(*_args):
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

        total = len(ret_arr)
        curr = 0
        todayStr = DateUtil.getTodayStr()
        for code, listing_date in ret_arr:
            curr += 1

            logging.info("current fetching progress {}/{} code:{} ".format(curr, total, code))
            if curr <  26243:
                continue

            b1 = time.time()

            ret_list = worker.storeservice.find_history_kline(code, 'hk_5m', listing_date, todayStr)
            if len(ret_list) <= 0:
                logging.info(
                    "fetching {} K_LINE, but no data".format(code))
                continue

            col_list = ['code', 'time_key', 'open', 'close', 'high', 'low', 'pe_ratio', 'turnover_rate', 'volume',
                        'turnover', 'change_rate', 'last_close']
            data = pd.DataFrame(ret_list, columns=col_list)
            data['position']=np.where( data.change_rate > 0.0, 1, 0)
            data.insert(loc=0, column='period', value=data.apply(lambda x: get_minute_index(x['time_key'],5), axis='columns'))
            xt = pd.crosstab(data.period,data.position)
            xt_pct = xt.div(xt.sum(1).astype(float), axis=0)

            add_list = []
            col_list = ['code', 'up_count', 'down_count', 'up_probability', 'down_probability', 'period','ptype']
            count =  0
            for item in xt:
                count += 1
            if count == 2:
                for week_of_day in range(0,97,1):
                    try:
                        if xt[0][week_of_day] is None or xt[1] is None or xt[1][week_of_day] is None:
                            continue
                    except KeyError as err:
                        logging.error("OS|error: {0}".format(err))
                        continue

                    up_count = xt[1][week_of_day]
                    down_count = xt[0][week_of_day]
                    up_probability = xt_pct[1][week_of_day]
                    down_probability = xt_pct[0][week_of_day]

                    add_list.append((code, up_count, down_count, up_probability, down_probability, week_of_day,'5m'))
                table = 'ft_stat_probability'
                worker.storeservice.insert_many(table, pd.DataFrame(add_list, columns=col_list))


            e1 = time.time()
            logging.info(
                "fetching {} K_LINE listing_date:{} start: {} end:{} cost time {}".format(code, listing_date, listing_date,
                                                                                           todayStr, e1 - b1))

            if is_closing is True:
                break

        end = time.time()
        logging.info("fetching for one  period , cost time: {}".format((end - begin)))
        break


def job_once_global_1m_analysis(*_args):
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

        total = len(ret_arr)
        curr = 0
        todayStr = DateUtil.getTodayStr()
        for code, listing_date in ret_arr:
            curr += 1

            logging.info("current fetching progress {}/{} code:{} ".format(curr, total, code))
            if curr <  0:
                continue

            b1 = time.time()

            ret_list = worker.storeservice.find_history_kline(code, 'hk_1m', listing_date, todayStr)
            if len(ret_list) <= 0:
                logging.info(
                    "fetching {} K_LINE, but no data".format(code))
                continue

            col_list = ['code', 'time_key', 'open', 'close', 'high', 'low', 'pe_ratio', 'turnover_rate', 'volume',
                        'turnover', 'change_rate', 'last_close']
            data = pd.DataFrame(ret_list, columns=col_list)
            data['position']=np.where( data.change_rate > 0.0, 1, 0)
            data.insert(loc=0, column='period', value=data.apply(lambda x: get_minute_index(x['time_key'],1), axis='columns'))
            xt = pd.crosstab(data.period,data.position)
            xt_pct = xt.div(xt.sum(1).astype(float), axis=0)

            add_list = []
            col_list = ['code', 'up_count', 'down_count', 'up_probability', 'down_probability', 'period','ptype']
            count =  0
            for item in xt:
                count += 1
            if count == 2:
                for week_of_day in range(0,481,1):
                    try:
                        if xt[0][week_of_day] is None or xt[1] is None or xt[1][week_of_day] is None:
                            continue
                    except KeyError as err:
                        logging.error("OS|error: {0}".format(err))
                        continue

                    up_count = xt[1][week_of_day]
                    down_count = xt[0][week_of_day]
                    up_probability = xt_pct[1][week_of_day]
                    down_probability = xt_pct[0][week_of_day]

                    add_list.append((code, up_count, down_count, up_probability, down_probability, week_of_day,'1m'))
                table = 'ft_stat_probability'
                worker.storeservice.insert_many(table, pd.DataFrame(add_list, columns=col_list))


            e1 = time.time()
            logging.info(
                "fetching {} K_LINE listing_date:{} start: {} end:{} cost time {}".format(code, listing_date, listing_date,
                                                                                           todayStr, e1 - b1))

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
    if ctx is not None:
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
    if ctx is not None:
        ctx.stop()
        ctx.close()
    sched.shutdown(True)

def try_exit():
    global is_closing
    if is_closing:
        # clean up here
        logging.info('exit success')

def once_global_m5_task(thread_name,arr,worker):
    #tfn = MyThread2(thread_name, job_once_global_day_analysis, worker, arr)
    #tfn = MyThread2(thread_name, job_once_global_quater_analysis, worker, arr)
    #tfn = MyThread2(thread_name, job_once_global_month_analysis, worker, arr)
    #tfn = MyThread2(thread_name, job_once_global_week_analysis, worker, arr)
    #tfn = MyThread2(thread_name, job_once_global_day_analysis, worker, arr)
    #tfn = MyThread2(thread_name, job_once_global_5m_analysis, worker, arr)
    tfn = MyThread2(thread_name, job_once_global_1m_analysis, worker, arr)


    tfn.start()

def gen_one_worker():
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
    return lf

#@sched.scheduled_job('cron',day_of_week='mon-fri',hour='17', minute='05',second='00')
def analysis_chs():
    worker = gen_one_worker()
    ret_arr = worker.storeservice.find_chs_stocks(True)
    thread_name = 'analysis for chs market'
    once_global_m5_task(thread_name, ret_arr, worker)

# hour='09'
# minute='05'
# @sched.scheduled_job('cron',day_of_week='tue-sat',hour=hour, minute=minute,second='00')
def analysis_us():
    worker = gen_one_worker()
    ret_arr = worker.storeservice.find_chs_stocks(False)
    thread_name = 'analysis for us market'
    once_global_m5_task(thread_name,ret_arr, worker)


def analysis():
    worker = gen_one_worker()
    ret_arr = worker.storeservice.find_chs_stocks(False)
    ret_arr2 = worker.storeservice.find_chs_stocks(True)
    thread_name = 'analysis for us market'
    once_global_m5_task(thread_name,ret_arr + ret_arr2, worker)


if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_int_handler)
    #signal.signal(signal.SIGKILL, signal_term_handler)
    signal.signal(signal.SIGTERM, signal_term_handler)
    setup_logging()
    #analysis_chs()
    #analysis_us()
    analysis()

    sched.start()

