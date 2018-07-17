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
lf_ctx  = None
hf_ctx = None
hk_ctx = None
us_ctx = None

def job_once_global(worker):
    '''
    功能：获取一次性的全局数据
    :param worker:
    :return:
    '''
    global is_closing

def job_once_custom(worker):
    '''

    :param worker:
    :return:
    '''
    global is_closing

def job_realtime_global(worker):
    '''

    :param workery:
    :return:
    '''
    global is_closing

def job_lf(worker):
    '''
    线程工作：低频数据接口
    :return:
    '''
    global is_closing

    while not is_closing:
        begin = time.time()
        markets = enumclass_to_list(Market)
        for market in markets:
            worker.get_trading_days(market)
        if is_closing is True:
            break
        securitytypes = enumclass_to_list(SecurityType)
        for market in markets:
            for securitytype in securitytypes:
                worker.get_stock_basicinfo(market, securitytype)
        if is_closing is True:
            break

        worker.get_multiple_history_kline(['US.NTES','US.BABA'], '2018-06-20', '2018-06-25', KLType.K_DAY, AuType.QFQ)
        if is_closing is True:
            break
        worker.get_multiple_history_kline(['HK.00771','HK.00700'], '2018-06-20', '2018-06-25',
                                                                  KLType.K_DAY, AuType.QFQ)
        if is_closing is True:
             break

        worker.get_history_kline('US.AAPL','2018-01-01', '2018-06-29',KLType.K_5M)
        if is_closing is True:
            break
        worker.get_history_kline('HK.00700', '2018-01-01', '2018-06-29',KLType.K_5M)
        if is_closing is True:
            break
        break
        worker.get_autype_list(['US.AAPL','HK.00700'])
        if is_closing is True:
            break
        worker.get_autype_list(['HK.00700'])
        if is_closing is True:
            break
        worker.get_market_snapshot(['HK.00700', 'US.AAPL'])
        if is_closing is True:
            break

        plate_list = []
        for market in markets:
            ret_code, ret_data = worker.get_plate_list(market)
            if ret_code is RET_OK:
                plate_list.append(ret_data)
        if is_closing is True:
            break

        # for i in range(0,len(plate_list),1):
        #     for j in range(0, len(plate_list[i]), 1):
        #         worker.get_plate_stock(plate_list[i].iloc[j].code)
        #         print('get_plate_stock current progress - {}.{}'.format(i,j))
        #         time.sleep(FREQLIMIT[FREQ.TOTAL_SECONDS]/FREQLIMIT[FREQ.GET_PLATE_STOCK])
        # if is_closing is True:
        #     break

        worker.get_global_state()
        if is_closing is True:
            break

        end = time.time()
        print(end-begin)
        time.sleep(FREQLIMIT[FREQ.TOTAL_SECONDS] - end + begin)

def job_hf(worker):
    '''
    线程工作：高频数据接口
    :return:
    '''
    global is_closing
    while not is_closing:
        worker.get_stock_quote(['US.AAPL','HK.00700'])
        if is_closing is True:
            break
        worker.get_rt_data('HK.00700')
        if is_closing is True:
            break
        worker.get_rt_data('US.AAPL')
        if is_closing is True:
            break
        worker.get_rt_ticker('HK.00700',500)
        if is_closing is True:
            break
        worker.get_cur_kline('HK.00700',1000)
        if is_closing is True:
            break
        worker.get_order_book('HK.00700')
        if is_closing is True:
            break
        worker.ctx.set_handler(HSStockQuoteHandler())
        worker.ctx.set_handler(HSOrderBookHandler())
        worker.ctx.set_handler(HSCurKlineHandler())
        worker.ctx.set_handler(HSTickerHandler())
        worker.ctx.set_handler(HSRTDataHandler())
        worker.ctx.set_handler(HSBrokerHandler())

def job_hk_trade(worker):
    '''
    线程工作：交易接口
    :return:
    '''
    global is_closing
    global hk_ctx
    while not is_closing:
        worker.get_acc_list()
        if is_closing is True:
            break
        worker.accinfo_query(TrdEnv.REAL)
        if is_closing is True:
            break
        worker.accinfo_query(TrdEnv.SIMULATE)
        if is_closing is True:
            break
        worker.position_list_query()
        if is_closing is True:
            break
        worker.place_order(0.1, 1000, 'HK.01060')
        if is_closing is True:
            break
        worker.order_list_query()
        if is_closing is True:
            break
        #worker.modify_order( modify_order_op, order_id, qty,price, adjust_limit, trd_env, acc_id)
        worker.deal_list_query()
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
        worker.get_acc_list()
        if is_closing is True:
            break
        worker.accinfo_query(TrdEnv.REAL)
        if is_closing is True:
            break
        worker.accinfo_query(TrdEnv.SIMULATE)
        if is_closing is True:
            break
        worker.position_list_query()
        if is_closing is True:
            break
        worker.place_order(1.88, 100, 'US.JMEI')
        if is_closing is True:
            break
        worker.order_list_query()
        if is_closing is True:
            break
        #worker.modify_order( modify_order_op, order_id, qty,price, adjust_limit, trd_env, acc_id)
        worker.deal_list_query()
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
    global lf_ctx
    global hf_ctx
    global hk_ctx
    global us_ctx
    logging.info('exiting...')
    is_closing = True
    lf_ctx.stop()
    lf_ctx.close()
    hf_ctx.stop()
    hf_ctx.close()
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
    global lf_ctx
    global hf_ctx
    global hk_ctx
    global us_ctx
    logging.info('killed, exiting...')
    is_closing = True
    lf_ctx.stop()
    lf_ctx.close()
    hf_ctx.stop()
    hf_ctx.close()
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

def lf_task(worker):
    tfn = MyThread('job_lf',job_lf,worker)
    tfn.start()

def hf_task(worker):
    tfn = MyThread('job_hf', job_hf,worker)
    tfn.start()

def hk_trade_task(worker):
    tfn = MyThread('job_hk_trade', job_hk_trade,worker)
    tfn.start()

def us_trade_task(worker):
    tfn = MyThread('job_us_trade', job_us_trade,worker)
    tfn.start()

def main():
    global lf_ctx
    global hf_ctx
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
    lf_ctx = ft.OpenQuoteContext(config.get('ftserver', 'host'), int(config.get('ftserver', 'port')))
    lf_ctx.start()
    lf = LF(lf_ctx)
    #lf_task(lf)

    hf_ctx = ft.OpenQuoteContext(config.get('ftserver', 'host'), int(config.get('ftserver', 'port')))
    hf_ctx.start()
    sub = Subscribe(hf_ctx, total, kline, tiker, quote, order_book, rt_data, broker)
    hf = HF(hf_ctx, sub)
    #hf_task(hf)

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