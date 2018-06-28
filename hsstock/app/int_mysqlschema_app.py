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
            "table":"ts2_sina_dd",
            "dtype":{
                     'code': sa.types.NVARCHAR(10), 'name': sa.types.NVARCHAR(20),
                     'time': sa.types.TIME, 'price': sa.types.FLOAT, 'volume': sa.types.BIGINT,
                     'preprice': sa.types.FLOAT, 'type': sa.types.NVARCHAR(10), 'date': sa.types.DATE
            },
            "clauses":[
                'ALTER TABLE `{0}` COMMENT  \'大单数据表\';',
                'ALTER TABLE `{0}` MODIFY COLUMN name VARCHAR(255) COMMENT  \'代码名称\';',
                'ALTER TABLE `{0}` ADD INDEX (`code`);'
                ]
        },
        {
            "table": "fiv2_stat",
            "dtype": {
                "No": sa.types.BIGINT,
                "Ticker": sa.types.NVARCHAR(15),
                "Company": sa.types.NVARCHAR(50),
                "Sector": sa.types.NVARCHAR(50),
                "Industry": sa.types.NVARCHAR(50),
                "Country": sa.types.NVARCHAR(20),
                "Market Cap": sa.types.NVARCHAR(10),
                "P/E": sa.types.FLOAT,
                "Fwd P/E": sa.types.FLOAT,
                "PEG": sa.types.FLOAT,
                "P/S": sa.types.FLOAT,
                "P/B": sa.types.FLOAT,
                "P/C": sa.types.FLOAT,
                "P/FCF": sa.types.FLOAT,
                "Dividend": sa.types.NVARCHAR(10),
                "Payout Ratio": sa.types.NVARCHAR(10),
                "EPS": sa.types.FLOAT,
                "EPS this Y": sa.types.NVARCHAR(10),
                "EPS next Y": sa.types.NVARCHAR(10),
                "EPS past 5Y": sa.types.NVARCHAR(10),
                "EPS next 5Y": sa.types.NVARCHAR(10),
                "Sales past 5Y": sa.types.NVARCHAR(10),
                "EPS Q/Q": sa.types.NVARCHAR(10),
                "Sales Q/Q": sa.types.NVARCHAR(10),
                "Outstanding": sa.types.NVARCHAR(10),
                "Float": sa.types.FLOAT,
                "Insider Own": sa.types.NVARCHAR(10),
                "Insider Trans": sa.types.NVARCHAR(10),
                "Inst Own": sa.types.NVARCHAR(10),
                "Inst Trans": sa.types.NVARCHAR(10),
                "Float Short": sa.types.NVARCHAR(10),
                "Short Ratio": sa.types.FLOAT,
                "ROA": sa.types.NVARCHAR(10),
                "ROE": sa.types.NVARCHAR(10),
                "ROI": sa.types.NVARCHAR(10),
                "CurrR": sa.types.FLOAT,
                "Quick R": sa.types.FLOAT,
                "LTDebt/Eq": sa.types.FLOAT,
                "Debt/Eq": sa.types.FLOAT,
                "Gross M": sa.types.NVARCHAR(10),
                "Oper M": sa.types.NVARCHAR(10),
                "Profit M": sa.types.NVARCHAR(10),
                "Perf Week": sa.types.NVARCHAR(10),
                "Perf Month": sa.types.NVARCHAR(10),
                "Perf Quart": sa.types.NVARCHAR(10),
                "Perf Half": sa.types.NVARCHAR(10),
                "Perf Year": sa.types.NVARCHAR(10),
                "Perf YTD": sa.types.NVARCHAR(10),
                "Beta": sa.types.FLOAT,
                "ATR": sa.types.FLOAT,
                "Volatility W": sa.types.NVARCHAR(10),
                "Volatility M": sa.types.NVARCHAR(10),
                "SMA20": sa.types.NVARCHAR(10),
                "SMA50": sa.types.NVARCHAR(10),
                "SMA200": sa.types.NVARCHAR(10),
                "50D High": sa.types.NVARCHAR(10),
                "50D Low": sa.types.NVARCHAR(10),
                "52W High": sa.types.NVARCHAR(10),
                "52W Low": sa.types.NVARCHAR(10),
                "RSI": sa.types.FLOAT,
                "from Open": sa.types.NVARCHAR(10),
                "Gap": sa.types.NVARCHAR(10),
                "Recom": sa.types.FLOAT,
                "Avg Volume": sa.types.NVARCHAR(10),
                "Rel Volume": sa.types.FLOAT,
                "Price": sa.types.FLOAT,
                "Change": sa.types.NVARCHAR(1),
                "Volume": sa.types.FLOAT,
                "Earnings": sa.types.NVARCHAR(10),
                "Target Price": sa.types.FLOAT,
                "IPO Date": sa.types.DATE
            },
            "clauses": [
                'ALTER TABLE `{0}` ADD PRIMARY KEY (`Ticker`);'
            ]
        },
        {
            "table": "ts2_area_classified",
            "dtype": {
                'code': sa.types.NVARCHAR(10),
                'name': sa.types.NVARCHAR(20),
                'area': sa.types.NVARCHAR(10)
            },
            "clauses": [
                'ALTER TABLE `{0}` ADD PRIMARY KEY(`code`);'
            ]
        },
        {
            "table": "ts2_cashflow_data",
            "dtype": {
                'code': sa.types.NVARCHAR(10),
                'name': sa.types.NVARCHAR(20),
                "cf_sales": sa.types.FLOAT,
                "rateofreturn": sa.types.FLOAT,
                "cf_nm": sa.types.FLOAT,
                "cf_liabilities": sa.types.FLOAT,
                "cashflowratio": sa.types.FLOAT
            },
            "clauses": [
                'ALTER TABLE `{0}` ADD PRIMARY KEY (`code`);'
            ]
        },
        {
            "table": "ts2_concept_classified",
            "dtype": {
                'code': sa.types.NVARCHAR(10),
                'name': sa.types.NVARCHAR(20),
                "c_name": sa.types.NVARCHAR(20)
            },
            "clauses": [
                'ALTER TABLE `{0}` ADD PRIMARY KEY (`code`);'
            ]
        },
        {
            "table": "ts2_cpi",
            "dtype": {
                "month": sa.types.DATE,
                "cpi": sa.types.FLOAT
            },
            "clauses": [

            ]
        },
        {
            "table": "ts2_debtpaying_data",
            "dtype": {
                "code": sa.types.NVARCHAR(10),
                "name": sa.types.NVARCHAR(20),
                "currentratio": sa.types.FLOAT,
                "quickratio": sa.types.FLOAT,
                "cashratio": sa.types.FLOAT,
                "icratio": sa.types.FLOAT,
                "sheqratio": sa.types.FLOAT,
                "adratio": sa.types.FLOAT
            },
            "clauses": [
                'ALTER TABLE `{0}` ADD PRIMARY KEY (`code`);'
            ]
        },
        {
            "table": "ts2_deposit_rate",
            "dtype": {
                "date": sa.types.DATE,
                "deposit_type": sa.types.NVARCHAR(50),
                "rate": sa.types.FLOAT
            },
            "clauses": [
                'ALTER TABLE `{0}` ADD INDEX (`date`);'
            ]
        },
        {
            "table": "ts2_forecast_data",
            "dtype": {
                'code': sa.types.NVARCHAR(10), 'name': sa.types.NVARCHAR(20),
                "type": sa.types.NVARCHAR(20),
                "report_date": sa.types.DATE,
                "pre_eps": sa.types.FLOAT,
                "range": sa.types.BIGINT
            },
            "clauses": [
                'ALTER TABLE `{0}` ADD INDEX (`code`);'
            ]
        },
        {
            "table": "ts2_fund_holdings",
            "dtype": {
                'code': sa.types.NVARCHAR(10), 'name': sa.types.NVARCHAR(20),
                "date": sa.types.DATE,
                "nums": sa.types.INT,
                "nlast": sa.types.INT,
                "count": sa.types.FLOAT,
                "clast": sa.types.FLOAT,
                "amount": sa.types.FLOAT,
                "ratio": sa.types.FLOAT
            },
            "clauses": [
                'ALTER TABLE `{0}` ADD INDEX (`code`);'
            ]
        },
        {
            "table": "ts2_gdp_contrib",
            "dtype": {
                "year": sa.types.INT,
                "gdp_yoy": sa.types.FLOAT,
                "pi": sa.types.FLOAT,
                "si": sa.types.FLOAT,
                "industry": sa.types.FLOAT,
                "ti": sa.types.FLOAT
            },
            "clauses": [
                'ALTER TABLE `{0}` ADD INDEX (`year`);'
            ]
        },
        {
            "table": "ts2_gdp_for",
            "dtype": {
                "year": sa.types.INT,
                "end_for": sa.types.FLOAT,
                "for_rate": sa.types.FLOAT,
                "asset_for": sa.types.FLOAT,
                "asset_rate": sa.types.FLOAT,
                "goods_for": sa.types.FLOAT,
                "goods_rate": sa.types.FLOAT
            },
            "clauses": [
                'ALTER TABLE `{0}` ADD INDEX (`year`);'
            ]
        },
        {
            "table": "ts2_gdp_pull",
            "dtype": {
                "year": sa.types.INT,
                "gdp_yoy": sa.types.FLOAT,
                "pi": sa.types.FLOAT,
                "si": sa.types.FLOAT,
                "industry": sa.types.FLOAT,
                "ti": sa.types.FLOAT
            },
            "clauses": [
                'ALTER TABLE `{0}` ADD INDEX (`year`);'
            ]
        },
        {
            "table": "ts2_gdp_quarter",
            "dtype": {
                "quarter": sa.types.FLOAT,
                "gdp": sa.types.FLOAT,
                "gdp_yoy": sa.types.FLOAT,
                "pi": sa.types.FLOAT,
                "pi_yoy": sa.types.FLOAT,
                "si": sa.types.FLOAT,
                "si_yoy": sa.types.FLOAT,
                "ti": sa.types.FLOAT,
                "ti_yoy": sa.types.FLOAT
            },
            "clauses": [
                'ALTER TABLE `{0}` ADD INDEX (`quarter`);'
            ]
        },
        {
            "table": "ts2_gdp_year",
            "dtype": {
                "year": sa.types.INT,
                "gdp": sa.types.FLOAT,
                "pc_gdp": sa.types.FLOAT,
                "gnp": sa.types.FLOAT,
                "pi": sa.types.FLOAT,
                "si": sa.types.FLOAT,
                "industry": sa.types.FLOAT,
                "cons_industry": sa.types.FLOAT,
                "ti": sa.types.FLOAT,
                "trans_industry": sa.types.FLOAT,
                "lbdy": sa.types.FLOAT,
            },
            "clauses": [
                'ALTER TABLE `{0}` ADD INDEX (`year`);'
            ]
        },
        {
            "table": "ts2_gem_classified",
            "dtype": {
                "code": sa.types.NVARCHAR(10),
                "name": sa.types.NVARCHAR(20),
            },
            "clauses": [
                'ALTER TABLE `{0}` ADD INDEX (`code`);'
            ]
        },
        {
            "table": "ts2_growth_data",
            "dtype": {
                "code": sa.types.NVARCHAR(10),
                "name": sa.types.NVARCHAR(20),
                "mbrg": sa.types.FLOAT,
                "nprg": sa.types.FLOAT,
                "nav": sa.types.FLOAT,
                "targ": sa.types.FLOAT,
                "epsg": sa.types.FLOAT,
                "seg": sa.types.FLOAT
            },
            "clauses": [
                'ALTER TABLE `{0}` ADD INDEX (`code`);'
            ]
        },
        {
            "table": "ts2_h_data",
            "dtype": {
                "date": sa.types.DATE,
                "open": sa.types.FLOAT,
                "high": sa.types.FLOAT,
                "close": sa.types.FLOAT,
                "low": sa.types.FLOAT,
                "volume": sa.types.FLOAT,
                "amount": sa.types.FLOAT
            },
            "clauses": [
                'ALTER TABLE `{0}` ADD INDEX (`date`);'
            ]
        },
        {
            "table": "ts2_hist_data",
            "dtype": {
                "date": sa.types.DATE,
                "open": sa.types.FLOAT,
                "high": sa.types.FLOAT,
                "close": sa.types.FLOAT,
                "low": sa.types.FLOAT,
                "volume": sa.types.FLOAT,
                "price_change": sa.types.FLOAT,
                "p_change": sa.types.FLOAT,
                "ma5": sa.types.FLOAT,
                "ma10": sa.types.FLOAT,
                "ma20": sa.types.FLOAT,
                "v_ma5": sa.types.FLOAT,
                "v_ma10": sa.types.FLOAT,
                "v_ma20": sa.types.FLOAT
            },
            "clauses": [
                'ALTER TABLE `{0}` ADD INDEX (`date`);'
            ]
        },
        {
            "table": "ts2_hs300s",
            "dtype": {
                "date": sa.types.DATE,
                "code": sa.types.NVARCHAR(10),
                "name": sa.types.NVARCHAR(20),
                "weight": sa.types.FLOAT
            },
            "clauses": [
                'ALTER TABLE `{0}` ADD INDEX (`code`);'
            ]
        },
        {
            "table": "ts2_index",
            "dtype": {
                "code": sa.types.NVARCHAR(10),
                "name": sa.types.NVARCHAR(20),
                "change": sa.types.FLOAT,
                "open": sa.types.FLOAT,
                "preclose": sa.types.FLOAT,
                "close": sa.types.FLOAT,
                "high": sa.types.FLOAT,
                "low": sa.types.FLOAT,
                "volume": sa.types.BIGINT,
                "amount": sa.types.FLOAT,
                "date": sa.types.DATE
            },
            "clauses": [
                'ALTER TABLE `{0}` ADD INDEX (`code`);'
            ]
        },
        {
            "table": "ts2_industry_classified",
            "dtype": {
                "code": sa.types.NVARCHAR(10),
                "name": sa.types.NVARCHAR(20),
                "c_name": sa.types.NVARCHAR(20)
            },
            "clauses": [
                'ALTER TABLE `{0}` ADD INDEX (`code`);'
            ]
        },
        {
            "table": "ts2_latest_news",
            "dtype": {
                "classify": sa.types.NVARCHAR(20),
                "title": sa.types.NVARCHAR(100),
                "time": sa.types.DATETIME,
                "url": sa.types.NVARCHAR(500)
            },
            "clauses": [
                'ALTER TABLE `{0}` ADD INDEX (`title`);'
            ]
        },
        {
            "table": "ts2_loan_rate",
            "dtype": {
                "date": sa.types.DATE,
                "loan_type": sa.types.NVARCHAR(100),
                "rate": sa.types.FLOAT
            },
            "clauses": [
                'ALTER TABLE `{0}` ADD INDEX (`date`);'
            ]
        },
        {
            "table": "ts2_money_supply",
            "dtype": {

                "month": sa.types.FLOAT,
                "m2": sa.types.FLOAT,
                "m2_yoy": sa.types.FLOAT,
                "m1": sa.types.FLOAT,
                "m1_yoy": sa.types.FLOAT,
                "m0": sa.types.FLOAT,
                "m0_yoy": sa.types.FLOAT,
                "cd": sa.types.FLOAT,
                "cd_yoy": sa.types.FLOAT,
                "qm": sa.types.FLOAT,
                "qm_yoy": sa.types.FLOAT,
                "ftd": sa.types.FLOAT,
                "ftd_yoy": sa.types.FLOAT,
                "sd": sa.types.FLOAT,
                "sd_yoy": sa.types.FLOAT,
                "rests": sa.types.FLOAT,
                "rests_yoy": sa.types.FLOAT
            },
            "clauses": [
                'ALTER TABLE `{0}` ADD INDEX (`month`);'
            ]
        },
        {
            "table": "ts2_money_supply_bal",
            "dtype": {
                "year": sa.types.INT,
                "m2": sa.types.FLOAT,
                "m1": sa.types.FLOAT,
                "m0": sa.types.FLOAT,
                "cd": sa.types.FLOAT,
                "qm": sa.types.FLOAT,
                "ftd": sa.types.FLOAT,
                "sd": sa.types.FLOAT,
                "rests": sa.types.FLOAT
            },
            "clauses": [
                'ALTER TABLE `{0}` ADD INDEX (`year`);'
            ]
        },
        {
            "table": "ts2_new_stocks",
            "dtype": {

                "code": sa.types.NVARCHAR(10),
                "xcode": sa.types.NVARCHAR(10),
                "name": sa.types.NVARCHAR(10),
                "ipo_date": sa.types.DATE,
                "issue_date": sa.types.DATE,
                "amount": sa.types.BIGINT,
                "markets": sa.types.BIGINT,
                "price": sa.types.FLOAT,
                "pe": sa.types.FLOAT,
                "limit": sa.types.FLOAT,
                "funds": sa.types.FLOAT,
                "ballot": sa.types.FLOAT
            },
            "clauses": [
                'ALTER TABLE `{0}` ADD INDEX (`code`);'
            ]
        },
        {
            "table": "ts2_operation_data",
            "dtype": {
                "code": sa.types.NVARCHAR(10),
                "name": sa.types.NVARCHAR(20),
                "arturnover": sa.types.FLOAT,
                "arturndays": sa.types.FLOAT,
                "inventory_turnover": sa.types.FLOAT,
                "inventory_days": sa.types.FLOAT,
                "currentasset_turnover": sa.types.FLOAT,
                "currentasset_days": sa.types.FLOAT
            },
            "clauses": [
                'ALTER TABLE `{0}` ADD INDEX (`code`);'
            ]
        },
        {
            "table": "ts2_ppi",
            "dtype": {
                "month": sa.types.DATE,
                "ppiip": sa.types.FLOAT,
                "ppi": sa.types.FLOAT,
                "qm": sa.types.FLOAT,
                "rmi": sa.types.FLOAT,
                "pi": sa.types.FLOAT,
                "cg": sa.types.FLOAT,
                "food": sa.types.FLOAT,
                "clothing": sa.types.FLOAT,
                "roeu": sa.types.FLOAT,
                "dcg": sa.types.FLOAT
            },
            "clauses": [
                'ALTER TABLE `{0}` ADD INDEX (`month`);'
            ]
        },
        {
            "table": "ts2_profit_data",
            "dtype": {
                "code": sa.types.NVARCHAR(10),
                "name": sa.types.NVARCHAR(20),
                "year": sa.types.INT,
                "report_date": sa.types.DATE,
                "divi": sa.types.FLOAT,
                "shares": sa.types.FLOAT
            },
            "clauses": [
                'ALTER TABLE `{0}` ADD INDEX (`code`);'
            ]
        },
        {
            "table": "ts2_realtime_quotes",
            "dtype": {
                "code": sa.types.NVARCHAR(10),
                "name": sa.types.NVARCHAR(20),
                "open": sa.types.FLOAT,
                "pre_close": sa.types.FLOAT,
                "price": sa.types.FLOAT,
                "high": sa.types.FLOAT,
                "low": sa.types.FLOAT,
                "bid": sa.types.FLOAT,
                "ask": sa.types.FLOAT,
                "volume": sa.types.FLOAT,
                "amount": sa.types.FLOAT,
                "b1_v": sa.types.FLOAT,
                "b1_p": sa.types.FLOAT,
                "b2_v": sa.types.FLOAT,
                "b2_p": sa.types.FLOAT,
                "b3_v": sa.types.FLOAT,
                "b3_p": sa.types.FLOAT,
                "b4_v": sa.types.FLOAT,
                "b4_p": sa.types.FLOAT,
                "b5_v": sa.types.FLOAT,
                "b5_p": sa.types.FLOAT,
                "a1_v": sa.types.FLOAT,
                "a1_p": sa.types.FLOAT,
                "a2_v": sa.types.FLOAT,
                "a2_p": sa.types.FLOAT,
                "a3_v": sa.types.FLOAT,
                "a3_p": sa.types.FLOAT,
                "a4_v": sa.types.FLOAT,
                "a4_p": sa.types.FLOAT,
                "a5_v": sa.types.FLOAT,
                "a5_p": sa.types.FLOAT,
                "date": sa.types.DATE,
                "time": sa.types.TIME
            },
            "clauses": [
                'ALTER TABLE `{0}` ADD INDEX (`code`);'
            ]
        },
        {
            "table": "ts2_report_data",
            "dtype": {
                'code': sa.types.NVARCHAR(10), 'name': sa.types.NVARCHAR(20),
                "eps": sa.types.FLOAT,
                "eps_yoy": sa.types.FLOAT,
                "bvps": sa.types.FLOAT,
                "roe": sa.types.FLOAT,
                "epcf": sa.types.FLOAT,
                "net_profits": sa.types.FLOAT,
                "profits_yoy": sa.types.FLOAT,
                "distrib": sa.types.FLOAT,
                "report_date": sa.types.DATE
            },
            "clauses": [
                'ALTER TABLE `{0}` ADD INDEX (`code`);'
            ]
        },
        {
            "table": "ts2_rrr",
            "dtype": {
                "date": sa.types.DATE,
                "before": sa.types.FLOAT,
                "now": sa.types.FLOAT,
                "changed": sa.types.FLOAT
            },
            "clauses": [
                'ALTER TABLE `{0}` ADD INDEX (`date`);'
            ]
        },
        {
            "table": "ts2_sme_classified",
            "dtype": {
                "index": sa.types.BIGINT,
                "code": sa.types.NVARCHAR(10),
                "name": sa.types.NVARCHAR(20),
            },
            "clauses": [
                'ALTER TABLE `{0}` ADD INDEX (`code`);'
            ]
        },
        {
            "table": "ts2_st_classified",
            "dtype": {
                "code": sa.types.NVARCHAR(10),
                "name": sa.types.NVARCHAR(20),
            },
            "clauses": [
                'ALTER TABLE `{0}` ADD INDEX (`code`);'
            ]
        },
        {
            "table": "ts2_stock_basics",
            "dtype": {
                "code": sa.types.NVARCHAR(10),
                "name": sa.types.NVARCHAR(20),
                "industry": sa.types.NVARCHAR(20),
                "area": sa.types.NVARCHAR(20),
                "pe": sa.types.FLOAT,
                "outstanding": sa.types.FLOAT,
                "totals": sa.types.FLOAT,
                "totalAssets": sa.types.FLOAT,
                "liquidAssets": sa.types.FLOAT,
                "fixedAssets": sa.types.FLOAT,
                "reserved": sa.types.FLOAT,
                "reservedPerShare": sa.types.FLOAT,
                "esp": sa.types.FLOAT,
                "bvps": sa.types.FLOAT,
                "pb": sa.types.FLOAT,
                "timeToMarket": sa.types.NVARCHAR(15),
                "undp": sa.types.FLOAT,
                "perundp": sa.types.FLOAT,
                "rev": sa.types.FLOAT,
                "profit": sa.types.FLOAT,
                "gpr": sa.types.FLOAT,
                "npr": sa.types.FLOAT,
                "holders": sa.types.BIGINT
            },
            "clauses": [
                'ALTER TABLE `{0}` ADD INDEX (`code`);'
            ]
        },
        {
            "table": "ts2_sz50s",
            "dtype": {
                "code": sa.types.NVARCHAR(10),
                "name": sa.types.NVARCHAR(20),
            },
            "clauses": [
                'ALTER TABLE `{0}` ADD INDEX (`code`);'
            ]
        },
        {
            "table": "ts2_tick_data",
            "dtype": {
                "time": sa.types.TIME,
                "price": sa.types.FLOAT,
                "change": sa.types.FLOAT,
                "volume": sa.types.BIGINT,
                "amount": sa.types.BIGINT,
                "type": sa.types.NVARCHAR(10),
                "date": sa.types.DATE
            },
            "clauses": [
                'ALTER TABLE `{0}` ADD INDEX (`date`);'
            ]
        },
        {
            "table": "ts2_today_all",
            "dtype": {
                "code": sa.types.NVARCHAR(10),
                "name": sa.types.NVARCHAR(20),
                "changepercent": sa.types.FLOAT,
                "trade": sa.types.FLOAT,
                "open": sa.types.FLOAT,
                "high": sa.types.FLOAT,
                "low": sa.types.FLOAT,
                "settlement": sa.types.FLOAT,
                "volume": sa.types.FLOAT,
                "turnoverratio": sa.types.FLOAT,
                "amount": sa.types.FLOAT,
                "per": sa.types.FLOAT,
                "pb": sa.types.FLOAT,
                "mktcap": sa.types.FLOAT,
                "nmc": sa.types.FLOAT,
                "date": sa.types.DATE
            },
            "clauses": [
                'ALTER TABLE `{0}` ADD INDEX (`code`);'
            ]
        },
        {
            "table": "ts2_today_ticks",
            "dtype": {
                "time": sa.types.TIME,
                "price": sa.types.FLOAT,
                "pchange": sa.types.NVARCHAR(10),
                "change": sa.types.FLOAT,
                "volume": sa.types.BIGINT,
                "amount": sa.types.BIGINT,
                "type": sa.types.NVARCHAR(10),
                "date": sa.types.DATE
            },
            "clauses": [
                'ALTER TABLE `{0}` ADD INDEX (`date`);'
            ]
        },
        {
            "table": "ts2_xsg_data",
            "dtype": {
                "code": sa.types.NVARCHAR(10),
                "name": sa.types.NVARCHAR(20),
                "date": sa.types.DATE,
                "count": sa.types.FLOAT,
                "ratio": sa.types.FLOAT
            },
            "clauses": [
                'ALTER TABLE `{0}` ADD INDEX (`code`);'
            ]
        },
        {
            "table": "ts2_zz500s",
            "dtype": {
                "code": sa.types.NVARCHAR(10),
                "name": sa.types.NVARCHAR(20),
                "date": sa.types.DATE,
                "weight": sa.types.FLOAT
            },
            "clauses": [
                'ALTER TABLE `{0}` ADD INDEX (`code`);'
            ]
        }
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


