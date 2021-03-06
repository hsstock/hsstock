# -*- coding: UTF-8 -*-
import logging
import sqlalchemy as sa
import pandas as pd

from hsstock.service.mysql_service import MysqlService
from hsstock.utils.app_logging import setup_logging

def main():

    storeservice = MysqlService(2)


    # The total number of history tables is 16, but last table is 9
    kline_tables_number = 17
    schemaArr = [
        {
            "table": "ft_kline_{0}",
            "dtype": {
                "id": sa.types.BIGINT,
                "code": sa.types.NVARCHAR(20),
                "time_key": sa.types.DATETIME,
                "open": sa.types.FLOAT,
                "close": sa.types.FLOAT,
                "high": sa.types.FLOAT,
                "low": sa.types.FLOAT,
                "pe_ratio": sa.types.FLOAT,
                "turnover_rate": sa.types.FLOAT,
                "volume": sa.types.BIGINT,
                "turnover": sa.types.FLOAT,
                "change_rate": sa.types.FLOAT,
                "last_close": sa.types.FLOAT
            },
            "clauses": [
                'ALTER TABLE `{0}` ADD PRIMARY  KEY (`id`);',
                'ALTER TABLE `{0}` ADD UNIQUE INDEX (`code`,`time_key`);',
                'ALTER TABLE `{0}` MODIFY COLUMN id BIGINT NOT NULL AUTO_INCREMENT COMMENT  \'id\'',
                'ALTER TABLE `{0}` MODIFY COLUMN pe_ratio FLOAT COMMENT  \'市盈率\';',
                'ALTER TABLE `{0}` MODIFY COLUMN turnover_rate FLOAT COMMENT  \'换手率\';',
                'ALTER TABLE `{0}` MODIFY COLUMN volume BIGINT COMMENT  \'成交量\';',
                'ALTER TABLE `{0}` MODIFY COLUMN turnover FLOAT COMMENT  \'成交额\';',
                'ALTER TABLE `{0}` MODIFY COLUMN change_rate FLOAT COMMENT  \'涨跌幅\';',
                'ALTER TABLE `{0}` MODIFY COLUMN last_close FLOAT COMMENT  \'昨收价\';',
                'ALTER TABLE `{0}` ENGINE=MyISAM;'
            ]
        },
    ]

    try:
        logging.info("create sub kline schema,  starting")

        for  index in range(1,kline_tables_number,1):
            for schema in schemaArr:
                df = pd.DataFrame(None, columns=schema['dtype'].keys())
                table = schema['table'].format(index)
                logging.info(table)
                logging.info('table:{0}'.format(table))
                clauses = []
                for clause in schema['clauses']:
                    clause = clause.format(table)
                    clauses.append(clause)
                storeservice.init_schema(table, df, schema['dtype'], clauses)

        logging.info("create sub kline, end")
    except IOError as err:
        logging.error("OS|error: {0}".format(err))
    else:
        logging.info('create sub kline success')


    union_table = [('ft_kline_{0}'.format(table)) for table in range(1, kline_tables_number, 1)]
    mrg_kline_claus = 'ALTER TABLE `{0}` ENGINE = MRG_MyISAM UNION = ({1}) INSERT_METHOD = LAST;'.format({0}, ','.join(union_table))
    schemaArr = [
        {
            "table": "ft_kline",
            "dtype": {
                "id": sa.types.BIGINT,
                "code": sa.types.NVARCHAR(20),
                "time_key": sa.types.DATETIME,
                "open": sa.types.FLOAT,
                "close": sa.types.FLOAT,
                "high": sa.types.FLOAT,
                "low": sa.types.FLOAT,
                "pe_ratio": sa.types.FLOAT,
                "turnover_rate": sa.types.FLOAT,
                "volume": sa.types.BIGINT,
                "turnover": sa.types.FLOAT,
                "change_rate": sa.types.FLOAT,
                "last_close": sa.types.FLOAT
            },
            "clauses": [
                'ALTER TABLE `{0}` ADD PRIMARY  KEY (`id`);',
                'ALTER TABLE `{0}` ADD UNIQUE INDEX (`code`,`time_key`);',
                'ALTER TABLE `{0}` MODIFY COLUMN id BIGINT NOT NULL AUTO_INCREMENT COMMENT  \'id\'',
                'ALTER TABLE `{0}` MODIFY COLUMN pe_ratio FLOAT COMMENT  \'市盈率\';',
                'ALTER TABLE `{0}` MODIFY COLUMN turnover_rate FLOAT COMMENT  \'换手率\';',
                'ALTER TABLE `{0}` MODIFY COLUMN volume BIGINT COMMENT  \'成交量\';',
                'ALTER TABLE `{0}` MODIFY COLUMN turnover FLOAT COMMENT  \'成交额\';',
                'ALTER TABLE `{0}` MODIFY COLUMN change_rate FLOAT COMMENT  \'涨跌幅\';',
                'ALTER TABLE `{0}` MODIFY COLUMN last_close FLOAT COMMENT  \'昨收价\';',
                mrg_kline_claus
            ]
        }
    ]
    try:
        logging.info("create kline schema,  starting")

        for schema in schemaArr:
            df = pd.DataFrame(None, columns=schema['dtype'].keys())
            table = schema['table']
            logging.info(table)
            logging.info('table:{0}'.format(table))
            clauses = []
            for clause in schema['clauses']:
                clause = clause.format(table)
                clauses.append(clause)
            storeservice.init_schema(table, df, schema['dtype'], clauses)

        logging.info("create kline, end")
    except IOError as err:
        logging.error("OS|error: {0}".format(err))
    else:
        logging.info('create kline success')

if __name__ == "__main__":
    setup_logging()
    main()
