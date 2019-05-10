# -*- coding: UTF-8 -*-
import logging
import sqlalchemy as sa
import pandas as pd

from hsstock.service.mysql_service import MysqlService
from hsstock.utils.app_logging import setup_logging
import hsstock.utils.logger as logger

def main():

    storeservice = MysqlService()


    from_table = 230
    to_table = 233


    migrate_num = 5

    try:
        for index in range(0,50,1):
            logger.info('addressing {0} ....'.format(index))
            # step 1: fetch one code
            sql = 'select distinct(code) from ft_1M_{0} limit {1}'.format(from_table,migrate_num)
            result = storeservice.executeSql(sql)
            codes = tuple([code[0]  for code in result.cursor._result.rows])
            print(codes)

            # step 2: insert into new table
            sql = 'insert into ft_1M_{0} select * from ft_1M_{1} where code in {2}'.format(to_table,from_table,codes)
            logger.info(sql)
            result = storeservice.executeSql(sql)


            # step 3: update sys_sharding.tindex
            sql = 'update sys_sharding set tindex = {0} where code in {1} and dtype = \"hk_1m\"'.format(to_table,codes)
            logger.info(sql)
            result = storeservice.executeSql(sql)


            # step 4: drop records from from_table
            sql = 'delete from ft_1M_{0} where code in {1}'.format(from_table,codes)
            logger.info(sql)
            result = storeservice.executeSql(sql)

    except Exception as err:
        logger.info(err)


if __name__ == "__main__":
    setup_logging()
    main()
