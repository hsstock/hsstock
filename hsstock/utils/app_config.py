import configparser
import os
import time
import threading

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


    @staticmethod
    def get_config():
        return AppConfig.instance().config

    @staticmethod
    def write_news_pulltime(time):
        #AppConfig.get_config().add_section('sec_b')
        AppConfig.get_config().set("pull_time", "latest_news", time)
        AppConfig.get_config().write(open(AppConfig.path, "w"))


if __name__ == "__main__":
    port = AppConfig.get_config().get('web','port')
    print(port)
    AppConfig.instance().write_news_pulltime('a')


