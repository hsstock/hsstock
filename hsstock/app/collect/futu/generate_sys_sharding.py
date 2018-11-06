# -*- coding: UTF-8 -*-
import logging
import sqlalchemy as sa
import pandas as pd

from hsstock.service.mysql_service import MysqlService
from hsstock.utils.app_logging import setup_logging

def main():

    storeservice = MysqlService()


    kline_tables_number = 17
    kline_5M_tables_number = 81
    kline_1M_tables_number = 267

    for index in range(1,kline_tables_number,1):
        sql = 'INSERT INTO sys_sharding(code, dtype, tindex,lastdate) SELECT code, \'hk\' as dtype, {0} as tindex, time_key as lastdate from (SELECT code,max(time_key) FROM ft_kline_{1}) group by code as tmp1'.format(index,index)
        storeservice.executeSql(sql)

    for index in range(1,kline_5M_tables_number,1):
        sql = 'INSERT INTO sys_sharding(code, dtype, tindex,lastdate) SELECT code, \'hk_5m\' as dtype, {0} as tindex, time_key as lastdate  from (SELECT code, max(time_key) FROM ft_5M_{1}) group by code as tmp1'.format(index,index)
        storeservice.executeSql(sql)

    for index in range(1,kline_1M_tables_number,1):
        sql = 'INSERT INTO sys_sharding(code, dtype, tindex, lastdate) SELECT code, \'hk_1m\' as dtype, {0} as tindex time_key as lastdate from (SELECT code, max(time_key) FROM ft_1M_{1}) group by code as tmp1'.format(index,index)
        storeservice.executeSql(sql)

if __name__ == "__main__":
    setup_logging()
    main()
