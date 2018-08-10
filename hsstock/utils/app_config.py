import configparser
import os
import time
import threading

from hsstock.utils.apollo_client import ApolloClient

class AppConfig:

    _instance_lock = threading.Lock()

    @classmethod
    def instance(cls,*args, **kwargs):
        if not hasattr(AppConfig,"_instance"):
            with AppConfig._instance_lock:
                AppConfig._instance = AppConfig(*args,**kwargs)
        return AppConfig._instance

    @classmethod
    def __init__(cls):
        AppConfig.config = configparser.RawConfigParser()
        AppConfig.path = ''.join((os.path.abspath(''.join((__file__, '../../../../'))), '/data/app.config'))
        AppConfig.config.read(AppConfig.path)
        AppConfig.latest_news_pulltime = float(AppConfig.config.get('pull_time','latest_news'))
        AppConfig.pull_year = int(AppConfig.config.get('pull_time', 'year'))
        AppConfig.pull_quarter = int(AppConfig.config.get('pull_time', 'quarter'))
        AppConfig.custom_stocks = AppConfig.config.get('custom', 'stocks').split(',')
        AppConfig.custom_indexes = AppConfig.config.get('custom', 'indexes').split(',')
        AppConfig.custom_ft_stocks = AppConfig.config.get('custom_ft', 'stocks').split(',')
        AppConfig.apollo_client = ApolloClient(AppConfig.config.get('apolloconfig', 'appid'), config_server_url=AppConfig.config.get('apolloconfig', 'config_server_url'))
        AppConfig.apollo_client.start()

    @staticmethod
    def get_config():
        return AppConfig.instance().config

    @staticmethod
    def write_news_pulltime(time,sync = False):
        #AppConfig.get_config().add_section('sec_b')A
        AppConfig.latest_news_pulltime = time
        if  sync is True:
            AppConfig.get_config().set("pull_time", "latest_news", time)
            AppConfig.get_config().write(open(AppConfig.path, "w"))

    @staticmethod
    def write_pulltime(year,quarter,sync = True):
        AppConfig.pull_year = year
        AppConfig.pull_quarter = quarter
        if sync is True:
            AppConfig.get_config().set("pull_time", "year", year)
            AppConfig.get_config().set("pull_time", "quarter", quarter)
            AppConfig.get_config().write(open(AppConfig.path, "w"))

    @staticmethod
    def write_custom_stocks(stocks):
        stocks_str = ','.join(stocks)
        AppConfig.get_config().set("custom", "stocks", stocks_str)
        AppConfig.get_config().write(open(AppConfig.path, "w"))

    @staticmethod
    def write_custom_ft_stocks(stocks):
        stocks_str = ','.join(stocks)
        AppConfig.get_config().set("custom_ft", "stocks", stocks_str)
        AppConfig.get_config().write(open(AppConfig.path, "w"))

    # Apollo配置中心
    @staticmethod
    def get_apollo_config():
        return AppConfig.instance().apollo_client

if __name__ == "__main__":
    # port = AppConfig.get_config().get('web','port')
    # print(port)
    # AppConfig.write_news_pulltime('a')
    appid = AppConfig.get_apollo_config().get_value('host')
    print(appid)




