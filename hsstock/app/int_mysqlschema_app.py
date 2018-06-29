# -*- coding: UTF-8 -*-
import logging
import sqlalchemy as sa
import pandas as pd

from hsstock.service.store_service import StoreService
from hsstock.utils.app_logging import setup_logging

def main():

    storeservice = StoreService()

    schemaArr = [
        # {
        #     "table":"ts2_sina_dd",
        #     "dtype":{
        #              'code': sa.types.NVARCHAR(10), 'name': sa.types.NVARCHAR(20),
        #              'time': sa.types.TIME, 'price': sa.types.FLOAT, 'volume': sa.types.BIGINT,
        #              'preprice': sa.types.FLOAT, 'type': sa.types.NVARCHAR(10), 'date': sa.types.DATE
        #     },
        #     "clauses":[
        #         'ALTER TABLE `{0}` ADD INDEX (`code`);'
        #         'ALTER TABLE `{0}` COMMENT  \'大单数据表\';',
        #         'ALTER TABLE `{0}` MODIFY COLUMN name VARCHAR(255) COMMENT  \'代码名称\';'
        #         ]
        # },
        # {
        #     "table": "fiv2_stat",
        #     "dtype": {
        #         "No": sa.types.BIGINT,
        #         "Ticker": sa.types.NVARCHAR(15),
        #         "Company": sa.types.NVARCHAR(50),
        #         "Sector": sa.types.NVARCHAR(50),
        #         "Industry": sa.types.NVARCHAR(50),
        #         "Country": sa.types.NVARCHAR(20),
        #         "Market Cap": sa.types.NVARCHAR(10),
        #         "P/E": sa.types.FLOAT,
        #         "Fwd P/E": sa.types.FLOAT,
        #         "PEG": sa.types.FLOAT,
        #         "P/S": sa.types.FLOAT,
        #         "P/B": sa.types.FLOAT,
        #         "P/C": sa.types.FLOAT,
        #         "P/FCF": sa.types.FLOAT,
        #         "Dividend": sa.types.NVARCHAR(10),
        #         "Payout Ratio": sa.types.NVARCHAR(10),
        #         "EPS": sa.types.FLOAT,
        #         "EPS this Y": sa.types.NVARCHAR(10),
        #         "EPS next Y": sa.types.NVARCHAR(10),
        #         "EPS past 5Y": sa.types.NVARCHAR(10),
        #         "EPS next 5Y": sa.types.NVARCHAR(10),
        #         "Sales past 5Y": sa.types.NVARCHAR(10),
        #         "EPS Q/Q": sa.types.NVARCHAR(10),
        #         "Sales Q/Q": sa.types.NVARCHAR(10),
        #         "Outstanding": sa.types.NVARCHAR(10),
        #         "Float": sa.types.FLOAT,
        #         "Insider Own": sa.types.NVARCHAR(10),
        #         "Insider Trans": sa.types.NVARCHAR(10),
        #         "Inst Own": sa.types.NVARCHAR(10),
        #         "Inst Trans": sa.types.NVARCHAR(10),
        #         "Float Short": sa.types.NVARCHAR(10),
        #         "Short Ratio": sa.types.FLOAT,
        #         "ROA": sa.types.NVARCHAR(10),
        #         "ROE": sa.types.NVARCHAR(10),
        #         "ROI": sa.types.NVARCHAR(10),
        #         "CurrR": sa.types.FLOAT,
        #         "Quick R": sa.types.FLOAT,
        #         "LTDebt/Eq": sa.types.FLOAT,
        #         "Debt/Eq": sa.types.FLOAT,
        #         "Gross M": sa.types.NVARCHAR(10),
        #         "Oper M": sa.types.NVARCHAR(10),
        #         "Profit M": sa.types.NVARCHAR(10),
        #         "Perf Week": sa.types.NVARCHAR(10),
        #         "Perf Month": sa.types.NVARCHAR(10),
        #         "Perf Quart": sa.types.NVARCHAR(10),
        #         "Perf Half": sa.types.NVARCHAR(10),
        #         "Perf Year": sa.types.NVARCHAR(10),
        #         "Perf YTD": sa.types.NVARCHAR(10),
        #         "Beta": sa.types.FLOAT,
        #         "ATR": sa.types.FLOAT,
        #         "Volatility W": sa.types.NVARCHAR(10),
        #         "Volatility M": sa.types.NVARCHAR(10),
        #         "SMA20": sa.types.NVARCHAR(10),
        #         "SMA50": sa.types.NVARCHAR(10),
        #         "SMA200": sa.types.NVARCHAR(10),
        #         "50D High": sa.types.NVARCHAR(10),
        #         "50D Low": sa.types.NVARCHAR(10),
        #         "52W High": sa.types.NVARCHAR(10),
        #         "52W Low": sa.types.NVARCHAR(10),
        #         "RSI": sa.types.FLOAT,
        #         "from Open": sa.types.NVARCHAR(10),
        #         "Gap": sa.types.NVARCHAR(10),
        #         "Recom": sa.types.FLOAT,
        #         "Avg Volume": sa.types.NVARCHAR(10),
        #         "Rel Volume": sa.types.FLOAT,
        #         "Price": sa.types.FLOAT,
        #         "Change": sa.types.NVARCHAR(1),
        #         "Volume": sa.types.FLOAT,
        #         "Earnings": sa.types.NVARCHAR(10),
        #         "Target Price": sa.types.FLOAT,
        #         "IPO Date": sa.types.DATE
        #     },
        #     "clauses": [
        #         'ALTER TABLE `{0}` ADD PRIMARY KEY (`Ticker`);'
        #     ]
        # },
        # {
        #     "table": "ts2_area_classified",
        #     "dtype": {
        #         'code': sa.types.NVARCHAR(10),
        #         'name': sa.types.NVARCHAR(20),
        #         'area': sa.types.NVARCHAR(10)
        #     },
        #     "clauses": [
        #         'ALTER TABLE `{0}` ADD PRIMARY KEY(`code`);'
        #     ]
        # },
        # {
        #     "table": "ts2_cashflow_data",
        #     "dtype": {
        #         'code': sa.types.NVARCHAR(10),
        #         'name': sa.types.NVARCHAR(20),
        #         'year': sa.types.INT,
        #         'quarter': sa.types.INT,
        #         "cf_sales": sa.types.FLOAT,
        #         "rateofreturn": sa.types.FLOAT,
        #         "cf_nm": sa.types.FLOAT,
        #         "cf_liabilities": sa.types.FLOAT,
        #         "cashflowratio": sa.types.FLOAT
        #     },
        #     "clauses": [
        #         'ALTER TABLE `{0}` ADD INDEX (`code`);',
        #         'ALTER TABLE `{0}` MODIFY COLUMN cf_sales FLOAT COMMENT  \'经营现金净流量对销售收入比率\';',
        #         'ALTER TABLE `{0}` MODIFY COLUMN rateofreturn FLOAT COMMENT  \'资产的经营现金流量回报率\';',
        #         'ALTER TABLE `{0}` MODIFY COLUMN cf_nm FLOAT COMMENT  \'经营现金净流量与净利润的比率\';',
        #         'ALTER TABLE `{0}` MODIFY COLUMN cf_liabilities FLOAT COMMENT  \'经营现金净流量对负债比率\';',
        #         'ALTER TABLE `{0}` MODIFY COLUMN cashflowratio FLOAT COMMENT  \'现金流量比率\';'
        #     ]
        # },
        # {
        #     "table": "ts2_concept_classified",
        #     "dtype": {
        #         'code': sa.types.NVARCHAR(10),
        #         'name': sa.types.NVARCHAR(20),
        #         "c_name": sa.types.NVARCHAR(20)
        #     },
        #     "clauses": [
        #         # Code有重复
        #         'ALTER TABLE `{0}` ADD KEY (`code`);'
        #     ]
        # },
        # {
        #     "table": "ts2_cpi",
        #     "dtype": {
        #         "month": sa.types.DATE,
        #         "cpi": sa.types.FLOAT
        #     },
        #     "clauses": [
        #         'ALTER TABLE `{0}` MODIFY COLUMN month INT COMMENT  \'年.月\';'
        #         'ALTER TABLE `{0}` MODIFY COLUMN cpi FLOAT COMMENT  \'价格指数\';'
        #     ]
        # },
        # {
        #     "table": "ts2_debtpaying_data",
        #     "dtype": {
        #         "code": sa.types.NVARCHAR(10),
        #         "name": sa.types.NVARCHAR(20),
        #         'year': sa.types.INT,
        #         'quarter': sa.types.INT,
        #         "currentratio": sa.types.NVARCHAR(20),
        #         "quickratio": sa.types.NVARCHAR(20),
        #         "cashratio": sa.types.NVARCHAR(20),
        #         "icratio": sa.types.NVARCHAR(20),
        #         "sheqratio": sa.types.NVARCHAR(20),
        #         "adratio": sa.types.NVARCHAR(20)
        #     },
        #     "clauses": [
        #         'ALTER TABLE `{0}` ADD INDEX (`code`);',
        #         'ALTER TABLE `{0}` MODIFY COLUMN currentratio VARCHAR(20) COMMENT  \'流动比率\';',
        #         'ALTER TABLE `{0}` MODIFY COLUMN quickratio VARCHAR(20) COMMENT  \'速动比率\';',
        #         'ALTER TABLE `{0}` MODIFY COLUMN cashratio VARCHAR(20) COMMENT  \'速动比率\';',
        #         'ALTER TABLE `{0}` MODIFY COLUMN icratio VARCHAR(20) COMMENT  \'利息支付倍数\';',
        #         'ALTER TABLE `{0}` MODIFY COLUMN sheqratio VARCHAR(20) COMMENT  \'股东权益比率\';',
        #         'ALTER TABLE `{0}` MODIFY COLUMN adratio VARCHAR(20) COMMENT  \'股东权益增长率\';'
        #     ]
        # },
        # {
        #     "table": "ts2_deposit_rate",
        #     "dtype": {
        #         "date": sa.types.DATE,
        #         "deposit_type": sa.types.NVARCHAR(50),
        #         "rate": sa.types.NVARCHAR(20)
        #     },
        #     "clauses": [
        #         'ALTER TABLE `{0}` ADD INDEX (`date`);',
        #         'ALTER TABLE `{0}` MODIFY COLUMN deposit_type VARCHAR(50) COMMENT  \'存款种类\';',
        #         'ALTER TABLE `{0}` MODIFY COLUMN rate  VARCHAR(50) COMMENT \'利率(百分比)\';'
        #     ]
        # },
        # {
        #     "table": "ts2_forecast_data",
        #     "dtype": {
        #         'code': sa.types.NVARCHAR(10), 'name': sa.types.NVARCHAR(20),
        #         'year': sa.types.INT,
        #         'quarter': sa.types.INT,
        #         "type": sa.types.NVARCHAR(20),
        #         "report_date": sa.types.DATE,
        #         "pre_eps": sa.types.FLOAT,
        #         "range": sa.types.NVARCHAR(20)
        #     },
        #     "clauses": [
        #         'ALTER TABLE `{0}` ADD INDEX (`code`);',
        #         'ALTER TABLE `{0}` MODIFY COLUMN pre_eps FLOAT COMMENT  \'上年同期每股收益\';',
        #         'ALTER TABLE `{0}` MODIFY COLUMN `range` VARCHAR(20) COMMENT  \'业绩变动范围\';'
        #     ]
        # },
        # {
        #     "table": "ts2_fund_holdings",
        #     "dtype": {
        #         'code': sa.types.NVARCHAR(10), 'name': sa.types.NVARCHAR(20),
        #         'year': sa.types.INT,
        #         'quarter': sa.types.INT,
        #         "date": sa.types.DATE,
        #         "nums": sa.types.INT,
        #         "nlast": sa.types.INT,
        #         "count": sa.types.FLOAT,
        #         "clast": sa.types.FLOAT,
        #         "amount": sa.types.FLOAT,
        #         "ratio": sa.types.FLOAT
        #     },
        #     "clauses": [
        #         'ALTER TABLE `{0}` ADD INDEX (`code`);',
        #         'ALTER TABLE `{0}` MODIFY COLUMN nums BIGINT COMMENT  \'基金家数\';',
        #         'ALTER TABLE `{0}` MODIFY COLUMN nlast BIGINT COMMENT  \'与上期相比（增加或减少了）\';',
        #         'ALTER TABLE `{0}` MODIFY COLUMN count FLOAT COMMENT  \'基金持股数（万股）\';',
        #         'ALTER TABLE `{0}` MODIFY COLUMN clast FLOAT COMMENT  \'与上期相比\';',
        #         'ALTER TABLE `{0}` MODIFY COLUMN amount FLOAT COMMENT  \'基金持股市值\';',
        #         'ALTER TABLE `{0}` MODIFY COLUMN ratio FLOAT COMMENT  \'占流通盘比率\';'
        #     ]
        # },
        # {
        #     "table": "ts2_gdp_contrib",
        #     "dtype": {
        #         "year": sa.types.INT,
        #         "gdp_yoy": sa.types.FLOAT,
        #         "pi": sa.types.FLOAT,
        #         "si": sa.types.FLOAT,
        #         "industry": sa.types.FLOAT,
        #         "ti": sa.types.FLOAT
        #     },
        #     "clauses": [
        #         'ALTER TABLE `{0}` ADD INDEX (`year`);'
        #         'ALTER TABLE `{0}` MODIFY COLUMN gdp_yoy FLOAT COMMENT  \'国内生产总值\';'
        #         'ALTER TABLE `{0}` MODIFY COLUMN pi FLOAT COMMENT  \'第一产业献率\';'
        #         'ALTER TABLE `{0}` MODIFY COLUMN si FLOAT COMMENT  \'第二产业献率\';'
        #         'ALTER TABLE `{0}` MODIFY COLUMN industry FLOAT COMMENT  \'其中工业献率\';'
        #         'ALTER TABLE `{0}` MODIFY COLUMN ti FLOAT COMMENT  \'第三产业献率\';'
        #     ]
        # },
        # {
        #     "table": "ts2_gdp_for",
        #     "dtype": {
        #         "year": sa.types.INT,
        #         "end_for": sa.types.FLOAT,
        #         "for_rate": sa.types.FLOAT,
        #         "asset_for": sa.types.FLOAT,
        #         "asset_rate": sa.types.FLOAT,
        #         "goods_for": sa.types.FLOAT,
        #         "goods_rate": sa.types.FLOAT
        #     },
        #     "clauses": [
        #         'ALTER TABLE `{0}` ADD INDEX (`year`);'
        #         'ALTER TABLE `{0}` MODIFY COLUMN end_for FLOAT COMMENT  \'最终消费支出贡献率(百分比)\';'
        #         'ALTER TABLE `{0}` MODIFY COLUMN for_rate FLOAT COMMENT  \'资本形成总额贡献率(百分比)\';'
        #         'ALTER TABLE `{0}` MODIFY COLUMN asset_for FLOAT COMMENT  \'资本形成总额贡献率(百分比)\';'
        #         'ALTER TABLE `{0}` MODIFY COLUMN asset_rate FLOAT COMMENT  \'资本形成总额拉动(百分点)\';'
        #         'ALTER TABLE `{0}` MODIFY COLUMN goods_for FLOAT COMMENT  \'货物和服务净出口贡献率(百分比)\';'
        #         'ALTER TABLE `{0}` MODIFY COLUMN goods_rate FLOAT COMMENT  \'货物和服务净出口拉动(百分点)\';'
        #     ]
        # },
        # {
        #     "table": "ts2_gdp_pull",
        #     "dtype": {
        #         "year": sa.types.INT,
        #         "gdp_yoy": sa.types.FLOAT,
        #         "pi": sa.types.FLOAT,
        #         "si": sa.types.FLOAT,
        #         "industry": sa.types.FLOAT,
        #         "ti": sa.types.FLOAT
        #     },
        #     "clauses": [
        #         'ALTER TABLE `{0}` ADD INDEX (`year`);'
        #         'ALTER TABLE `{0}` MODIFY COLUMN gdp_yoy FLOAT COMMENT  \'国内生产总值同比增长(百分比)\';'
        #         'ALTER TABLE `{0}` MODIFY COLUMN pi FLOAT COMMENT  \'第一产业拉动率(百分比)\';'
        #         'ALTER TABLE `{0}` MODIFY COLUMN si FLOAT COMMENT  \'第二产业拉动率(百分比)\';'
        #         'ALTER TABLE `{0}` MODIFY COLUMN industry FLOAT COMMENT  \'其中工业拉动(百分比)\';'
        #         'ALTER TABLE `{0}` MODIFY COLUMN ti FLOAT COMMENT  \'第三产业拉动率(百分比)\';'
        #     ]
        # },
        # {
        #     "table": "ts2_gdp_quarter",
        #     "dtype": {
        #         "quarter": sa.types.FLOAT,
        #         "gdp": sa.types.FLOAT,
        #         "gdp_yoy": sa.types.FLOAT,
        #         "pi": sa.types.FLOAT,
        #         "pi_yoy": sa.types.FLOAT,
        #         "si": sa.types.FLOAT,
        #         "si_yoy": sa.types.FLOAT,
        #         "ti": sa.types.FLOAT,
        #         "ti_yoy": sa.types.FLOAT
        #     },
        #     "clauses": [
        #         'ALTER TABLE `{0}` ADD INDEX (`quarter`);'
        #         'ALTER TABLE `{0}` MODIFY COLUMN gdp FLOAT COMMENT  \'国内生产总值(亿元)\';'
        #         'ALTER TABLE `{0}` MODIFY COLUMN gdp_yoy FLOAT COMMENT  \'国内生产总值同比增长(百分比)\';'
        #         'ALTER TABLE `{0}` MODIFY COLUMN pi FLOAT COMMENT  \'第一产业增加值(亿元)\';'
        #         'ALTER TABLE `{0}` MODIFY COLUMN pi_yoy FLOAT COMMENT  \'第一产业增加值同比增长(百分比)\';'
        #         'ALTER TABLE `{0}` MODIFY COLUMN si FLOAT COMMENT  \'第二产业增加值(亿元)\';'
        #         'ALTER TABLE `{0}` MODIFY COLUMN si_yoy FLOAT COMMENT  \'第二产业增加值同比增长(百分比)\';'
        #         'ALTER TABLE `{0}` MODIFY COLUMN ti FLOAT COMMENT  \'第三产业增加值(亿元)\';'
        #         'ALTER TABLE `{0}` MODIFY COLUMN ti_yoy FLOAT COMMENT  \'第三产业增加值同比增长(百分比)\';'
        #     ]
        # },
        # {
        #     "table": "ts2_gdp_year",
        #     "dtype": {
        #         "year": sa.types.INT,
        #         "gdp": sa.types.FLOAT,
        #         "pc_gdp": sa.types.FLOAT,
        #         "gnp": sa.types.FLOAT,
        #         "pi": sa.types.FLOAT,
        #         "si": sa.types.FLOAT,
        #         "industry": sa.types.FLOAT,
        #         "cons_industry": sa.types.FLOAT,
        #         "ti": sa.types.FLOAT,
        #         "trans_industry": sa.types.FLOAT,
        #         "lbdy": sa.types.FLOAT,
        #     },
        #     "clauses": [
        #         'ALTER TABLE `{0}` ADD INDEX (`year`);'
        #         'ALTER TABLE `{0}` MODIFY COLUMN gdp FLOAT COMMENT  \'国内生产总值(亿元)\';'
        #         'ALTER TABLE `{0}` MODIFY COLUMN pc_gdp FLOAT COMMENT  \'人均国内生产总值(元)\';'
        #         'ALTER TABLE `{0}` MODIFY COLUMN gnp FLOAT COMMENT  \'国民生产总值(亿元)\';'
        #         'ALTER TABLE `{0}` MODIFY COLUMN pi FLOAT COMMENT  \'第一产业(亿元)\';'
        #         'ALTER TABLE `{0}` MODIFY COLUMN si FLOAT COMMENT  \'第二产业(亿元)\';'
        #         'ALTER TABLE `{0}` MODIFY COLUMN industry FLOAT COMMENT  \'工业(亿元)\';'
        #         'ALTER TABLE `{0}` MODIFY COLUMN cons_industry FLOAT COMMENT  \'建筑业(亿元)\';'
        #         'ALTER TABLE `{0}` MODIFY COLUMN ti FLOAT COMMENT  \'第三产业(亿元)\';'
        #         'ALTER TABLE `{0}` MODIFY COLUMN trans_industry FLOAT COMMENT  \'交通运输仓储邮电通信业(亿元)\';'
        #         'ALTER TABLE `{0}` MODIFY COLUMN lbdy FLOAT COMMENT  \'批发零售贸易及餐饮业(亿元)\';'
        #     ]
        # },
        # {
        #     "table": "ts2_gem_classified",
        #     "dtype": {
        #         "code": sa.types.NVARCHAR(10),
        #         "name": sa.types.NVARCHAR(20),
        #     },
        #     "clauses": [
        #         'ALTER TABLE `{0}` ADD INDEX (`code`);'
        #     ]
        # },
        # {
        #     "table": "ts2_growth_data",
        #     "dtype": {
        #         "code": sa.types.NVARCHAR(10),
        #         "name": sa.types.NVARCHAR(20),
        #         'year': sa.types.INT,
        #         'quarter': sa.types.INT,
        #         "mbrg": sa.types.FLOAT,
        #         "nprg": sa.types.FLOAT,
        #         "nav": sa.types.FLOAT,
        #         "targ": sa.types.FLOAT,
        #         "epsg": sa.types.FLOAT,
        #         "seg": sa.types.FLOAT
        #     },
        #     "clauses": [
        #         'ALTER TABLE `{0}` ADD INDEX (`code`);',
        #         'ALTER TABLE `{0}` MODIFY COLUMN mbrg FLOAT COMMENT  \'主营业务收入增长率(百分比)\';'
        #         'ALTER TABLE `{0}` MODIFY COLUMN nprg FLOAT COMMENT  \'净利润增长率(百分比)\';'
        #         'ALTER TABLE `{0}` MODIFY COLUMN nav FLOAT COMMENT  \'净资产增长率\';'
        #         'ALTER TABLE `{0}` MODIFY COLUMN targ FLOAT COMMENT  \'总资产增长率\';'
        #         'ALTER TABLE `{0}` MODIFY COLUMN epsg FLOAT COMMENT  \'每股收益增长率\';'
        #         'ALTER TABLE `{0}` MODIFY COLUMN seg FLOAT COMMENT  \'股东权益增长率\';'
        #     ]
        # },
        # {
        #     "table": "ts2_h_data",
        #     "dtype": {
        #         "code": sa.types.NVARCHAR(20),
        #         "date": sa.types.DATE,
        #         "open": sa.types.FLOAT,
        #         "high": sa.types.FLOAT,
        #         "close": sa.types.FLOAT,
        #         "low": sa.types.FLOAT,
        #         "volume": sa.types.FLOAT,
        #         "amount": sa.types.FLOAT
        #     },
        #     "clauses": [
        #         'ALTER TABLE `{0}` ADD INDEX (`code`);',
        #         'ALTER TABLE `{0}` ADD INDEX (`date`);'
        #     ]
        # },
        # {
        #     "table": "ts2_hist_data",
        #     "dtype": {
        #         "date": sa.types.DATE,
        #         "open": sa.types.FLOAT,
        #         "code": sa.types.NVARCHAR(20),
        #         "high": sa.types.FLOAT,
        #         "close": sa.types.FLOAT,
        #         "low": sa.types.FLOAT,
        #         "volume": sa.types.FLOAT,
        #         "price_change": sa.types.FLOAT,
        #         "p_change": sa.types.FLOAT,
        #         "ma5": sa.types.FLOAT,
        #         "ma10": sa.types.FLOAT,
        #         "ma20": sa.types.FLOAT,
        #         "v_ma5": sa.types.FLOAT,
        #         "v_ma10": sa.types.FLOAT,
        #         "v_ma20": sa.types.FLOAT,
        #         "turnover": sa.types.FLOAT
        #     },
        #     "clauses": [
        #         'ALTER TABLE `{0}` ADD INDEX (`date`);',
        #         'ALTER TABLE `{0}` ADD INDEX (`code`);',
        #         'ALTER TABLE `{0}` MODIFY COLUMN p_change FLOAT COMMENT  \'涨跌变动\';',
        #         'ALTER TABLE `{0}` MODIFY COLUMN turnover FLOAT COMMENT  \'换手率\';'
        #     ]
        # },
        # {
        #     "table": "ts2_hs300s",
        #     "dtype": {
        #         "date": sa.types.DATE,
        #         "code": sa.types.NVARCHAR(10),
        #         "name": sa.types.NVARCHAR(20),
        #         "weight": sa.types.FLOAT
        #     },
        #     "clauses": [
        #         'ALTER TABLE `{0}` ADD INDEX (`code`);'
        #     ]
        # },
        # {
        #     "table": "ts2_index",
        #     "dtype": {
        #         "code": sa.types.NVARCHAR(10),
        #         "name": sa.types.NVARCHAR(20),
        #         "change": sa.types.FLOAT,
        #         "open": sa.types.FLOAT,
        #         "preclose": sa.types.FLOAT,
        #         "close": sa.types.FLOAT,
        #         "high": sa.types.FLOAT,
        #         "low": sa.types.FLOAT,
        #         "volume": sa.types.BIGINT,
        #         "amount": sa.types.FLOAT,
        #         "date": sa.types.DATE
        #     },
        #     "clauses": [
        #         'ALTER TABLE `{0}` ADD INDEX (`code`);'
        #     ]
        # },
        # {
        #     "table": "ts2_industry_classified",
        #     "dtype": {
        #         "code": sa.types.NVARCHAR(10),
        #         "name": sa.types.NVARCHAR(20),
        #         "c_name": sa.types.NVARCHAR(20)
        #     },
        #     "clauses": [
        #         'ALTER TABLE `{0}` ADD INDEX (`code`);'
        #     ]
        # },
        # {
        #     "table": "ts2_latest_news",
        #     "dtype": {
        #         "classify": sa.types.NVARCHAR(20),
        #         "title": sa.types.NVARCHAR(100),
        #         "time": sa.types.NVARCHAR(20),
        #         "url": sa.types.NVARCHAR(500)
        #     },
        #     "clauses": [
        #         'ALTER TABLE `{0}` ADD INDEX (`title`);'
        #     ]
        # },
        # {
        #     "table": "ts2_loan_rate",
        #     "dtype": {
        #         "date": sa.types.DATE,
        #         "loan_type": sa.types.NVARCHAR(100),
        #         "rate": sa.types.NVARCHAR(50)
        #     },
        #     "clauses": [
        #         'ALTER TABLE `{0}` ADD INDEX (`date`);',
        #         'ALTER TABLE `{0}` MODIFY COLUMN loan_type VARCHAR (100) COMMENT  \'存款种类\';',
        #         'ALTER TABLE `{0}` MODIFY COLUMN rate VARCHAR(50) COMMENT  \'利率(百分比)\';'
        #     ]
        # },
        # {
        #     "table": "ts2_money_supply",
        #     "dtype": {
        #
        #         "month": sa.types.VARCHAR(20),
        #         "m2": sa.types.VARCHAR(20),
        #         "m2_yoy": sa.types.VARCHAR(20),
        #         "m1": sa.types.VARCHAR(20),
        #         "m1_yoy": sa.types.VARCHAR(20),
        #         "m0": sa.types.VARCHAR(20),
        #         "m0_yoy": sa.types.VARCHAR(20),
        #         "cd": sa.types.VARCHAR(20),
        #         "cd_yoy": sa.types.VARCHAR(20),
        #         "qm": sa.types.VARCHAR(20),
        #         "qm_yoy": sa.types.VARCHAR(20),
        #         "ftd": sa.types.VARCHAR(20),
        #         "ftd_yoy": sa.types.VARCHAR(20),
        #         "sd": sa.types.VARCHAR(20),
        #         "sd_yoy": sa.types.VARCHAR(20),
        #         "rests": sa.types.VARCHAR(20),
        #         "rests_yoy": sa.types.VARCHAR(20)
        #     },
        #     "clauses": [
        #         'ALTER TABLE `{0}` ADD INDEX (`month`);',
        #         'ALTER TABLE `{0}` MODIFY COLUMN m2 VARCHAR(20)COMMENT  \'货币和准货币（广义货币M2）(亿元)\';',
        #         'ALTER TABLE `{0}` MODIFY COLUMN m2_yoy VARCHAR(20) COMMENT  \'货币和准货币（广义货币M2）同比增长(百分比)\';',
        #         'ALTER TABLE `{0}` MODIFY COLUMN m1 VARCHAR(20) COMMENT  \'货币(狭义货币M1)(亿元)\';',
        #         'ALTER TABLE `{0}` MODIFY COLUMN m1_yoy VARCHAR(20) COMMENT  \'货币(狭义货币M1)同比增长(百分比)\';'
        #         'ALTER TABLE `{0}` MODIFY COLUMN m0 VARCHAR(20) COMMENT  \'流通中现金(M0)(亿元)\';'
        #         'ALTER TABLE `{0}` MODIFY COLUMN m0_yoy VARCHAR(20) COMMENT  \'流通中现金(M0)同比增长(百分比)\';'
        #         'ALTER TABLE `{0}` MODIFY COLUMN cd VARCHAR(20) COMMENT  \'活期存款(亿元)\';'
        #         'ALTER TABLE `{0}` MODIFY COLUMN cd_yoy VARCHAR(20) COMMENT  \'活期存款同比增长(百分比)\';'
        #         'ALTER TABLE `{0}` MODIFY COLUMN qm VARCHAR(20) COMMENT  \'准货币(亿元)\';'
        #         'ALTER TABLE `{0}` MODIFY COLUMN qm_yoy VARCHAR(20) COMMENT  \'准货币同比增长(百分比)\';'
        #         'ALTER TABLE `{0}` MODIFY COLUMN ftd VARCHAR(20) COMMENT  \'定期存款(亿元)\';'
        #         'ALTER TABLE `{0}` MODIFY COLUMN ftd_yoy VARCHAR(20) COMMENT  \'定期存款同比增长(百分比)\';'
        #         'ALTER TABLE `{0}` MODIFY COLUMN sd VARCHAR(20) COMMENT  \'储蓄存款(亿元)\';'
        #         'ALTER TABLE `{0}` MODIFY COLUMN sd_yoy VARCHAR(20) COMMENT  \'储蓄存款同比增长(百分比)\';'
        #         'ALTER TABLE `{0}` MODIFY COLUMN rests VARCHAR(20) COMMENT  \'其他存款(亿元)\';'
        #         'ALTER TABLE `{0}` MODIFY COLUMN rests_yoy VARCHAR(20) COMMENT  \'其他存款同比增长(百分比)\';'
        #     ]
        # },
        # {
        #     "table": "ts2_money_supply_bal",
        #     "dtype": {
        #         "year": sa.types.INT,
        #         "m2": sa.types.NVARCHAR(20),
        #         "m1": sa.types.NVARCHAR(20),
        #         "m0": sa.types.NVARCHAR(20),
        #         "cd": sa.types.NVARCHAR(20),
        #         "qm": sa.types.NVARCHAR(20),
        #         "ftd": sa.types.NVARCHAR(20),
        #         "sd": sa.types.NVARCHAR(20),
        #         "rests": sa.types.NVARCHAR(20)
        #     },
        #     "clauses": [
        #         'ALTER TABLE `{0}` ADD INDEX (`year`);'
        #         'ALTER TABLE `{0}` MODIFY COLUMN m2 VARCHAR(20) COMMENT  \'货币和准货币(亿元)\';'
        #         'ALTER TABLE `{0}` MODIFY COLUMN m1 VARCHAR(20) COMMENT  \'货币(亿元)\';'
        #         'ALTER TABLE `{0}` MODIFY COLUMN m0 VARCHAR(20) COMMENT  \'流通中现金(亿元)\';'
        #         'ALTER TABLE `{0}` MODIFY COLUMN cd VARCHAR(20) COMMENT  \'活期存款(亿元)\';'
        #         'ALTER TABLE `{0}` MODIFY COLUMN qm VARCHAR(20) COMMENT  \'准货币(亿元)\';'
        #         'ALTER TABLE `{0}` MODIFY COLUMN ftd VARCHAR(20) COMMENT  \'定期存款(亿元)\';'
        #         'ALTER TABLE `{0}` MODIFY COLUMN sd VARCHAR(20) COMMENT  \'储蓄存款(亿元)\';'
        #         'ALTER TABLE `{0}` MODIFY COLUMN rests VARCHAR(20) COMMENT  \'其他存款(亿元)\';'
        #     ]
        # },
        # {
        #     "table": "ts2_new_stocks",
        #     "dtype": {
        #
        #         "code": sa.types.NVARCHAR(10),
        #         "xcode": sa.types.NVARCHAR(10),
        #         "name": sa.types.NVARCHAR(10),
        #         "ipo_date": sa.types.DATE,
        #         "issue_date": sa.types.DATE,
        #         "amount": sa.types.BIGINT,
        #         "markets": sa.types.BIGINT,
        #         "price": sa.types.FLOAT,
        #         "pe": sa.types.FLOAT,
        #         "limit": sa.types.FLOAT,
        #         "funds": sa.types.FLOAT,
        #         "ballot": sa.types.FLOAT
        #     },
        #     "clauses": [
        #         'ALTER TABLE `{0}` ADD INDEX (`code`);',
        #         'ALTER TABLE `{0}` MODIFY COLUMN ipo_date DATE COMMENT  \'上网发行日期\';',
        #         'ALTER TABLE `{0}` MODIFY COLUMN issue_date BIGINT COMMENT  \'上市日期\';',
        #         'ALTER TABLE `{0}` MODIFY COLUMN amount BIGINT COMMENT  \'发行数量(万股)\';',
        #         'ALTER TABLE `{0}` MODIFY COLUMN markets BIGINT COMMENT  \'上网发行数量(万股)\';',
        #         'ALTER TABLE `{0}` MODIFY COLUMN pe FLOAT COMMENT  \'发行市盈率\';',
        #         'ALTER TABLE `{0}` MODIFY COLUMN limit FLOAT COMMENT  \'个人申购上限(万股)\';',
        #         'ALTER TABLE `{0}` MODIFY COLUMN funds FLOAT COMMENT  \'募集资金(亿元)\';',
        #         'ALTER TABLE `{0}` MODIFY COLUMN ballot FLOAT COMMENT  \'网上中签率(百分比)\';'
        #     ]
        # },
        # {
        #     "table": "ts2_operation_data",
        #     "dtype": {
        #         "code": sa.types.NVARCHAR(10),
        #         "name": sa.types.NVARCHAR(20),
        #         'year': sa.types.INT,
        #         'quarter': sa.types.INT,
        #         "arturnover": sa.types.FLOAT,
        #         "arturndays": sa.types.FLOAT,
        #         "inventory_turnover": sa.types.FLOAT,
        #         "inventory_days": sa.types.FLOAT,
        #         "currentasset_turnover": sa.types.FLOAT,
        #         "currentasset_days": sa.types.FLOAT
        #     },
        #     "clauses": [
        #         'ALTER TABLE `{0}` ADD INDEX (`code`);',
        #         'ALTER TABLE `{0}` MODIFY COLUMN arturnover FLOAT COMMENT  \'应收账款周转率(次)\';'
        #         'ALTER TABLE `{0}` MODIFY COLUMN arturndays FLOAT COMMENT  \'应收账款周转天数(天)\';'
        #         'ALTER TABLE `{0}` MODIFY COLUMN inventory_turnover FLOAT COMMENT  \'存货周转率(次)\';'
        #         'ALTER TABLE `{0}` MODIFY COLUMN inventory_days FLOAT COMMENT  \'存货周转天数(天)\';'
        #         'ALTER TABLE `{0}` MODIFY COLUMN currentasset_turnover FLOAT COMMENT  \'流动资产周转率(次)\';'
        #         'ALTER TABLE `{0}` MODIFY COLUMN currentasset_days FLOAT COMMENT  \'流动资产周转天数(天)\';'
        #     ]
        # },
        # {
        #     "table": "ts2_ppi",
        #     "dtype": {
        #         "month": sa.types.NVARCHAR(20),
        #         "ppiip": sa.types.FLOAT,
        #         "ppi": sa.types.FLOAT,
        #         "qm": sa.types.FLOAT,
        #         "rmi": sa.types.FLOAT,
        #         "pi": sa.types.FLOAT,
        #         "cg": sa.types.FLOAT,
        #         "food": sa.types.FLOAT,
        #         "clothing": sa.types.FLOAT,
        #         "roeu": sa.types.FLOAT,
        #         "dcg": sa.types.FLOAT
        #     },
        #     "clauses": [
        #         'ALTER TABLE `{0}` ADD INDEX (`month`);'
        #         'ALTER TABLE `{0}` MODIFY COLUMN month VARCHAR(20) COMMENT  \'年.月\';'
        #         'ALTER TABLE `{0}` MODIFY COLUMN ppiip FLOAT COMMENT  \'工业品出厂价格指数\';'
        #         'ALTER TABLE `{0}` MODIFY COLUMN ppi FLOAT COMMENT  \'生产资料价格指数\';'
        #         'ALTER TABLE `{0}` MODIFY COLUMN qm FLOAT COMMENT  \'采掘工业价格指数\';'
        #         'ALTER TABLE `{0}` MODIFY COLUMN rmi FLOAT COMMENT  \'原材料工业价格指数\';'
        #         'ALTER TABLE `{0}` MODIFY COLUMN pi FLOAT COMMENT  \'加工工业价格指数\';'
        #         'ALTER TABLE `{0}` MODIFY COLUMN cg FLOAT COMMENT  \'生活资料价格指数\';'
        #         'ALTER TABLE `{0}` MODIFY COLUMN food FLOAT COMMENT  \'食品类价格指数\';'
        #         'ALTER TABLE `{0}` MODIFY COLUMN clothing FLOAT COMMENT  \'衣着类价格指数\';'
        #         'ALTER TABLE `{0}` MODIFY COLUMN roeu FLOAT COMMENT  \'一般日用品价格指数\';'
        #         'ALTER TABLE `{0}` MODIFY COLUMN dcg FLOAT COMMENT  \'耐用消费品价格指数\';'
        #     ]
        # },
        # {
        #     "table": "ts2_profit_data",
        #     "dtype": {
        #         "code": sa.types.NVARCHAR(10),
        #         "name": sa.types.NVARCHAR(20),
        #         "roe": sa.types.FLOAT,
        #         "net_profit_ratio": sa.types.FLOAT,
        #         "gross_profit_rate": sa.types.FLOAT,
        #         "net_profits": sa.types.FLOAT,
        #         "esp": sa.types.FLOAT,
        #         "business_income": sa.types.FLOAT,
        #         "bips": sa.types.FLOAT,
        #         "year": sa.types.INT,
        #         "quarter": sa.types.INT,
        #         "report_date": sa.types.DATETIME,
        #
        #         "divi": sa.types.FLOAT,
        #         "shares": sa.types.FLOAT
        #     },
        #     "clauses": [
        #         'ALTER TABLE `{0}` ADD INDEX (`code`);',
        #         'ALTER TABLE `{0}` MODIFY COLUMN roe FLOAT COMMENT  \'净资产收益率(百分比)\';',
        #         'ALTER TABLE `{0}` MODIFY COLUMN net_profit_ratio FLOAT COMMENT  \'净利率(百分比)\';',
        #         'ALTER TABLE `{0}` MODIFY COLUMN gross_profit_rate FLOAT COMMENT  \'毛利率(百分比)\';',
        #         'ALTER TABLE `{0}` MODIFY COLUMN net_profits FLOAT COMMENT  \'净利润(万元)\';',
        #         'ALTER TABLE `{0}` MODIFY COLUMN esp FLOAT COMMENT  \'每股收益\';',
        #         'ALTER TABLE `{0}` MODIFY COLUMN business_income FLOAT COMMENT  \'营业收入(百万元)\';',
        #         'ALTER TABLE `{0}` MODIFY COLUMN bips FLOAT COMMENT  \'每股主营业务收入(元)\';'
        #     ]
        # },
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
                "b1_v": sa.types.NVARCHAR(10),
                "b1_p": sa.types.FLOAT,
                "b2_v": sa.types.NVARCHAR(10),
                "b2_p": sa.types.FLOAT,
                "b3_v": sa.types.NVARCHAR(10),
                "b3_p": sa.types.FLOAT,
                "b4_v": sa.types.NVARCHAR(10),
                "b4_p": sa.types.FLOAT,
                "b5_v": sa.types.NVARCHAR(10),
                "b5_p": sa.types.FLOAT,
                "a1_v": sa.types.NVARCHAR(10),
                "a1_p": sa.types.FLOAT,
                "a2_v": sa.types.NVARCHAR(10),
                "a2_p": sa.types.FLOAT,
                "a3_v": sa.types.NVARCHAR(10),
                "a3_p": sa.types.FLOAT,
                "a4_v": sa.types.NVARCHAR(10),
                "a4_p": sa.types.FLOAT,
                "a5_v": sa.types.NVARCHAR(10),
                "a5_p": sa.types.FLOAT,
                "date": sa.types.DATE,
                "time": sa.types.TIME
            },
            "clauses": [
                'ALTER TABLE `{0}` ADD INDEX (`code`);'
            ]
        },
        # {
        #     "table": "ts2_report_data",
        #     "dtype": {
        #         'code': sa.types.NVARCHAR(10), 'name': sa.types.NVARCHAR(20),
        #         'year': sa.types.INT,
        #         'quarter': sa.types.INT,
        #         "eps": sa.types.FLOAT,
        #         "eps_yoy": sa.types.FLOAT,
        #         "bvps": sa.types.FLOAT,
        #         "roe": sa.types.FLOAT,
        #         "epcf": sa.types.FLOAT,
        #         "net_profits": sa.types.FLOAT,
        #         "profits_yoy": sa.types.FLOAT,
        #         "distrib": sa.types.NVARCHAR(50),
        #         "report_date": sa.types.NVARCHAR(20)
        #     },
        #     "clauses": [
        #         'ALTER TABLE `{0}` ADD INDEX (`code`);',
        #         'ALTER TABLE `{0}` MODIFY COLUMN eps FLOAT COMMENT  \'每股收益\';',
        #         'ALTER TABLE `{0}` MODIFY COLUMN eps_yoy FLOAT COMMENT  \'每股收益同比(百分比)\';',
        #         'ALTER TABLE `{0}` MODIFY COLUMN bvps FLOAT COMMENT  \'每股净资产\';',
        #         'ALTER TABLE `{0}` MODIFY COLUMN roe FLOAT COMMENT  \'净资产收益率(百分比)\';',
        #         'ALTER TABLE `{0}` MODIFY COLUMN epcf FLOAT COMMENT  \'每股现金流量(元)\';',
        #         'ALTER TABLE `{0}` MODIFY COLUMN net_profits FLOAT COMMENT  \'净利润(万元)\';',
        #         'ALTER TABLE `{0}` MODIFY COLUMN profits_yoy FLOAT COMMENT  \'净利润同比(百分比)\';',
        #         'ALTER TABLE `{0}` MODIFY COLUMN distrib VARCHAR(50) COMMENT  \'分配方案\';'
        #     ]
        # },
        # {
        #     "table": "ts2_rrr",
        #     "dtype": {
        #         "date": sa.types.DATE,
        #         "before": sa.types.NVARCHAR(20),
        #         "now": sa.types.FLOAT,
        #         "changed": sa.types.NVARCHAR(20)
        #     },
        #     "clauses": [
        #         'ALTER TABLE `{0}` ADD INDEX (`date`);',
        #         'ALTER TABLE `{0}` MODIFY COLUMN changed VARCHAR(20) COMMENT  \'调整幅度(百分比)\';'
        #     ]
        # },
        # {
        #     "table": "ts2_sme_classified",
        #     "dtype": {
        #         "index": sa.types.BIGINT,
        #         "code": sa.types.NVARCHAR(10),
        #         "name": sa.types.NVARCHAR(20),
        #     },
        #     "clauses": [
        #         'ALTER TABLE `{0}` ADD INDEX (`code`);'
        #     ]
        # },
        # {
        #     "table": "ts2_st_classified",
        #     "dtype": {
        #         "code": sa.types.NVARCHAR(10),
        #         "name": sa.types.NVARCHAR(20),
        #     },
        #     "clauses": [
        #         'ALTER TABLE `{0}` ADD INDEX (`code`);'
        #     ]
        # },
        # {
        #     "table": "ts2_stock_basics",
        #     "dtype": {
        #         "code": sa.types.NVARCHAR(10),
        #         "name": sa.types.NVARCHAR(20),
        #         "industry": sa.types.NVARCHAR(20),
        #         "area": sa.types.NVARCHAR(20),
        #         "pe": sa.types.FLOAT,
        #         "outstanding": sa.types.FLOAT,
        #         "totals": sa.types.FLOAT,
        #         "totalAssets": sa.types.FLOAT,
        #         "liquidAssets": sa.types.FLOAT,
        #         "fixedAssets": sa.types.FLOAT,
        #         "reserved": sa.types.FLOAT,
        #         "reservedPerShare": sa.types.FLOAT,
        #         "esp": sa.types.FLOAT,
        #         "bvps": sa.types.FLOAT,
        #         "pb": sa.types.FLOAT,
        #         "timeToMarket": sa.types.NVARCHAR(15),
        #         "undp": sa.types.FLOAT,
        #         "perundp": sa.types.FLOAT,
        #         "rev": sa.types.FLOAT,
        #         "profit": sa.types.FLOAT,
        #         "gpr": sa.types.FLOAT,
        #         "npr": sa.types.FLOAT,
        #         "holders": sa.types.BIGINT
        #     },
        #     "clauses": [
        #         'ALTER TABLE `{0}` ADD INDEX (`code`);',
        #         'ALTER TABLE `{0}` MODIFY COLUMN pe FLOAT COMMENT  \'市盈率\';',
        #         'ALTER TABLE `{0}` MODIFY COLUMN outstanding FLOAT COMMENT  \'流通股本(亿)\';',
        #         'ALTER TABLE `{0}` MODIFY COLUMN totals FLOAT COMMENT  \'总股本(亿)\';',
        #         'ALTER TABLE `{0}` MODIFY COLUMN totalAssets FLOAT COMMENT  \'总资产(万)\';',
        #         'ALTER TABLE `{0}` MODIFY COLUMN liquidAssets FLOAT COMMENT  \'流动资产\';',
        #         'ALTER TABLE `{0}` MODIFY COLUMN fixedAssets FLOAT COMMENT  \'固定资产\';',
        #         'ALTER TABLE `{0}` MODIFY COLUMN reserved FLOAT COMMENT  \'公积金\';',
        #         'ALTER TABLE `{0}` MODIFY COLUMN reservedPerShare FLOAT COMMENT  \'每股公积金\';',
        #         'ALTER TABLE `{0}` MODIFY COLUMN esp FLOAT COMMENT  \'每股收益\';',
        #         'ALTER TABLE `{0}` MODIFY COLUMN bvps FLOAT COMMENT  \'每股净资\';',
        #         'ALTER TABLE `{0}` MODIFY COLUMN pb FLOAT COMMENT  \'市净率\';',
        #         'ALTER TABLE `{0}` MODIFY COLUMN timeToMarket VARCHAR(15 COMMENT  \'上市日期\';',
        #         'ALTER TABLE `{0}` MODIFY COLUMN undp FLOAT COMMENT  \'未分利润\';',
        #         'ALTER TABLE `{0}` MODIFY COLUMN perundp FLOAT COMMENT  \'每股未分配\';',
        #         'ALTER TABLE `{0}` MODIFY COLUMN rev FLOAT COMMENT  \'收入同比(百分比)\';',
        #         'ALTER TABLE `{0}` MODIFY COLUMN profit FLOAT COMMENT  \'利润同比(百分比)';',
        #         'ALTER TABLE `{0}` MODIFY COLUMN gpr FLOAT COMMENT  \'毛利率(百分比)\';',
        #         'ALTER TABLE `{0}` MODIFY COLUMN npr FLOAT COMMENT  \'净利润率(百分比)\';',
        #         'ALTER TABLE `{0}` MODIFY COLUMN holders BIGINT COMMENT  \'股东人数\';'
        #     ]
        # },
        # {
        #     "table": "ts2_sz50s",
        #     "dtype": {
        #         "code": sa.types.NVARCHAR(10),
        #         "name": sa.types.NVARCHAR(20),
        #         "date": sa.types.DATE
        #     },
        #     "clauses": [
        #         'ALTER TABLE `{0}` ADD INDEX (`code`);'
        #     ]
        # },
        # {
        #     "table": "ts2_tick_data",
        #     "dtype": {
        #         "code": sa.types.NVARCHAR(10),
        #         "time": sa.types.TIME,
        #         "price": sa.types.FLOAT,
        #         "change": sa.types.NVARCHAR(20),
        #         "volume": sa.types.BIGINT,
        #         "amount": sa.types.BIGINT,
        #         "type": sa.types.NVARCHAR(10),
        #         "date": sa.types.DATE
        #     },
        #     "clauses": [
        #         'ALTER TABLE `{0}` ADD INDEX (`date`);',
        #         'ALTER TABLE `{0}` MODIFY COLUMN type VARCHAR(10) COMMENT  \'买卖类型【买盘、卖盘、中性盘】\';'
        #     ]
        # },
        # {
        #     "table": "ts2_today_all",
        #     "dtype": {
        #         "code": sa.types.NVARCHAR(10),
        #         "name": sa.types.NVARCHAR(20),
        #         "changepercent": sa.types.FLOAT,
        #         "trade": sa.types.FLOAT,
        #         "open": sa.types.FLOAT,
        #         "high": sa.types.FLOAT,
        #         "low": sa.types.FLOAT,
        #         "settlement": sa.types.FLOAT,
        #         "volume": sa.types.FLOAT,
        #         "turnoverratio": sa.types.FLOAT,
        #         "amount": sa.types.FLOAT,
        #         "per": sa.types.FLOAT,
        #         "pb": sa.types.FLOAT,
        #         "mktcap": sa.types.FLOAT,
        #         "nmc": sa.types.FLOAT,
        #         "date": sa.types.DATE
        #     },
        #     "clauses": [
        #         'ALTER TABLE `{0}` ADD INDEX (`code`);',
        #         'ALTER TABLE `{0}` MODIFY COLUMN changepercent FLOAT COMMENT  \'涨跌率\';',
        #         'ALTER TABLE `{0}` MODIFY COLUMN trade FLOAT COMMENT  \'现价\';',
        #         'ALTER TABLE `{0}` MODIFY COLUMN settlement FLOAT COMMENT  \'昨日收盘价\';',
        #         'ALTER TABLE `{0}` MODIFY COLUMN turnoverratio FLOAT COMMENT  \'换手率\';',
        #         'ALTER TABLE `{0}` MODIFY COLUMN per FLOAT COMMENT  \'市盈率率\';',
        #         'ALTER TABLE `{0}` MODIFY COLUMN pb FLOAT COMMENT  \'市净率\';',
        #         'ALTER TABLE `{0}` MODIFY COLUMN mktcap FLOAT COMMENT  \'总市值\';',
        #         'ALTER TABLE `{0}` MODIFY COLUMN nmc FLOAT COMMENT  \'流通市值\';'
        #     ]
        # },
        # {
        #     "table": "ts2_today_ticks",
        #     "dtype": {
        #         "code": sa.types.NVARCHAR(10),
        #         "time": sa.types.TIME,
        #         "price": sa.types.FLOAT,
        #         "pchange": sa.types.NVARCHAR(10),
        #         "change": sa.types.FLOAT,
        #         "volume": sa.types.BIGINT,
        #         "amount": sa.types.BIGINT,
        #         "type": sa.types.NVARCHAR(10),
        #         "date": sa.types.DATE
        #     },
        #     "clauses": [
        #         'ALTER TABLE `{0}` ADD INDEX (`code`);',
        #         'ALTER TABLE `{0}` ADD INDEX (`date`);'
        #     ]
        # },
        # {
        #     "table": "ts2_xsg_data",
        #     "dtype": {
        #         "code": sa.types.NVARCHAR(10),
        #         "name": sa.types.NVARCHAR(20),
        #         "date": sa.types.DATE,
        #         "count": sa.types.FLOAT,
        #         "ratio": sa.types.FLOAT
        #     },
        #     "clauses": [
        #         'ALTER TABLE `{0}` ADD INDEX (`code`);',
        #         'ALTER TABLE `{0}` MODIFY COLUMN ratio FLOAT COMMENT  \'占总盘比率\';'
        #     ]
        # },
        # {
        #     "table": "ts2_zz500s",
        #     "dtype": {
        #         "code": sa.types.NVARCHAR(10),
        #         "name": sa.types.NVARCHAR(20),
        #         "date": sa.types.DATE,
        #         "weight": sa.types.FLOAT
        #     },
        #     "clauses": [
        #         'ALTER TABLE `{0}` ADD INDEX (`code`);'
        #     ]
        # }
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


