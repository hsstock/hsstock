# -*- coding: UTF-8 -*-

from abc import ABC
import logging
from sqlalchemy import create_engine
from sqlalchemy import and_
from sqlalchemy import text
from sqlalchemy.orm import sessionmaker

import sqlalchemy as sa
from sqlalchemy.exc import IntegrityError
from sqlalchemy.exc import OperationalError
from sqlalchemy.pool import QueuePool
from sqlalchemy import update

from hsstock.utils.app_config import AppConfig
from hsstock.model.mysql.ft_stock_basicinfo import FTStockBasicInfo
from hsstock.model.mysql.sys_sharding import SysSharding
from hsstock.model.mysql.ft_history_kline import *
from hsstock.model.mysql.ft_history_kline_K_5M import *
from hsstock.model.mysql.ft_plate_list import FTPlateList
from hsstock.model.mysql.ft_plate_stock import FTPlateStock

from hsstock.model.mysql.ft_stock_basicinfo_now_nohistdata import FTStockBasicInfoNoHistData
from hsstock.utils.date_util import DateUtil

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
        self.mysql_engine = create_engine(self.connect_url,poolclass=QueuePool,pool_pre_ping=True,pool_recycle=3600,pool_size=20)
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

    def find_all_stockcodes_exclude_nodata(self):
        ret_codes = []
        subquery = self.mysqlStore.session.query(FTStockBasicInfoNoHistData.code)
        for code,name in self.mysqlStore.session.query(FTStockBasicInfo.code,FTStockBasicInfo.name).filter_by(stock_type='STOCK').filter(~FTStockBasicInfo.code.in_(subquery)):
            ret_codes.append(code)
        return ret_codes

    def find_all_stocks(self):
        ret_arr = []
        subquery = self.mysqlStore.session.query(FTStockBasicInfoNoHistData.code)
        for code, listing_date in self.mysqlStore.session.query(FTStockBasicInfo.code,FTStockBasicInfo.listing_date).filter(~FTStockBasicInfo.code.in_(subquery)):
            ret_arr.append((code,listing_date))
        return ret_arr

    def find_chs_stocks(self, is_chs=False):
        ret_arr = []
        subquery = self.mysqlStore.session.query(FTStockBasicInfoNoHistData.code)
        if is_chs is True:
            for code, listing_date in self.mysqlStore.session.query(FTStockBasicInfo.code,
                                                                    FTStockBasicInfo.listing_date).filter(
                ~FTStockBasicInfo.code.in_(subquery)).filter(FTStockBasicInfo.code.like('%US.%')):
                ret_arr.append((code, listing_date))
        else:
            ret_arr = []
            for code, listing_date in self.mysqlStore.session.query(FTStockBasicInfo.code,
                                                                    FTStockBasicInfo.listing_date).filter(
                ~FTStockBasicInfo.code.in_(subquery)).filter(~FTStockBasicInfo.code.like('%US.%')):
                ret_arr.append((code, listing_date))
            return ret_arr
        return ret_arr

    def find_stocks(self,dtype,tindex):
        ret_arr = []
        subquery = self.mysqlStore.session.query(FTStockBasicInfoNoHistData.code)
        subquery2 = self.mysqlStore.session.query(SysSharding.code).filter_by(dtype=dtype,tindex=tindex)
        for code, listing_date in self.mysqlStore.session.query(FTStockBasicInfo.code,
                                                                FTStockBasicInfo.listing_date).filter(
                ~FTStockBasicInfo.code.in_(subquery)).filter(FTStockBasicInfo.code.in_(subquery2)):
            ret_arr.append((code, listing_date))
        return ret_arr

    def find_plate_stock(self):
        ret = []
        col_list = ['code', 'lot_size', 'stock_name','stock_owner','stock_child_type','stock_type','list_time','stock_id']
        cls = FTPlateStock
        for code, lot_size, stock_name, stock_owner, stock_child_type, stock_type, list_time,stock_id in self.mysqlStore.session.query(cls.code, cls.lot_size, cls.stock_name,cls.stock_owner,cls.stock_child_type,cls.stock_type,cls.list_time,cls.stock_id).all():
            item = (code, lot_size, stock_name, stock_owner, stock_child_type, stock_type, list_time,stock_id )
            ret.append(item)
        return ret

    def find_plate_list(self):
        ret = []
        cls = FTPlateList
        for code, plate_name, plate_id in self.mysqlStore.session.query(cls.code, cls.plate_name, cls.plate_id).all():
            item = (code, plate_name, plate_id)
            ret.append(item)
        return ret

    def find_history_kline(self,code,dtype,start,end):
        tindex = self.find_tindex(code, dtype)
        cls = getClassByIndex(tindex)
        ret = []
        #for item in self.mysqlStore.session.query(FTHistoryKline6).filter(cls.code == code).filter(and_(text('time_key>:start'),text('time_key<:end')).params(start=start,end=end)).all():
        #,cls.code,cls.time_key,cls.open,cls.close,cls.high,cls.low,cls.pe_ratio,cls.turnover_rate,cls.volume,cls.turnover,cls.change_rate,cls.last_close
        #(code, time_key, open, close, high, low, pe_ratio, turnover_rate, volume, turnover, change_rate, last_close)
        for code, time_key, open, close, high, low, pe_ratio, turnover_rate, volume, turnover, change_rate, last_close in self.mysqlStore.session.query(cls.code, cls.time_key,cls.open,cls.close,cls.high,cls.low,cls.pe_ratio,cls.turnover_rate,cls.volume,cls.turnover,cls.change_rate,cls.last_close).filter(cls.code == code).filter(and_(cls.time_key>=start, cls.time_key<=end)).order_by(cls.time_key).all():
            item = (code, DateUtil.datetime_toString(time_key), open, close, high, low, pe_ratio, turnover_rate, volume, turnover, change_rate, last_close)
            ret.append(item)
        return ret

    def find_tindex(self,code,dtype):
        #TODO , now 17 as the last kl_K_5M table, 11 as the last kl table
        tindex = 17
        if dtype == 'hk_5m':
            tindex = 17
        else:
            tindex = 11

        syssharding = self.mysqlStore.session.query(SysSharding).filter_by(code=code,dtype=dtype).first()
        if syssharding is not None:
            tindex = syssharding.tindex
        return tindex

    def find_lastdate(self,code,lastdate):
        try:
            tindex = self.find_tindex(code,'hk')
            cls = getClassByIndex(tindex)
            time_keys = self.mysqlStore.session.query(cls.time_key).filter_by(code=code).filter(cls.time_key > lastdate).order_by(cls.time_key.desc()).limit(1).first()
            if time_keys is not None :
                for time in time_keys:
                    return time
        except IOError as err:
            logging.error("OS|error: {0}".format(err))
        else:
            pass
        return None

    def find_lastdate2(self,code,dtype):
        try:
            time_keys = self.mysqlStore.session.query(SysSharding.lastdate).filter(and_(SysSharding.code==code,SysSharding.dtype==dtype)).limit(1).first()
            if time_keys is not None :
                for time in time_keys:
                    return time
        except IOError as err:
            logging.error("OS|error: {0}".format(err))
        else:
            pass
        return None


    def find_lastdate_5M(self, code,lastdate):
        try:
            tindex = self.find_tindex(code, 'hk_5m')
            cls = getClass5mByIndex(tindex)
            time_keys = self.mysqlStore.session.query(cls.time_key).filter_by(code=code).filter(cls.time_key > lastdate).order_by(cls.time_key.desc()).limit(1).first()
            if time_keys is not None:
                for time in time_keys:
                    return time
        except IOError as err:
            logging.error("OS|error: {0}".format(err))
        else:
            pass
        return None

    def update_lastdate(self, code, dtype, lastest_date):
        try:
            #MyISAM work ok, but failed after changing the storage engine to InnoDB
            #需要注意的是，update和delete在做批量操作的时候（使用 where…in(…)）操作，需要指定synchronize_session的值。
            #self.mysqlStore.session.query(SysSharding).filter(and_(SysSharding.code==code,SysSharding.dtype==dtype)).update({SysSharding.lastdate:lastest_date},synchronize_session=False)
            self.mysqlStore.session.query(SysSharding).filter(
                and_(SysSharding.code == code, SysSharding.dtype == dtype)).update({SysSharding.lastdate: lastest_date})
            self.mysqlStore.session.commit()
        except IOError as err:
            logging.error("OS|error: {0}".format(err))
        else:
            pass
        return None



    def update(self, query, newitem):
        pass

    def delete(self, query):
        pass
