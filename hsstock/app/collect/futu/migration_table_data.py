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

    #init_history_data_table(storeservice)
    storeservice = MysqlService()
    migration_table_and_data(storeservice)
    #migration_data(storeservice)

def migration_data(storeservice):
    """
        在新数据库中生成初始数据表
        1) 删除原来索引，添加新的组合索引：
            alter table test drop index `key`;
            'ALTER TABLE `{0}` ADD INDEX (`code`);',
            'ALTER TABLE `{0}` ADD INDEX (`time_key`);',
            =》
            'ALTER TABLE `{0}` ADD UNIQUE INDEX (`code,time_key`);',
            废弃，建一个模板拷贝
            create table ft_kline_1
        (
            id            bigint auto_increment comment 'id'
                primary key,
            code          varchar(20) charset utf8 null,
            time_key      datetime                 null,
            open          float                    null,
            close         float                    null,
            high          float                    null,
            low           float                    null,
            pe_ratio      float                    null comment '市盈率',
            turnover_rate float                    null comment '换手率',
            volume        bigint                   null comment '成交量',
            turnover      float                    null comment '成交额',
            change_rate   float                    null comment '涨跌幅',
            last_close    float                    null comment '昨收价',
            constraint code_timekey
                unique (code, time_key)
        )
            engine = MyISAM;

        2）MysqlService
            改成连接参数可以设置，这样支持多个数据库连接

        3）生成数据表结构
        4）迁移所有表
            a）找出本表set(代码)
    :param storeservice:
    :return:
    """
    for table_index in range(1, 16 + 1, 1):
        migration_one_table(storeservice, 'ft_kline_', table_index)
    # 2)迁移5分钟数据：ft_5M_(1~80)表,range作闭右开,查看ft_5m


    for table_index in range(1, 80 + 1, 1):
        migration_one_table(storeservice, 'ft_5M_', table_index)
        # # 2)迁移1分钟数据：ft_1M_(1~266)表,range作闭右开,查看ft_1m
    for table_index in range(1, 266 + 1, 1):
        migration_one_table(storeservice, 'ft_1M_', table_index)

def migration_one_table(storeservice,table_prefix,table_index):
    pass

def init_history_data_table(storeservice):
    for table_index in range(1, 16 + 1, 1):
        copy_table_from_template(storeservice, 'ft_kline_', table_index)
    # 2)迁移5分钟数据：ft_5M_(1~80)表,range作闭右开,查看ft_5m
    for table_index in range(1, 80 + 1, 1):
        copy_table_from_template(storeservice, 'ft_5M_', table_index)
    # # 2)迁移1分钟数据：ft_1M_(1~266)表,range作闭右开,查看ft_1m
    for table_index in range(1, 266 + 1, 1):
        copy_table_from_template(storeservice, 'ft_1M_', table_index)

def copy_table_from_template(storeservice,table_prefix,table_index):

    old_table = '{0}{1}'.format(table_prefix, table_index)

    # 2）复制模板表结构到新表

    try:
        print("复制模板表结构到新表{0}".format(old_table))
        sql = "CREATE TABLE IF NOT EXISTS {0} LIKE ft_history_template".format(old_table)
        result = storeservice.executeSql(sql)
        print(result)
    except Exception as e:
        print(e)


def migration_table_and_data(storeservice):
    # 1)迁移日线数据：ft_kline_(1~16)表,range作闭右开,查看ft_kline
    for table_index in range(1, 16 + 1, 1):
        migration_table(storeservice, 'ft_kline_', table_index)
    # 2)迁移5分钟数据：ft_5M_(1~80)表,range作闭右开,查看ft_5m
    for table_index in range(1, 80 + 1, 1):
        migration_table(storeservice, 'ft_5M_', table_index)
    # # 2)迁移1分钟数据：ft_1M_(1~266)表,range作闭右开,查看ft_1m
    for table_index in range(1, 266 + 1, 1):
        migration_table(storeservice, 'ft_1M_', table_index)


def migration_table(storeservice,table_prefix,table_index):
    # 1) table_prefix,table_index 生成新旧表名

    old_table = '{0}{1}'.format(table_prefix,table_index)
    new_table = '{0}{1}_new'.format(table_prefix,table_index)

    # 2）复制模板表结构到新表

    try:
        print("复制模板表结构到新表{0}".format( new_table ))
        sql = "CREATE TABLE IF NOT EXISTS {0} LIKE ft_history_template".format(new_table)
        result = storeservice.executeSql(sql)
        print(result)
    except Exception as e:
        print(e)


    try:
        print("为新表{0}生成组合索引".format( new_table ))
        sql = "CREATE UNIQUE INDEX `code_timekey` on {0}(code,time_key)".format(new_table)
        result = storeservice.executeSql(sql)
        print(result)
    except Exception as e:
        print(e)

    # 3）迁移老表数据到新表，达到去重目的

    try:
        print("迁移老表{0}数据到新表{1}，达到去重目的".format( old_table,new_table ))
        # bug 模板里的索引一直没变
        sql = "INSERT IGNORE INTO {0} SELECT * FROM {1}".format(new_table,old_table)
        result = storeservice.executeSql(sql)
        print(result)
    except Exception as e:
        print(e)


    # 4）删除老表

    try:
        print("删除老表{0}".format(old_table))
        sql = "DROP TABLE  {0}".format(old_table)
        result = storeservice.executeSql(sql)
        print(result)
    except Exception as e:
        print(e)


    # 5）改名新表为老表名
    try:
        print("改名新表{0}为老表名{1}".format(new_table,old_table))
        sql = "RENAME TABLE {0} TO {1}".format(new_table,old_table)
        result = storeservice.executeSql(sql)
        print(result)
    except Exception as e:
        print(e)

if __name__ == "__main__":
    setup_logging()
    main()
