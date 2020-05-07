# -*- coding: UTF-8 -*-

from abc import ABC
import logging
import pymysql
pymysql.install_as_MySQLdb()

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
from hsstock.model.mysql.ft_kline import *
from hsstock.model.mysql.ft_5M import *
from hsstock.model.mysql.ft_1M import *
from hsstock.model.mysql.ft_plate_list import FTPlateList
from hsstock.model.mysql.ft_plate_stock import FTPlateStock

from hsstock.model.mysql.ft_stock_basicinfo_now_nohistdata import FTStockBasicInfoNoHistData
from hsstock.utils.date_util import DateUtil

from sqlalchemy.sql import func

'''
MyISAM:  大量插入是，不要查询
'''
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
    def __init__(self,sel=1):
        '''
        Store Engine Init
        '''
        self.config = AppConfig.get_config()
        self.connect_url = self.config.get('mysql', 'connecturl') if  sel == 1 else self.config.get('mysql', 'connecturl2')
        self.mysql_engine = create_engine(self.connect_url,poolclass=QueuePool,pool_pre_ping=True,pool_recycle=3600,pool_size=20)
        self.mysqlStore = MysqlStore(self.mysql_engine)


    def executeSql(self,sql):
        with self.mysql_engine.connect() as con:
            result = con.execute(sql)
            if result.returns_rows == True:
                # for r in result:
                #     print(r)
                return result

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

    def find_all_stock_codeandname(self):
        ret_codes = []
        for code,name in self.mysqlStore.session.query(FTStockBasicInfo.code,FTStockBasicInfo.name):
            ret_codes.append((code,name))
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
                ~FTStockBasicInfo.code.in_(subquery)).filter(~FTStockBasicInfo.code.like('%US.%')):
                ret_arr.append((code, listing_date))
        else:
            ret_arr = []
            for code, listing_date in self.mysqlStore.session.query(FTStockBasicInfo.code,
                                                                    FTStockBasicInfo.listing_date).filter(
                ~FTStockBasicInfo.code.in_(subquery)).filter(FTStockBasicInfo.code.like('%US.%')):
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

        if dtype == 'hk_5m':
            cls = get5MClassByIndex(tindex)
        elif dtype == 'hk_1m':
            cls = get1MClassByIndex(tindex)
        else:
            cls = getHKClassByIndex(tindex)

        ret = []
        #for item in self.mysqlStore.session.query(FTHistoryKline6).filter(cls.code == code).filter(and_(text('time_key>:start'),text('time_key<:end')).params(start=start,end=end)).all():
        #,cls.code,cls.time_key,cls.open,cls.close,cls.high,cls.low,cls.pe_ratio,cls.turnover_rate,cls.volume,cls.turnover,cls.change_rate,cls.last_close
        #(code, time_key, open, close, high, low, pe_ratio, turnover_rate, volume, turnover, change_rate, last_close)
        # for code, time_key, open, close, high, low, pe_ratio, turnover_rate, volume, turnover, change_rate, last_close in self.mysqlStore.session.query(cls.code, cls.time_key,cls.open,cls.close,cls.high,cls.low,cls.pe_ratio,cls.turnover_rate,cls.volume,cls.turnover,cls.change_rate,cls.last_close).filter(cls.code == code).filter(and_(cls.time_key>=start, cls.time_key<=end)).order_by(cls.time_key).all():
        #     item = (code, DateUtil.datetime_toString(time_key), open, close, high, low, pe_ratio, turnover_rate, volume, turnover, change_rate, last_close)
        #     ret.append(item)
        for code, time_key, open, close, high, low, pe_ratio, turnover_rate, volume, turnover, change_rate, last_close in self.mysqlStore.session.query(cls.code, cls.time_key,cls.open,cls.close,cls.high,cls.low,cls.pe_ratio,cls.turnover_rate,cls.volume,cls.turnover,cls.change_rate,cls.last_close).filter(cls.code == code).filter(and_(cls.time_key>=start, cls.time_key<=end)).order_by(cls.time_key).all():
            item = (code, time_key, open, close, high, low, pe_ratio, turnover_rate, volume, turnover, change_rate, last_close)
            ret.append(item)
        return ret

    def find_tindex(self,code,dtype):
        tindex = 1

        syssharding = self.mysqlStore.session.query(SysSharding).filter_by(code=code,dtype=dtype).first()
        if syssharding is not None:
            tindex = syssharding.tindex
        return tindex

    def find_lastdate_from_origin(self, code, dtype,lastdate='2018-09-01'):
        '''
        hk,1m, 5m表里取得最后日期
        :param code:
        :param dtype:
        :param lastdate:
        :return:
        '''
        try:
            tindex = self.find_tindex(code,dtype)

            if dtype == 'hk_5m':
                cls = get5MClassByIndex(tindex)
            elif dtype == 'hk_1m':
                cls = get1MClassByIndex(tindex)
            else:
                cls = getHKClassByIndex(tindex)

            time_keys = self.mysqlStore.session.query(cls.time_key).filter_by(code=code).filter(cls.time_key > lastdate).order_by(cls.time_key.desc()).limit(1).first()
            if time_keys is not None :
                for time in time_keys:
                    return time
        except IOError as err:
            logging.error("OS|error: {0}".format(err))
        else:
            pass
        return None

    def _get_last_index(self,dtype):
        '''
        ToDO
        最后一个表填满后，即需要修改
        :param dtype:
        :return:
        '''
        if dtype == 'hk_5m':
            return 63
        elif dtype == 'hk_1m':
            return 230
        else:
            return 9

    def find_lastdate(self,code,dtype):
        '''
        sys_sharding表里取得最后时间
        :param code:
        :param dtype:
        :return:
        '''
        try:
            time_keys = self.mysqlStore.session.query(SysSharding.lastdate).filter(and_(SysSharding.code==code,SysSharding.dtype==dtype)).limit(1).first()
            if time_keys is not None :
                for time in time_keys:
                    # if time is None:
                    #     time = self._find_lastdate(code,dtype)
                    return time
        except IOError as err:
            logging.error("OS|error: {0}".format(err))
        else:
            pass
        return None

    def find_lastdate_and_tindex(self,code,dtype):
        '''
        sys_sharding表里取得最后时间和索引
        :param code:
        :param dtype:
        :return:
        '''
        try:
            records  = self.mysqlStore.session.query(SysSharding.lastdate,SysSharding.tindex).filter(and_(SysSharding.code==code,SysSharding.dtype==dtype)).limit(1).first()
            if records is not None:
                lastdate,tindex = records
                # if lastdate is None:
                #     lastdate =  self._find_lastdate(code,dtype)
            else:
                return None, self._get_last_index(dtype)

            return lastdate, tindex
        except IOError as err:
            logging.error("OS|error: {0}".format(err))
        else:
            pass
        return None

    def update_lastdate(self, code, dtype, lastest_date):
        '''
        update sys_sharding table for setting lastdate
        :param code:
        :param dtype:
        :param lastest_date:
        :return:
        '''
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
