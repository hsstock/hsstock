# -*- coding: UTF-8 -*-
import logging
import sqlalchemy as sa
import pandas as pd

from hsstock.service.mysql_service import MysqlService
from hsstock.utils.app_logging import setup_logging
import hsstock.utils.logger as logger

def main():

    storeservice = MysqlService()

    deal_1m(storeservice)


def deal_1m(storeservice):
    from_table = 230
    to_table = 235

    migrate_num = 5


    try:
        for index in range(0, 500, 1):
            logger.info('addressing {0} ....'.format(index))
            # # step 1: fetch one code
            sql = 'select distinct(code) from ft_1M_{0}  limit {1} offset {2} '.format(from_table, migrate_num,index)
            result = storeservice.executeSql(sql)
            codes = tuple([code[0] for code in result.cursor._result.rows])
            print(codes)

            codes = [code[0] for code in result.cursor._result.rows]
            code = codes[0]
            print(code)

            try:
                # step 2: insert into new table
                sql = 'insert into ft_1M_{0} select * from ft_1M_{1} where code = \"{2}\"'.format(to_table, from_table, code)
                logger.info(sql)
                result = storeservice.executeSql(sql)

                # step 3: update sys_sharding.tindex
                sql = 'update sys_sharding set tindex = {0} where code = \"{1}\" and dtype = \"hk_1m\"'.format(to_table, code)
                logger.info(sql)
                result = storeservice.executeSql(sql)

                # step 4: drop records from from_table
                sql = 'delete from ft_1M_{0} where code = \"{1}\"'.format(from_table, code)
                logger.info(sql)
                result = storeservice.executeSql(sql)
            except Exception as e:
                pass

    except Exception as err:
        logger.info(err)

def deal_1m_old():
    from_table = 230
    to_table = 235

    migrate_num = 5

    try:
        for index in range(0, 30, 1):
            logger.info('addressing {0} ....'.format(index))
            # # step 1: fetch one code
            sql = 'select distinct(code) from ft_1M_{0} limit {1}'.format(from_table, migrate_num)
            result = storeservice.executeSql(sql)
            codes = tuple([code[0] for code in result.cursor._result.rows])
            print(codes)
            # step 2: insert into new table
            sql = 'insert into ft_1M_{0} select * from ft_1M_{1} where code in {2}'.format(to_table, from_table, codes)
            logger.info(sql)
            result = storeservice.executeSql(sql)

            # step 3: update sys_sharding.tindex
            sql = 'update sys_sharding set tindex = {0} where code in {1} and dtype = \"hk_1m\"'.format(to_table, codes)
            logger.info(sql)
            result = storeservice.executeSql(sql)

            # step 4: drop records from from_table
            sql = 'delete from ft_1M_{0} where code in {1}'.format(from_table, codes)
            logger.info(sql)
            result = storeservice.executeSql(sql)

    except Exception as err:
        logger.info(err)


def counter_statistics():

    storeservice = MysqlService()


    index = 0
    to_table = 234


    try:
        for index in range(1,250,1):
            logger.info('addressing {0} ....'.format(index))
            # step 1: fetch one code
            sql = 'select count(code) from ft_1M_{0}'.format(index)
            result = storeservice.executeSql(sql)
            print(result.cursor._result.rows[0])

    except Exception as err:
        logger.info(err)



if __name__ == "__main__":
    setup_logging()
    main()
    #counter_statistics()
