# -*- coding: UTF-8 -*-
"""
 https://finviz.com/help/screener.ashx
"""


from apscheduler.schedulers.blocking import BlockingScheduler
import logging
import time
import datetime
import random
import pandas as pd

from hsstock.service.mysql_service import MysqlService
from hsstock.utils.fiv_crawler import Crawler
from hsstock.utils.app_logging import setup_logging

sched = BlockingScheduler()

@sched.scheduled_job('cron',day_of_week='mon-fri',hour='16', minute='39')
def scheduled_job():
    logging.info('This job is run every weekday at 5pm')
    crawler = Crawler('##')
    storeservice = MysqlService()

    pos = 0
    while pos < 7101:
        print(pos)
        url = 'http://finviz.com/screener.ashx?v=152&r=' + str(
            pos) + '&c=0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70'

        crawler.get_page(url)
        time.sleep(2 * random.random())
        pos += 21
        jsonArray = crawler.toJsons()
        table = 'fiv2_stat'
        df = pd.DataFrame(jsonArray, columns=crawler.propertiesList)
        df = df.replace('-', 0)
        df['P/E'] = df['P/E'].astype(float)
        df['Fwd P/E'] = df['Fwd P/E'].astype(float)
        df['PEG'] = df['PEG'].astype(float)
        df['P/S'] = df['P/S'].astype(float)
        df['P/B'] = df['P/B'].astype(float)
        df['P/C'] = df['P/C'].astype(float)
        df['P/FCF'] = df['P/FCF'].astype(float)
        df['EPS'] = df['EPS'].astype(float)
        df['Short Ratio'] = df['Short Ratio'].astype(float)
        df['CurrR'] = df['CurrR'].astype(float)
        df['Quick R'] = df['Quick R'].astype(float)
        df['LTDebt/Eq'] = df['LTDebt/Eq'].astype(float)
        df['Debt/Eq'] = df['Debt/Eq'].astype(float)
        df['Beta'] = df['Beta'].astype(float)
        df['ATR'] = df['ATR'].astype(float)
        df['RSI'] = df['RSI'].astype(float)
        df['Recom'] = df['Recom'].astype(float)
        df['Rel Volume'] = df['Rel Volume'].astype(float)
        df['Price'] = df['Price'].astype(float)
        df['Target Price'] = df['Target Price'].astype(float)
        try:
            storeservice.insert_many(table, df)
        except IOError as err:
            logging.error(err)
        else:
            pass

def main():
    logging.info('before the start function')
    #sched.start()
    scheduled_job()
    logging.info('let us figure out the situation')

if __name__ == "__main__":
    setup_logging()
    main()
