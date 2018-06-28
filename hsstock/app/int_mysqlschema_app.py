# -*- coding: UTF-8 -*-
import logging
import sqlalchemy as sa
import pandas as pd

from hsstock.service.store_service import StoreService
from hsstock.utils.app_logging import setup_logging


def main():

    storeservice = StoreService()

    schemaArr = [
          {
            "table":"ts_sina_dd",
            "dtype":{
                     'code': sa.types.NVARCHAR(10), 'name': sa.types.NVARCHAR(20),
                     'time': sa.types.TIME, 'price': sa.types.FLOAT, 'volume': sa.types.BIGINT,
                     'preprice': sa.types.FLOAT, 'type': sa.types.NVARCHAR(10), 'date': sa.types.DATE
            },
            "clauses":[
                'ALTER TABLE `{0}` ADD INDEX (`code`);'
            ]
          }
        ]

    try:
        logging.info("int_schema,  starting")

        for schema in schemaArr:
            df = pd.DataFrame(None,columns=schema['dtype'].keys())
            table = schema['table']
            clauses = []
            for clause in schema['clauses']:
                clause = clause.format(table)
                clauses.append(clause)
            storeservice.init_schema(table,df,schema['dtype'],clauses)

        logging.info("int_schema, end")
    except IOError as err:
        logging.error("OS|error: {0}".format(err))
    else:
        logging.info('init schema success')

if __name__ == "__main__":
    setup_logging()
    main()
