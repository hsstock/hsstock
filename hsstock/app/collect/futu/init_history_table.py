# -*- coding: UTF-8 -*-
import logging
import sqlalchemy as sa
import pandas as pd

from hsstock.service.mysql_service import MysqlService
from hsstock.utils.app_logging import setup_logging
import hsstock.utils.logger as logger

def main():

    #192.168.1.101 数据库
    storeservice2 = MysqlService(2)
    #10.0.0.1
    storeservice = MysqlService()

    init_history_table(storeservice,storeservice2)



def init_history_table(storeservice,storeservice2):
    """
    1)获取10.0.0.1种ft_stock_basicinfo表中所有(code,name)
    2)192.168.1.101中生成日线，5分钟线，1分钟线，一只一表
     ft_kline_code_name
     ft_1M_code_name
     ft_5M_code_name
    3)生成merged表
    ft_kline
    ft_1m
    ft_5m
    :param storeservice:
    :return:
    """
    arr = storeservice.find_all_stock_codeandname()
    for code,name in arr:
        print('code:{0} name:{1}'.format(code,name))


if __name__ == "__main__":
    setup_logging()
    main()
