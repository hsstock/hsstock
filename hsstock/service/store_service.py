# -*- coding: UTF-8 -*-

from abc import ABC

from sqlalchemy import create_engine
import sqlalchemy as sa

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

    def insert_many(self,table, df, if_exists='append', index=False, index_label=None):
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

    # def insert_many(self, table, df, if_exists='replace', index=False, index_label=None):
    #     df.to_sql(table, self.engine, if_exists = 'replace' if if_exists ==  None else if_exists,
    #               index = False if index == False else True,
    #               index_label = None if index_label == None else index_label,
    #               dtype = {
    #             'code': sa.types.NVARCHAR(10),'index':sa.types.BIGINT,'name':sa.types.NVARCHAR(20),
    #             'time': sa.types.TIME, 'price': sa.types.FLOAT, 'volume': sa.types.BIGINT,
    #             'preprice': sa.types.FLOAT, 'type': sa.types.NVARCHAR(10),'date':sa.types.DATE
    #         })
    #     with self.engine.connect() as con:
    #         con.execute('ALTER TABLE `ts_sina_dd` ADD PRIMARY KEY (`index`);')
    #         con.execute('ALTER TABLE `ts_sina_dd` ADD INDEX (`code`);')
    #
    #     pass

    def insert_many(self, table, df, if_exists='append', index=False, index_label=None):
        df.to_sql(table, self.engine, if_exists = 'append' if if_exists ==  None else if_exists,
                  index=False if index == False else True,
                  index_label = None if index_label == None else index_label
                  )
        pass

    # dtype = {'sighting_placename': sa.types.CLOB(50), 'firstname': sa.types.CLOB(50),
    #          'sight_place_id': sa.types.CLOB(50), 'userdevice_id': sa.types.CLOB(50), 'lastname': sa.types.CLOB(50),
    #          'created_at': sa.types.DATETIME(), 'sighting_longitude': sa.types.Float,
    #          'sighting_device_name': sa.types.CLOB(50), 'sighting_battery': sa.types.BIGINT,
    #          'sighting_latitude': sa.types.Float, 'sighting_rssi': sa.types.BIGINT,
    #          'sighted_device_id': sa.types.CLOB(50), 'user_device_typ': sa.types.CLOB(50),
    #          'sighting_temperature': sa.types.BIGINT, 'owner_id': sa.types.CLOB(50)}
    #
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