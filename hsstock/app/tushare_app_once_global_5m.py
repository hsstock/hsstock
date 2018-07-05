# -*- coding: UTF-8 -*-
import logging
import signal
import time

from apscheduler.schedulers.blocking import BlockingScheduler

from hsstock.utils.app_logging import setup_logging
import hsstock.utils.tick_deco  as tick
from hsstock.service.tushare_service_new import TUShare_service
from hsstock.utils.date_util import DateUtil
from hsstock.utils.threadutil import MyThread
from hsstock.utils.app_config import AppConfig

sched = BlockingScheduler()
ts_realtime_global = TUShare_service()
ts_realtime_custom = TUShare_service()
ts_sunday = TUShare_service()
ts_once = TUShare_service()
ts_news = TUShare_service()

is_closing = False

"""
交易数据
    (ok)1:历史行情:近三年数据get_hist_data，全部数据用get_h_data
    (ok)1:复权数据:前复权，后复权，不复权，默认：前复权，不设定日期：获取近一年数据，设定日期：最好不要超过三年，获取全部数据，分年段获取，get_h_data
    (ok)N:R:实时行情：一次性获取当前所有股票行情数据 get_today_all
    (ok)1:历史分笔：当日之前的分笔数据，当天的用get_today_ticks获取，或当日18点之后，用本接口, get_tick_data
    (ok)N:R:实时分笔: 两三秒可调用一次，get_realtime_quotes(['code1','code2'])
    (ok)N:R:当日历史分笔: 交易进行中使用，get_today_ticks('601333') 列表吗？
    (ok)N:R:大盘指数行情列表: 大盘指数实时行情列表，get_index
    (ok)1:大单交易数据: 大单交易数据，来自新浪财经，默认400手，最好转换成金额（加转换功能）？
投资参考数据
    (ok)N:+R:分配预案: 季报，年报之前的送转，分红预案 profit_data
    (ok)N:+R 业绩预告：forecast_data(year,quarter)
    (ok)N:+R 限售股解禁: xsg_data(year,quarter) 
    (ok)N:+R 基金持股 fund_holding(year,quarter)
    (ok)1:新股数据 new_stocks()
    融资融券（沪市）
    融资融券（深市）
股票分类数据
    (ok)1:行业分类 get_industry_classified()
    (ok)1:概念分类 get_concept_classified()
    (ok)1:地域分类 get_area_classified()
    (ok)1:中小板分类: get_sme_classified()
    (ok)1:创业板分类 get_gem_classified()
    (ok)1:风险警示板分类 get_st_classified()
    (ok)1: 沪深300成份及权重 get_hs300s()
    (ok)1: 上证50成份股 get_sz50s()
    (ok)1: 中证500成份股 get_zz500s()
    终止上市股票列表
    暂停上市股票列表
基本面数据
    (ok?)1:股票列表: get_stock_basics()
    (ok)1:业绩报告（主表）: get_report_data(year,quarter)
    (ok)1:盈利能力: get_profit_data(year, quarter)
    (ok)1:营运能力: get_operation_data(year,quarter)
    (ok)1:成长能力: get_growth_data(year,quarter)
    (ok)1:偿债能力: get_debtpaying_data(year,quarter)
    (ok)1:现金流量: get_cashflow_data(year,quarter)
宏观经济数据
    (ok)1:存款利率: get_deposit_rate()
    (ok)1:贷款利率: get_loan_rate()
    (ok)1:存款准备金率: get_rrr()
    (ok)1:货币供应量: get_money_supply()
    (ok)1:货币供应量(年底余额): get_money_supply_bal()
    (ok)1:国内生产总值(年度): get_gdp_year()
    (ok)1:国内生产总值(季度): get_gdp_quarter()
    (ok)1:三大需求对GDP贡献: get_gdp_for()
    (ok)1:三大产业对GDP拉动: get_gdp_pull()
    (ok)1:三大产业贡献率: get_gdp_contrib()
    (ok)1:居民消费价格指数: get_cpi()
    (ok)1:工业品出厂价格指数: get_ppi()
新闻事件数据
    (ok)N+R:即时新闻: 获取即时财经新闻，类型包括国内财经、证券、外汇、期货、港股和美股等新闻信息。数据更新较快，使用过程中可用定时任务来获取。get_latest_news()
"""

def job_news(ts):
    '''
    线程工作：抓取新闻
    :param ts:
    :return:
    '''
    ts.get_latest_news()

def job_sunday(ts):
    """
    线程工作：定时间执行
    :return:
    """
    ts.get_ppi()
    ts.get_cpi()
    ts.get_gdp_contrib()
    ts.get_gdp_pull()
    ts.get_gdp_for()
    ts.get_gdp_quarter()
    ts.get_gdp_year()
    ts.get_money_supply_bal()
    ts.get_money_supply()
    ts.get_rrr()
    ts.get_loan_rate()
    ts.get_deposit_rate()

    ts.get_zz500s()
    ts.get_sz50s()
    ts.get_hs300s()
    ts.get_st_classified()
    ts.get_gem_classified()
    ts.get_sme_classified()
    ts.get_area_classified()
    ts.get_concept_classified()
    ts.get_industry_classified()
    ts.new_stocks()
    ts.xsg_data()

    doneYear = AppConfig.pull_year
    doneQuarter = AppConfig.pull_quarter
    for year in range(doneYear, 2019):
        for quarter in range(doneQuarter, 5):
            ts.get_cashflow_data(year, quarter)
            ts.get_debtpaying_data(year, quarter)
            ts.get_growth_data(year, quarter)
            ts.get_operation_data(year, quarter)
            ts.get_profit_data(year, quarter)
            ts.get_report_data(year, quarter)
            ts.fund_holdings(year, quarter)
            ts.forecast_data(year, quarter)
            ts.profit_data(year, 100)
            AppConfig.write_pulltime(year, quarter)


def job_once_custom(ts):
    ts.get_stock_basics()
    for symbol in AppConfig.custom_stocks:
        ts.get_hist_data(symbol)
        time.sleep(1)
        ts.get_h_data(symbol, '2015-07-06', '2018-07-05', 'hfq')
        time.sleep(1)
        ts.get_sina_dd(symbol, '2018-07-05', 400)
        time.sleep(1)

def job_once_global(ts):
    df = ts.get_stock_basics()
    cont = False
    lastsymbol = '600318'
    for symbol in df['name'].index.values:
        if symbol == lastsymbol:
            cont = True
        if not cont:
            continue
        ts.get_hist_data(symbol)
        #ts.get_h_data(symbol, '2017-07-06', '2018-07-05', 'hfq')
        time.sleep(3)
        ts.get_sina_dd(symbol, '2018-07-05', 400)
        time.sleep(2)


def job_once_global_5m(ts):
    global is_closing
    df = ts.get_stock_basics()
    cont = False
    for symbol in df['name'].index.values:
        if not is_closing:
            ts.get_hist_data(symbol,None,None,'5')
            time.sleep(2)

def job_realtime_global(ts):
    ts.get_index()
    ts.get_today_all()

def job_realtime_custom(ts):
    ts.get_today_ticks(AppConfig.custom_stocks)
    ts.get_realtime_quotes(AppConfig.custom_stocks)
    ts.get_realtime_quotes(AppConfig.custom_indexes)
    for symbol in AppConfig.custom_stocks:
        ts.get_tick_data(symbol, DateUtil.getDatetimeYesterdayStr(DateUtil.getDatetimeToday()))


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



#
# @sched.scheduled_job('cron',day_of_week='sat-sun',hour='18', minute='00-01',second='*/10')
# def sunday_task():
#     tfn = MyThread('job_sunday', job_sunday,ts_sunday)
#     tfn.start()
#
# #@sched.scheduled_job('interval',seconds=3)
# def once_custom_task():
#     tfn = MyThread('job_once_custom',job_once_custom, ts_once)
#     tfn.start()

# def once_global_task():
#     tfn = MyThread('job_once_global',job_once_global, ts_once)
#     tfn.start()

def once_global_task_5m():
    tfn = MyThread('job_once_global_5m',job_once_global_5m, ts_once)
    tfn.start()

# @sched.scheduled_job('interval',seconds=5)
# def news_task():
#     tfn = MyThread('job_news',job_news, ts_news)
#     tfn.start()
#
# @sched.scheduled_job('interval',seconds=20)
# def realtime_global_task():
#     tfn = MyThread('job_realtime_global',job_realtime_global, ts_realtime_global)
#     tfn.start()
#
# @sched.scheduled_job('interval',seconds=20)
# def realtime_custom_task():
#     tfn = MyThread('job_realtime_custom',job_realtime_custom, ts_realtime_custom)
#     tfn.start()



def main():
    # sunday_task()
    # once_custom_task()
    # once_global_task()
    once_global_task_5m()
    #news_task()
    # realtime_global_task()
    # realtime_custom_task()

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_int_handler)
    #signal.signal(signal.SIGKILL, signal_term_handler)
    signal.signal(signal.SIGTERM, signal_term_handler)
    setup_logging()
    main()
    sched.start()


