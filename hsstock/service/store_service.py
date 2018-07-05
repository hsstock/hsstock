# -*- coding: UTF-8 -*-

from abc import ABC
import logging
from sqlalchemy import create_engine
import sqlalchemy as sa
from sqlalchemy.exc import IntegrityError
from sqlalchemy.exc import OperationalError
from sqlalchemy.pool import QueuePool

from hsstock.utils.app_config import AppConfig


class Store(ABC):
    def __init__(self,engine):
        self.engine = engine
        pass

    def init_schema(self,table, df, dtype=None,clauses=[],if_exists='replace', index=False, index_label=None ):
        with self.engine.connect() as con:
            df.to_sql(table, self.engine, if_exists = 'replace' if if_exists ==  None else if_exists,
                  index=False if index == False else True,
                  index_label = None if index_label == None else index_label,
                  dtype=None if dtype == None else dtype
                )
            for clause in clauses:
                con.execute(clause)

    def insert_one(self,item):
        pass

    def insert_many(self,table, df, if_exists='replace', index=False, index_label=None):
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

    def insert_many(self, table, df, if_exists='replace', index=False, index_label=None):
        try:
            df.to_sql(table, self.engine, if_exists = 'replace' if if_exists ==  None else if_exists,
                      index=False if index == False else True,
                      index_label = None if index_label == None else index_label
                      )
        except IntegrityError as exc:
            logging.error(exc)
        except OperationalError as exc:
            logging.error(exc)

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
        self.mysql_engine = create_engine(self.connect_url,poolclass=QueuePool,pool_pre_ping=True,pool_recycle=3600)
        mysqlStore = MysqlStore(self.mysql_engine)
        self.stores = []
        self.stores.append(mysqlStore)


    def insert_one(self, item):
        pass

    def init_schema(self, table, df, dtype=None, clauses=[], if_exists='replace', index=False, index_label=None):
        for store in self.stores:
            store.init_schema(table,df,dtype,clauses,if_exists,index,index_label)

    def insert_many(self, table, df,if_exists='append', index=False, index_label=None):
        for store in self.stores:
            store.insert_many(table,df,if_exists, index, index_label)

    def find(self, query):
        pass

    def update(self, query, newitem):
        pass

    def delete(self, query):
        pass