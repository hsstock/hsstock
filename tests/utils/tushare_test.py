import tushare as ts

# print(ts.__version__)
# df = ts.get_hist_data('601138')
# print( df )
#
# df.to_csv('./000875.csv')
# df.to_excel('./000875.xlsx')
# df.to_hdf('./hdf.h5','date')
# df.to_json('./000875.json',orient='records')
# #
# df = ts.get_stock_basics()
# date = df.ix['601138']['timeToMarket'] #上市日期YYYYMMDD
# print(date)
#
#
# ts.get_today_all()

# df = ts.get_tick_data('601138',date='2018-06-13')
# print(df.head(10))

#
#
# df = ts.get_realtime_quotes('601138') #Single stock symbol
# print( df[['code','name','price','bid','ask','volume','amount','time']] )

from sqlalchemy import create_engine
import tushare as ts
#
df = ts.get_tick_data('002049', date='2018-06-13')
#engine = create_engine('mysql://hsstock:Ba123!@#@10.240.154.201/hsstock?charset=utf8')
engine = create_engine('mysql://hsstock:Ba123!@#@192.168.1.4/hsstock?charset=utf8')

#存入数据库
df.to_sql('person3',engine, if_exists='append')


# 投资参考数据

import tushare as ts

# df = ts.profit_data(top=100)
# #df.groupby('shares').apply(lambda subf: subf['shares'])
# print(df)
#
# print( df[df.shares>=10])
#
#
# ts.forecast_data(2016,1)
#
# print( ts.xsg_data() )

# print( ts.fund_holdings(2018, 1) )

# print( ts.new_stocks() )

#ts.sh_margins(start='2018-01-01', end='2018-04-19')

# ts.sh_margin_details(start='2015-01-01', end='2015-04-19', symbol='601989')


# 股票分类数据

# print( ts.get_industry_classified() )


# print( ts.get_concept_classified() )


# print( ts.get_area_classified() )

# print( ts.get_sme_classified() )

# print (ts.get_gem_classified() )

# print( ts.get_st_classified() )

# print ( ts.get_hs300s() )

# print( ts.get_sz50s() )

# print( ts.get_zz500s() )


# print( ts.get_terminated() )

# print( ts.get_suspended() )


# 基本面数据

# print (ts.get_stock_basics())

# print( ts.get_report_data(2018,1) )

# print( ts.get_profit_data(2018,1) )

# print( ts.get_operation_data(2018,1) )

# print( ts.get_growth_data(2018,1) )

# print( ts.get_debtpaying_data(2018,1) )

# print( ts.get_cashflow_data(2018,1) )

# 宏观经济数据

# print( ts.get_deposit_rate() )

# print( ts.get_loan_rate() )


# print( ts.get_rrr() )

# print( ts.get_money_supply() )

# print( ts.get_money_supply_bal() )

# print( ts.get_gdp_year() )

# print( ts.get_gdp_quarter() )

# print( ts.get_gdp_for() )

# print( ts.get_gdp_pull() )

# print( ts.get_gdp_contrib() )

# print( ts.get_cpi() )

# print( ts.get_ppi() )

# 新闻事件数据

#print( ts.get_latest_news(top=100, show_content=True) )

#print( ts.get_notices() )

#print( ts.guba_sina(True) )
#print( ts.guba_sina(True).ix[3]['content'])

# 龙虎榜数据

#print( ts.top_list('2018-06-12') )

#print( ts.cap_tops() )

# print( ts.broker_tops() )

#print( ts.inst_tops() )

#print( ts.inst_detail() )


# 银行间同业拆借

#print( ts.shibor_data() )
#print( ts.shibor_quote_data() )

#print( ts.shibor_ma_data() )

#print( ts.lpr_data() )
#print( ts.lpr_ma_data() )

# 实时票房

# df = ts.realtime_boxoffice()
# print(df)

# df = ts.day_boxoffice()
# print(df)


#df = ts.month_boxoffice()
#print(df)

# df = ts.day_cinema()
# print(df)