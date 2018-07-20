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
env = Environment()
env_us = Environment()

is_closing = False
hk_ctx  = None
us_ctx = None

def job_hk_trade(worker):
    '''
    线程工作：交易接口
    :return:
    '''
    global is_closing
    global hk_ctx
    while not is_closing:
        print('hk')
        ret_code, ret_data = worker.get_acc_list()
        env.accs = ret_data
        if is_closing is True:
            break
        ret_code, ret_data = worker.accinfo_query(TrdEnv.REAL)
        env.account_info = ret_data
        if is_closing is True:
            break
        ret_code, ret_data = worker.accinfo_query(TrdEnv.REAL)
        env.account_info_simulate = ret_data
        if is_closing is True:
            break
        ret_code, ret_data = worker.position_list_query()
        env.account_info_positions = ret_data
        if is_closing is True:
            break
        ret_code, ret_data = worker.place_order(0.1, 1000, 'HK.01060')
        env.curr_order = ret_data
        if is_closing is True:
            break
        ret_code, ret_data = worker.order_list_query()
        env.orders = ret_data
        if is_closing is True:
            break
        #worker.modify_order( modify_order_op, order_id, qty,price, adjust_limit, trd_env, acc_id)
        ret_code, ret_data = worker.deal_list_query()
        env.deals = ret_data
        if is_closing is True:
            break
        worker.history_order_list_query()
        if is_closing is True:
            break
        worker.history_deal_list_query('HK.00700','2018-06-01 00:00:00','2018-07-10 00:00:00',TrdEnv.REAL)
        if is_closing is True:
            break
        hk_ctx.set_handler(HSTradeOrder())
        hk_ctx.set_handler(HSTradeDeal())
        worker.place_order(300, 100, "HK.00700", TrdSide.BUY)
        time.sleep(FREQLIMIT[FREQ.TOTAL_SECONDS])

def job_us_trade(worker):
    '''
    线程工作：交易接口
    :return:
    '''
    global is_closing
    global us_ctx
    while not is_closing:
        print('us')
        ret_code, ret_data = worker.get_acc_list()
        env_us.accs = ret_data
        if is_closing is True:
            break
        ret_code, ret_data = worker.accinfo_query(TrdEnv.REAL)
        env_us.account_info = ret_data
        if is_closing is True:
            break
        ret_code, ret_data = worker.accinfo_query(TrdEnv.REAL)
        env_us.account_info_simulate = ret_data
        if is_closing is True:
            break
        ret_code, ret_data = worker.position_list_query()
        env.account_info_positions = ret_data
        if is_closing is True:
            break
        ret_code, ret_data = worker.place_order(1.88, 100, 'US.JMEI')
        env.curr_order = ret_data
        if is_closing is True:
            break
        ret_code, ret_data = worker.order_list_query()
        env.orders = ret_data
        if is_closing is True:
            break
        #worker.modify_order( modify_order_op, order_id, qty,price, adjust_limit, trd_env, acc_id)
        ret_code, ret_data = worker.deal_list_query()
        env.deals = ret_data
        if is_closing is True:
            break
        worker.history_order_list_query()
        if is_closing is True:
            break
        worker.history_deal_list_query('US.AAPL','2018-06-01 00:00:00','2018-07-10 00:00:00',TrdEnv.REAL)
        if is_closing is True:
            break
        us_ctx.set_handler(HSTradeOrder())
        us_ctx.set_handler(HSTradeDeal())
        worker.place_order(150, 100, "US.AAPL", TrdSide.BUY)

        time.sleep(FREQLIMIT[FREQ.TOTAL_SECONDS])

def signal_int_handler(signum, frame):
    global is_closing
    global hk_ctx
    global us_ctx
    logging.info('exiting...')
    is_closing = True
    hk_ctx.stop()
    hk_ctx.close()
    us_ctx.stop()
    us_ctx.close()
    sched.shutdown(True)


#SIGKILL 不可被捕获
# def signal_kill_handler():
#     global is_closing
#     logging.info('killed, exiting...')
#     is_closing = True
#     sched.shutdown(True)

def signal_term_handler(*args):
    global is_closing
    global hk_ctx
    global us_ctx
    logging.info('killed, exiting...')
    is_closing = True
    hk_ctx.stop()
    hk_ctx.close()
    us_ctx.stop()
    us_ctx.close()
    sched.shutdown(True)

def try_exit():
    global is_closing
    if is_closing:
        # clean up here
        logging.info('exit success')


def hk_trade_task(worker):
    tfn = MyThread('job_hk_trade', job_hk_trade,worker)
    tfn.start()

def us_trade_task(worker):
    tfn = MyThread('job_us_trade', job_us_trade,worker)
    tfn.start()

def main():
    global hk_ctx
    global us_ctx
    config = AppConfig.get_config()
    total = config.get('quota', 'total')
    kline = config.get('quota', 'kline')
    tiker = config.get('quota', 'ticker')
    quote = config.get('quota', 'quote')
    order_book = config.get('quota', 'order_book')
    rt_data = config.get('quota', 'rt_data')
    broker = config.get('quota', 'broker')

    hk_ctx = ft.OpenHKTradeContext(config.get('ftserver', 'host'), int(config.get('ftserver', 'port')))
    hk_trade = Trade(hk_ctx)
    hk_trade.unlock_trade(None,config.get('ftserver', 'decipher'))
    hk_trade_task(hk_trade)

    us_ctx = ft.OpenUSTradeContext(config.get('ftserver', 'host'), int(config.get('ftserver', 'port')))
    us_trade = Trade(us_ctx)
    us_trade.unlock_trade(None, config.get('ftserver', 'decipher'))
    us_trade_task(us_trade)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_int_handler)
    #signal.signal(signal.SIGKILL, signal_term_handler)
    signal.signal(signal.SIGTERM, signal_term_handler)
    setup_logging()
    main()
    sched.start()