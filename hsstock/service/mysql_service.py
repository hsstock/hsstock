# -*- coding: UTF-8 -*-

from abc import ABC
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import sqlalchemy as sa
from sqlalchemy.exc import IntegrityError
from sqlalchemy.exc import OperationalError
from sqlalchemy.pool import QueuePool

from hsstock.utils.app_config import AppConfig
from hsstock.model.mysql.ft_stock_basicinfo import FTStockBasicInfo

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
        Session = sessionmaker()
        Session.configure(bind=engine)
        self.session = Session()

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
        try:
            pass #self.session.query
        except IOError as exc:
            logging.error(exc)

    def update(self, query, newitem):
        pass

    def delete(self, query):
        pass

# class MongodbStore(Store):
#     def __init__(self):
#         super(MongodbStore,self).__init__()
#
#
# class InfluxdbStore(Store):
#     def __init__(self):
#         super(InfluxdbStore,self).__init__()



class MysqlService():
    def __init__(self):
        '''
        Store Engine Init
        '''
        self.config = AppConfig.get_config()
        self.connect_url = self.config.get('mysql', 'connecturl')
        self.mysql_engine = create_engine(self.connect_url,poolclass=QueuePool,pool_pre_ping=True,pool_recycle=3600)
        self.mysqlStore = MysqlStore(self.mysql_engine)


    def insert_one(self, item):
        pass

    def init_schema(self, table, df, dtype=None, clauses=[], if_exists='replace', index=False, index_label=None):
        self.mysqlStore.init_schema(table,df,dtype,clauses,if_exists,index,index_label)

    def insert_many(self, table, df,if_exists='append', index=False, index_label=None):
        self.mysqlStore.insert_many(table,df,if_exists, index, index_label)

    def find(self, query):
        a = self.mysqlStore.session.query(FTStockBasicInfo.code, FTStockBasicInfo.name)
        print(a)
        for code,name in self.mysqlStore.session.query(FTStockBasicInfo.code,FTStockBasicInfo.name):
            print(code,name)

        pass

    def update(self, query, newitem):
        pass

    def delete(self, query):
        pass