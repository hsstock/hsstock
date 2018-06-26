# -*- coding: UTF-8 -*-

from abc import ABC, abstractclassmethod
import pandas as pd

from sqlalchemy import create_engine
import tushare as ts


from hsstock.web.app_logging import setup_logging
from hsstock.utils.app_config import AppConfig


class Store(ABC):
    def __init__(self,engine):
        self.engine = engine
        pass

    def insert_one(self,item):
        pass

    def insert_many(self,table, df):
        pass

    def find(self,query):
        pass

    def update(self,query, newitem):
        pass

    def delete(self,query):
        pass


class MysqlStore(Store):
    def __init__(self,engine):
        super(MysqlStore,self).__init__(engine)

    def insert_one(self, item):
        pass

    def insert_many(self, table,df):
        df.to_sql(table, self.engine, if_exists='append')
        pass

    def find(self, query):
        pass

    def update(self, query, newitem):
        pass

    def delete(self, query):
        pass

class MongodbStore(Store):
    def __init__(self):
        super(MongodbStore,self).__init__()


class InfluxdbStore(Store):
    def __init__(self):
        super(InfluxdbStore,self).__init__()



class StoreService(Store):
    def __init__(self):
        '''
        Store Engine Init
        '''
        self.config = AppConfig.get_config()
        self.connect_url = self.config.get('mysql', 'connecturl')
        self.mysql_engine = create_engine(self.connect_url)
        mysqlStore = MysqlStore(self.mysql_engine)
        self.stores = []
        self.stores.append(mysqlStore)


    def insert_one(self, item):
        pass

    def insert_many(self, table, df):
        for store in self.stores:
            store.insert_many(table,df)

    def find(self, query):
        pass

    def update(self, query, newitem):
        pass

    def delete(self, query):
        pass