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
from hsstock.model.mysql.ft_kline import FTHistoryKlineAll


sched = BlockingScheduler()

is_closing = False
ctx  = None

jump_pd = pd.DataFrame()

def job_once_global_day_analysis(*_args):
    '''
    线程工作：低频数据接口
    :return:
    '''
    global is_closing
    global jump_pd

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
            if curr < 1:
                continue

            b1 = time.time()

            ret_list = worker.storeservice.find_history_kline(code, 'hk', listing_date, todayStr)
            if len(ret_list) <= 0:
                logging.info(
                    "fetching {} K_LINE, but no data".format(code))
                continue

            col_list = ['code', 'time_key', 'open', 'close', 'high', 'low', 'pe_ratio', 'turnover_rate', 'volume',
                        'turnover', 'change_rate', 'last_close']
            data_pd = pd.DataFrame(ret_list, columns=col_list)
            jump_threshold = data_pd.close.median() * 0.03

            if abs(jump_threshold) >  0.01:
                for index in np.arange(0,data_pd.shape[0]):
                    today = data_pd.ix[index]
                    judge_jump(today,jump_threshold)

            e1 = time.time()
            logging.info(
                "fetching {} K_LINE listing_date:{} start: {} end:{} cost time {}".format(code, listing_date, listing_date,
                                                                                           todayStr, e1 - b1))

            if is_closing is True:
                break

        if len(jump_pd) > 0:
            table = 'ft_stat_jump'
            worker.storeservice.insert_many(table, jump_pd, 'append')

        end = time.time()
        logging.info("fetching for one  period , cost time: {}".format((end - begin)))
        break



def judge_jump(today,jump_threshold):
    global jump_pd
    if today.last_close == 0:
        return

    if today.change_rate > 0 and (today.low - today.last_close) > jump_threshold:
        """
            符合向上跳空
        """
        # jump记录方向 1向上
        today['jump'] = 1
        # 向上跳能量＝（今天最低 － 昨收）／ 跳空阀值
        today['jump_power'] = (today.low - today.last_close) / jump_threshold
        jump_pd = jump_pd.append(today)
    elif today.change_rate < 0 and (today.last_close - today.high) > jump_threshold:
        """
            符合向下跳空
        """
        # jump记录方向 －1向下
        today['jump'] = -1
        # 向下跳能量＝（昨收 － 今天最高）／ 跳空阀值
        today['jump_power'] = (today.last_close - today.high) / jump_threshold
        jump_pd = jump_pd.append(today)

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
    tfn = MyThread2(thread_name, job_once_global_day_analysis, worker, arr)
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
    ret_arr = worker.storeservice.find_chs_stocks(False)
    thread_name = 'analysis for chs market'
    once_global_m5_task(thread_name, ret_arr, worker)

# hour='09'
# minute='05'
# @sched.scheduled_job('cron',day_of_week='tue-sat',hour=hour, minute=minute,second='00')
def analysis_us():
    worker = gen_one_worker()
    ret_arr = worker.storeservice.find_chs_stocks(True)
    thread_name = 'analysis for us market'
    once_global_m5_task(thread_name,ret_arr, worker)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_int_handler)
    #signal.signal(signal.SIGKILL, signal_term_handler)
    signal.signal(signal.SIGTERM, signal_term_handler)
    setup_logging()
    analysis_chs()
    analysis_us()
    sched.start()

