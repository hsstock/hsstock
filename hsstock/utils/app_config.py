import configparser
import os


class AppConfig:
    @staticmethod
    def get_config():
        config = configparser.RawConfigParser()
        config.read(''.join((os.path.abspath(''.join((__file__, '../../../'))), '/data/app.config')))
        return config
