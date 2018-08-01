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
from hsstock.model.mysql.sys_sharding import SysSharding
from hsstock.model.mysql.ft_history_kline import FTHistoryKline
from hsstock.model.mysql.ft_history_kline_K_5M import FTHistoryKline5M
from sqlalchemy.sql import func

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

    def find_all_stockcodes(self):
        ret_codes = []
        for code,name in self.mysqlStore.session.query(FTStockBasicInfo.code,FTStockBasicInfo.name):
            ret_codes.append(code)
        return ret_codes

    def find_all_stocks(self):
        ret_arr = []
        for code, listing_date in self.mysqlStore.session.query(FTStockBasicInfo.code,FTStockBasicInfo.listing_date):
            ret_arr.append((code,listing_date))
        return ret_arr

    def find_tindex(self,code,dtype):
        #TODO , now 11 as the last table
        tindex = 11
        syssharding = self.mysqlStore.session.query(SysSharding).filter_by(code=code,dtype=dtype).first()
        if syssharding is not None:
            tindex = syssharding.tindex
        return tindex

    def find_lastdate(self,code):
        time_keys = self.mysqlStore.session.query(func.max(FTHistoryKline.time_key)).filter_by(code=code).first()
        for time in time_keys:
            return time

    def update(self, query, newitem):
        pass

    def delete(self, query):
        pass