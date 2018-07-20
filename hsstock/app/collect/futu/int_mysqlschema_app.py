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
            "table": "ft_stock_basicinfo",
            "dtype": {
                "code": sa.types.NVARCHAR(20),
                "name": sa.types.NVARCHAR(200),
                "lot_size": sa.types.BIGINT,
                "stock_type": sa.types.NVARCHAR(30),
                "stock_child_type": sa.types.NVARCHAR(30),
                "stock_owner": sa.types.NVARCHAR(30),
                "listing_date": sa.types.DATE,
                "stock_id": sa.types.BIGINT
            },
            "clauses": [
                'ALTER TABLE `{0}` ADD INDEX (`name`);',
                'ALTER TABLE `{0}` ADD INDEX (`code`);',
                'ALTER TABLE `{0}` ADD INDEX (`stock_type`);',
                'ALTER TABLE `{0}` MODIFY COLUMN lot_size BIGINT COMMENT  \'每手数量\';'
                'ALTER TABLE `{0}` MODIFY COLUMN stock_type VARCHAR(30) COMMENT  \'股票类型，参见SecurityType\';'
                'ALTER TABLE `{0}` MODIFY COLUMN stock_child_type VARCHAR(30) COMMENT  \'涡轮子类型，参见WrtType\';'
                'ALTER TABLE `{0}` MODIFY COLUMN stock_owner VARCHAR(30) COMMENT  \'正股代码\';'
                'ALTER TABLE `{0}` MODIFY COLUMN listing_date DATE COMMENT  \'上市时间\';'
                'ALTER TABLE `{0}` MODIFY COLUMN stock_id BIGINT COMMENT  \'股票id\';'
            ]
        },
        {
            "table": "ft_history_kline",
            "dtype": {
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
                'ALTER TABLE `{0}` ADD INDEX (`code`);',
                'ALTER TABLE `{0}` ADD INDEX (`time_key`);'
                'ALTER TABLE `{0}` MODIFY COLUMN pe_ratio FLOAT COMMENT  \'市盈率\';'
                'ALTER TABLE `{0}` MODIFY COLUMN turnover_rate FLOAT COMMENT  \'换手率\';'
                'ALTER TABLE `{0}` MODIFY COLUMN volume BIGINT COMMENT  \'成交量\';'
                'ALTER TABLE `{0}` MODIFY COLUMN turnover FLOAT COMMENT  \'成交额\';'
                'ALTER TABLE `{0}` MODIFY COLUMN change_rate FLOAT COMMENT  \'涨跌幅\';'
                'ALTER TABLE `{0}` MODIFY COLUMN last_close FLOAT COMMENT  \'昨收价\';'
            ]
        },
        {
            "table": "ft_history_kline_K_5M",
            "dtype": {
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
                'ALTER TABLE `{0}` ADD INDEX (`code`);',
                'ALTER TABLE `{0}` ADD INDEX (`time_key`);'
                'ALTER TABLE `{0}` MODIFY COLUMN pe_ratio FLOAT COMMENT  \'市盈率\';'
                'ALTER TABLE `{0}` MODIFY COLUMN turnover_rate FLOAT COMMENT  \'换手率\';'
                'ALTER TABLE `{0}` MODIFY COLUMN volume BIGINT COMMENT  \'成交量\';'
                'ALTER TABLE `{0}` MODIFY COLUMN turnover FLOAT COMMENT  \'成交额\';'
                'ALTER TABLE `{0}` MODIFY COLUMN change_rate FLOAT COMMENT  \'涨跌幅\';'
                'ALTER TABLE `{0}` MODIFY COLUMN last_close FLOAT COMMENT  \'昨收价\';'
            ]
        },
        {
            "table": "ft_broker",
            "dtype": {
                "code": sa.types.NVARCHAR(20),
                "bid_broker_id": sa.types.BIGINT,
                "bid_broker_name": sa.types.NVARCHAR(100),
                "bid_broker_pos": sa.types.BIGINT,
                "ask_broker_id": sa.types.BIGINT,
                "ask_broker_name": sa.types.NVARCHAR(100),
                "ask_broker_pos": sa.types.BIGINT
            },
            "clauses": [
                'ALTER TABLE `{0}` ADD INDEX (`code`);',
            ]
        },
        {
            "table": "ft_rtdata",
            "dtype": {
                "code": sa.types.NVARCHAR(20),
                "time": sa.types.DATETIME,
                "is_blank": sa.types.INT,
                "opened_mins": sa.types.INT,
                "cur_price": sa.types.FLOAT,
                "last_close": sa.types.FLOAT,
                "avg_price": sa.types.FLOAT,
                "turnover": sa.types.FLOAT,
                "volume": sa.types.FLOAT
             },
            "clauses": [
                'ALTER TABLE `{0}` ADD INDEX (`code`);',
                'ALTER TABLE `{0}` ADD INDEX (`time`);'
                'ALTER TABLE `{0}` MODIFY COLUMN opened_mins INT COMMENT  \'零点到当前多少分钟\';'
                'ALTER TABLE `{0}` MODIFY COLUMN cur_price FLOAT COMMENT  \'当前价格\';'
                'ALTER TABLE `{0}` MODIFY COLUMN last_close FLOAT COMMENT  \'昨天收盘的价格\';'
                'ALTER TABLE `{0}` MODIFY COLUMN avg_price FLOAT COMMENT  \'平均价格\';'
                'ALTER TABLE `{0}` MODIFY COLUMN turnover FLOAT COMMENT  \'成交额\';'
                'ALTER TABLE `{0}` MODIFY COLUMN volume FLOAT COMMENT  \'成交量\';'
            ]
        },
        {
            "table": "ft_stockquote",
            "dtype": {
                "code": sa.types.NVARCHAR(20),
                "data_date": sa.types.DATE,
                "data_time": sa.types.TIME,
                "last_price": sa.types.FLOAT,
                "open_price": sa.types.FLOAT,
                "high_price": sa.types.FLOAT,
                "low_price": sa.types.FLOAT,
                "prev_close_price": sa.types.FLOAT,
                "volume": sa.types.BIGINT,
                "turnover": sa.types.FLOAT,
                "turnover_rate": sa.types.FLOAT,
                "amplitude": sa.types.INT,
                "suspension": sa.types.BOOLEAN,
                "listing_date": sa.types.DATE,
                "price_spread": sa.types.FLOAT,
            },
            "clauses": [
                'ALTER TABLE `{0}` ADD INDEX (`code`);',
                'ALTER TABLE `{0}` ADD INDEX (`data_date`);'
                'ALTER TABLE `{0}` ADD INDEX (`data_time`);'
                'ALTER TABLE `{0}` MODIFY COLUMN turnover FLOAT COMMENT  \'成交金额\';'
                'ALTER TABLE `{0}` MODIFY COLUMN turnover_rate FLOAT COMMENT  \'换手率\';'
                'ALTER TABLE `{0}` MODIFY COLUMN amplitude INT COMMENT  \'振幅\';'
                'ALTER TABLE `{0}` MODIFY COLUMN suspension BOOL COMMENT  \'是否停牌(True表示停牌)\';'
                'ALTER TABLE `{0}` MODIFY COLUMN listing_date DATE COMMENT  \'上市日期\';'
                'ALTER TABLE `{0}` MODIFY COLUMN price_spread FLOAT COMMENT  \'当前价差，亦即摆盘数据的买档或卖档的相邻档位的报价差\';'
             ]
        },
        {
            "table": "ft_ticker",
            "dtype": {
                "code": sa.types.NVARCHAR(20),
                "time": sa.types.DATETIME,
                "price": sa.types.FLOAT,
                "volume": sa.types.BIGINT,
                "turnover": sa.types.FLOAT,
                "ticker_direction": sa.types.VARCHAR(20),
                "sequence": sa.types.VARCHAR(50),
                "recv_time": sa.types.DATETIME,
            },
            "clauses": [
                'ALTER TABLE `{0}` ADD INDEX (`code`);',
                'ALTER TABLE `{0}` ADD INDEX (`time`);'
                'ALTER TABLE `{0}` ADD INDEX (`sequence`);',
                'ALTER TABLE `{0}` MODIFY COLUMN turnover FLOAT COMMENT  \'成交金额\';',
                'ALTER TABLE `{0}` MODIFY COLUMN volume BIGINT COMMENT  \'成交数量(股数)\';',
                'ALTER TABLE `{0}` MODIFY COLUMN ticker_direction VARCHAR(20) COMMENT  \'逐笔方向\';',
                'ALTER TABLE `{0}` MODIFY COLUMN sequence VARCHAR(50) COMMENT  \'逐笔序号\';',
            ]
        },
        {
            "table": "ft_tradeorder",
            "dtype": {
                "code": sa.types.NVARCHAR(20),
                "stock_name": sa.types.NVARCHAR(100),
                "dealt_avg_price": sa.types.FLOAT,
                "dealt_qty": sa.types.FLOAT,
                "qty": sa.types.FLOAT,
                "order_id": sa.types.NVARCHAR(50),
                "order_type": sa.types.NVARCHAR(20),
                "price": sa.types.FLOAT,
                "order_status": sa.types.NVARCHAR(20),
                "create_time": sa.types.DATETIME,
                "updated_time": sa.types.DATETIME,
                "trd_side": sa.types.NVARCHAR(20),
                "last_err_msg": sa.types.NVARCHAR(1000),
                "trd_market": sa.types.NVARCHAR(30),
                "trd_env": sa.types.NVARCHAR(30),
            },
            "clauses": [
                'ALTER TABLE `{0}` ADD INDEX (`code`);',
                'ALTER TABLE `{0}` ADD INDEX (`stock_name`);',
                'ALTER TABLE `{0}` ADD INDEX (`create_time`);'
                'ALTER TABLE `{0}` MODIFY COLUMN dealt_avg_price FLOAT COMMENT  \'成交均价，无精度限制\';',
                'ALTER TABLE `{0}` MODIFY COLUMN dealt_qty FLOAT COMMENT  \'成交数量，2位精度，期权单位是”张”\';',
                'ALTER TABLE `{0}` MODIFY COLUMN qty FLOAT COMMENT  \'订单数量，2位精度，期权单位是”张”\';',
            ]
        },
        {
            "table": "ft_tradedetail",
            "dtype": {
                "code": sa.types.NVARCHAR(20),
                "stock_name": sa.types.NVARCHAR(100),
                "trd_env": sa.types.NVARCHAR(20),
                "deal_id": sa.types.NVARCHAR(50),
                "order_id": sa.types.NVARCHAR(50),
                "qty": sa.types.FLOAT,
                "price": sa.types.FLOAT,
                "trd_side": sa.types.NVARCHAR(20),
                "create_time": sa.types.DATETIME,
                "counter_broker_id": sa.types.INT,
                "counter_broker_name": sa.types.NVARCHAR(100),
                "trd_market": sa.types.NVARCHAR(50),
            },
            "clauses": [
                'ALTER TABLE `{0}` ADD INDEX (`code`);',
                'ALTER TABLE `{0}` ADD INDEX (`stock_name`);'
                'ALTER TABLE `{0}` ADD INDEX (`create_time`);',
                'ALTER TABLE `{0}` MODIFY COLUMN trd_env VARCHAR(20) COMMENT  \'交易环境\';',
                'ALTER TABLE `{0}` MODIFY COLUMN deal_id VARCHAR(50) COMMENT  \'成交号\';',
                'ALTER TABLE `{0}` MODIFY COLUMN order_id VARCHAR(50) COMMENT  \'订单号\';',
                'ALTER TABLE `{0}` MODIFY COLUMN qty FLOAT COMMENT  \'成交数量，2位精度，期权单位是”张”\';',
                'ALTER TABLE `{0}` MODIFY COLUMN price FLOAT COMMENT  \'成交价格，3位精度(A股2位)\';',
                'ALTER TABLE `{0}` MODIFY COLUMN trd_side VARCHAR(20) COMMENT  \'交易方向\';',
                'ALTER TABLE `{0}` MODIFY COLUMN counter_broker_id INT COMMENT  \'对手经纪号，港股有效\';',
                'ALTER TABLE `{0}` MODIFY COLUMN counter_broker_name VARCHAR(100) COMMENT  \'对手经纪名称，港股有效\';',
                'ALTER TABLE `{0}` MODIFY COLUMN trd_market VARCHAR(50) COMMENT  \'交易市场\';',
            ]
        },
        {
            "table": "ft_autype",
            "dtype": {
                "code": sa.types.NVARCHAR(20),
                "ex_div_date": sa.types.DATE,
                "split_ratio": sa.types.FLOAT,
                "per_cash_div": sa.types.FLOAT,
                "per_share_div_ratio": sa.types.FLOAT,
                "per_share_trans_ratio": sa.types.FLOAT,
                "allotment_ratio": sa.types.FLOAT,
                "allotment_price": sa.types.FLOAT,
                "stk_spo_ratio": sa.types.FLOAT,
                "stk_spo_price": sa.types.FLOAT,
                "forward_adj_factorA": sa.types.FLOAT,
                "forward_adj_factorB": sa.types.FLOAT,
                "backward_adj_factorA": sa.types.FLOAT,
                "backward_adj_factorB": sa.types.FLOAT
            },
            "clauses": [
                'ALTER TABLE `{0}` ADD INDEX (`code`);',
                'ALTER TABLE `{0}` ADD INDEX (`ex_div_date`);'
                'ALTER TABLE `{0}` MODIFY COLUMN ex_div_date DATE COMMENT  \'除权除息日\';'
                'ALTER TABLE `{0}` MODIFY COLUMN split_ratio FLOAT COMMENT  \'拆合股比例； double，例如，对于5股合1股为1/5，对于1股拆5股为5/1\';'
                'ALTER TABLE `{0}` MODIFY COLUMN per_cash_div FLOAT COMMENT  \'每股派现\';'
                'ALTER TABLE `{0}` MODIFY COLUMN per_share_div_ratio FLOAT COMMENT  \'每股送股比例\';'
                'ALTER TABLE `{0}` MODIFY COLUMN per_share_trans_ratio FLOAT COMMENT  \'每股转增股比例\';'
                'ALTER TABLE `{0}` MODIFY COLUMN allotment_ratio FLOAT COMMENT  \'每股配股比例\';'
                'ALTER TABLE `{0}` MODIFY COLUMN allotment_price FLOAT COMMENT  \'配股价\';'
                'ALTER TABLE `{0}` MODIFY COLUMN stk_spo_ratio FLOAT COMMENT  \'增发比例\';'
                'ALTER TABLE `{0}` MODIFY COLUMN stk_spo_price FLOAT COMMENT  \'增发价格\';'
                'ALTER TABLE `{0}` MODIFY COLUMN forward_adj_factorA FLOAT COMMENT  \'前复权因子A\';'
                'ALTER TABLE `{0}` MODIFY COLUMN forward_adj_factorB FLOAT COMMENT  \'前复权因子B\';'
                'ALTER TABLE `{0}` MODIFY COLUMN backward_adj_factorA FLOAT COMMENT  \'后复权因子A\';'
                'ALTER TABLE `{0}` MODIFY COLUMN backward_adj_factorB FLOAT COMMENT  \'后复权因子B\';'
            ]
        },
        {
            "table": "ft_market_snapshot",
            "dtype": {
                "code": sa.types.NVARCHAR(20),
                "update_time": sa.types.DATETIME,
                "last_price": sa.types.FLOAT,
                "open_price": sa.types.FLOAT,
                "high_price": sa.types.FLOAT,
                "low_price": sa.types.FLOAT,
                "prev_close_price": sa.types.FLOAT,
                "volume": sa.types.BIGINT,
                "turnover": sa.types.BIGINT,
                "turnover_rate": sa.types.FLOAT,
                "suspension": sa.types.INT,
                "listing_date": sa.types.DATE,
                "circular_market_val": sa.types.FLOAT,
                "low_price": sa.types.FLOAT,
                "total_market_val": sa.types.FLOAT,
                "wrt_valid": sa.types.INT,
                "wrt_conversion_ratio": sa.types.FLOAT,
                "wrt_type": sa.types.FLOAT,
                "wrt_strike_price": sa.types.FLOAT,
                "wrt_maturity_date": sa.types.DATE,
                "wrt_end_trade": sa.types.DATE,
                "wrt_code": sa.types.FLOAT,
                "wrt_recovery_price": sa.types.FLOAT,
                "wrt_street_vol": sa.types.FLOAT,
                "wrt_issue_vol": sa.types.FLOAT,
                "wrt_street_ratio": sa.types.FLOAT,
                "wrt_delta": sa.types.FLOAT,
                "wrt_implied_volatility": sa.types.FLOAT,
                "wrt_premium": sa.types.FLOAT,
                "lot_size": sa.types.BIGINT,
                "issued_Shares": sa.types.BIGINT,
                "net_asset": sa.types.FLOAT,
                "net_profit": sa.types.FLOAT,
                "earning_per_share": sa.types.FLOAT,
                "outstanding_shares": sa.types.BIGINT,
                "net_asset_per_share": sa.types.FLOAT,
                "ey_ratio": sa.types.FLOAT,
                "pe_ratio": sa.types.FLOAT,
                "pb_ratio": sa.types.FLOAT,
                "price_spread": sa.types.FLOAT
            },
            "clauses": [
                'ALTER TABLE `{0}` ADD INDEX (`code`);',
                'ALTER TABLE `{0}` ADD INDEX (`update_time`);'
                'ALTER TABLE `{0}` MODIFY COLUMN last_price FLOAT COMMENT  \'最新价格\';'
                'ALTER TABLE `{0}` MODIFY COLUMN open_price FLOAT COMMENT  \'今日开盘价\';'
                'ALTER TABLE `{0}` MODIFY COLUMN high_price FLOAT COMMENT  \'最高价格\';'
                'ALTER TABLE `{0}` MODIFY COLUMN low_price FLOAT COMMENT  \'最低价格\';'
                'ALTER TABLE `{0}` MODIFY COLUMN prev_close_price FLOAT COMMENT  \'昨收盘价格\';'
                'ALTER TABLE `{0}` MODIFY COLUMN volume BIGINT COMMENT  \'成交数量\';'
                'ALTER TABLE `{0}` MODIFY COLUMN turnover FLOAT COMMENT  \'成交金额\';'
                'ALTER TABLE `{0}` MODIFY COLUMN turnover_rate FLOAT COMMENT  \'换手率\';'
                'ALTER TABLE `{0}` MODIFY COLUMN suspension INT COMMENT  \'是否停牌(True表示停牌)\';'
                'ALTER TABLE `{0}` MODIFY COLUMN listing_date DATE COMMENT  \'上市日期 (yyyy-MM-dd)\';'
                'ALTER TABLE `{0}` MODIFY COLUMN circular_market_val FLOAT COMMENT  \'流通市值\';'
                'ALTER TABLE `{0}` MODIFY COLUMN total_market_val FLOAT COMMENT  \'总市值\';'
                'ALTER TABLE `{0}` MODIFY COLUMN wrt_valid INT COMMENT  \'是否是窝轮\';'
                'ALTER TABLE `{0}` MODIFY COLUMN wrt_conversion_ratio FLOAT COMMENT  \'换股比率\';'
                'ALTER TABLE `{0}` MODIFY COLUMN wrt_type FLOAT COMMENT  \'窝轮类型；1=认购证 2=认沽证 3=牛证 4=熊证 \';'
                'ALTER TABLE `{0}` MODIFY COLUMN wrt_strike_price FLOAT COMMENT  \'行使价格\';'
                'ALTER TABLE `{0}` MODIFY COLUMN wrt_maturity_date DATE COMMENT  \'格式化窝轮到期时间\';'
                'ALTER TABLE `{0}` MODIFY COLUMN wrt_end_trade DATE COMMENT  \'格式化窝轮最后交易时间\';'
                'ALTER TABLE `{0}` MODIFY COLUMN wrt_code FLOAT COMMENT  \'窝轮对应的正股\';'
                'ALTER TABLE `{0}` MODIFY COLUMN wrt_recovery_price FLOAT COMMENT  \'窝轮回收价\';'
                'ALTER TABLE `{0}` MODIFY COLUMN wrt_street_vol FLOAT COMMENT  \'窝轮街货量\';'
                'ALTER TABLE `{0}` MODIFY COLUMN wrt_issue_vol FLOAT COMMENT  \'窝轮发行量\';'
                'ALTER TABLE `{0}` MODIFY COLUMN wrt_street_ratio FLOAT COMMENT  \'窝轮街货占比\';'
                'ALTER TABLE `{0}` MODIFY COLUMN wrt_delta FLOAT COMMENT  \'窝轮对冲值\';'
                'ALTER TABLE `{0}` MODIFY COLUMN wrt_implied_volatility FLOAT COMMENT  \'窝轮引伸波幅\';'
                'ALTER TABLE `{0}` MODIFY COLUMN wrt_premium FLOAT COMMENT  \'窝轮溢价\';'
                'ALTER TABLE `{0}` MODIFY COLUMN lot_size BIGINT COMMENT  \'每手股数\';'
                'ALTER TABLE `{0}` MODIFY COLUMN issued_Shares BIGINT COMMENT  \'发行股本\';'
                'ALTER TABLE `{0}` MODIFY COLUMN net_asset FLOAT COMMENT  \'资产净值\';'
                'ALTER TABLE `{0}` MODIFY COLUMN net_profit FLOAT COMMENT  \'净利润\';'
                'ALTER TABLE `{0}` MODIFY COLUMN earning_per_share FLOAT COMMENT  \'每股盈利\';'
                'ALTER TABLE `{0}` MODIFY COLUMN outstanding_shares BIGINT COMMENT  \'流通股本\';'
                'ALTER TABLE `{0}` MODIFY COLUMN net_asset_per_share FLOAT COMMENT  \'每股净资产\';'
                'ALTER TABLE `{0}` MODIFY COLUMN ey_ratio FLOAT COMMENT  \'收益率\';'
                'ALTER TABLE `{0}` MODIFY COLUMN pe_ratio FLOAT COMMENT  \'市盈率\';'
                'ALTER TABLE `{0}` MODIFY COLUMN pb_ratio FLOAT COMMENT  \'市净率\';'
                'ALTER TABLE `{0}` MODIFY COLUMN price_spread FLOAT COMMENT  \'当前摆盘价差亦即摆盘数据的买档或卖档的相邻档位的报价差\';'
            ]
        },
        {
            "table": "ft_plate_list",
            "dtype": {
                "code": sa.types.NVARCHAR(20),
                "plate_name": sa.types.NVARCHAR(50),
                "plate_id": sa.types.NVARCHAR(20),
            },
            "clauses": [
                'ALTER TABLE `{0}` ADD INDEX (`code`);',
                'ALTER TABLE `{0}` ADD INDEX (`plate_name`);'
                'ALTER TABLE `{0}` MODIFY COLUMN code VARCHAR(20) COMMENT  \'股票代码\';'
                'ALTER TABLE `{0}` MODIFY COLUMN plate_name VARCHAR(50) COMMENT  \'板块名字\';'
                'ALTER TABLE `{0}` MODIFY COLUMN plate_id VARCHAR(20) COMMENT  \'板块id\';'
            ]
        },
        {
            "table": "ft_plate_stock",
            "dtype": {
                "code": sa.types.NVARCHAR(20),
                "lot_size": sa.types.BIGINT,
                "stock_name": sa.types.NVARCHAR(100),
                "stock_owner": sa.types.NVARCHAR(100),
                "stock_child_type": sa.types.NVARCHAR(20),
                "stock_type": sa.types.NVARCHAR(20),
                "list_time": sa.types.DATE,
                "stock_id": sa.types.BIGINT,
            },
            "clauses": [
                'ALTER TABLE `{0}` ADD INDEX (`code`);',
                'ALTER TABLE `{0}` ADD INDEX (`stock_name`);'
                'ALTER TABLE `{0}` ADD INDEX (`stock_child_type`);'
                'ALTER TABLE `{0}` ADD INDEX (`stock_type`);'
                'ALTER TABLE `{0}` MODIFY COLUMN code VARCHAR(20) COMMENT  \'股票代码\';'
                'ALTER TABLE `{0}` MODIFY COLUMN lot_size BIGINT COMMENT  \'每手股数\';'
                'ALTER TABLE `{0}` MODIFY COLUMN stock_name VARCHAR(100) COMMENT  \'股票名称\';'
                'ALTER TABLE `{0}` MODIFY COLUMN stock_owner VARCHAR(100) COMMENT  \'所属正股的代码\';'
                'ALTER TABLE `{0}` MODIFY COLUMN stock_child_type VARCHAR(100) COMMENT  \'股票子类型，参见WrtType\';'
                'ALTER TABLE `{0}` MODIFY COLUMN stock_type VARCHAR(20) COMMENT  \'股票类型，参见SecurityType\';'
                'ALTER TABLE `{0}` MODIFY COLUMN list_time DATE COMMENT  \'上市时间\';'
                'ALTER TABLE `{0}` MODIFY COLUMN stock_id BIGINT COMMENT  \'股票id\';'
            ]
        },
    ]

    try:
        logging.info("int_schema,  starting")

        for schema in schemaArr:
            df = pd.DataFrame(None,columns=schema['dtype'].keys())
            table = schema['table']
            logging.info('table:{0}'.format(table))
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


