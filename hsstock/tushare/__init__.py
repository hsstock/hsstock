# -*- coding:utf-8 -*- 

__version__ = '1.2.4'
__author__ = 'Jimmy Liu'

"""
for trading data
"""
from hsstock.tushare.stock.trading import (get_hist_data, get_tick_data,
                                   get_today_all, get_realtime_quotes,
                                   get_h_data, get_today_ticks,
                                   get_index, get_hists,
                                   get_k_data, get_day_all,
                                   get_sina_dd, bar, tick,
                                   get_markets, quotes,
                                   get_instrument, reset_instrument)

"""
for trading data
"""
from hsstock.tushare.stock.fundamental import (get_stock_basics, get_report_data,
                                       get_profit_data,
                                       get_operation_data, get_growth_data,
                                       get_debtpaying_data, get_cashflow_data,
                                       get_balance_sheet, get_profit_statement, get_cash_flow)

"""
for macro data
"""
from hsstock.tushare.stock.macro import (get_gdp_year, get_gdp_quarter,
                                 get_gdp_for, get_gdp_pull,
                                 get_gdp_contrib, get_cpi,
                                 get_ppi, get_deposit_rate,
                                 get_loan_rate, get_rrr,
                                 get_money_supply, get_money_supply_bal,
                                 get_gold_and_foreign_reserves)

"""
for classifying data
"""
from hsstock.tushare.stock.classifying import (get_industry_classified, get_concept_classified,
                                       get_area_classified, get_gem_classified,
                                       get_sme_classified, get_st_classified,
                                       get_hs300s, get_sz50s, get_zz500s,
                                       get_terminated, get_suspended)

"""
for macro data
"""
from hsstock.tushare.stock.newsevent import (get_latest_news, latest_content,
                                     get_notices, notice_content,
                                     guba_sina)

"""
for reference
moneyflow_hsgt:沪深港通资金流向
"""
from hsstock.tushare.stock.reference import (profit_data, forecast_data,
                                     xsg_data, fund_holdings,
                                     new_stocks, new_cbonds, sh_margins,
                                     sh_margin_details,
                                     sz_margins, sz_margin_details,
                                     top10_holders, profit_divis,
                                     moneyflow_hsgt, margin_detail,
                                     margin_target, margin_offset,
                                     margin_zsl, stock_issuance,
                                     stock_pledged, pledged_detail)

"""
for shibor
"""
from hsstock.tushare.stock.shibor import (shibor_data, shibor_quote_data,
                                  shibor_ma_data, lpr_data,
                                  lpr_ma_data)

"""
for LHB
"""
from hsstock.tushare.stock.billboard import (top_list, cap_tops, broker_tops,
                                     inst_tops, inst_detail)


"""
for utils
"""
from hsstock.tushare.util.dateu import (trade_cal, is_holiday)



from hsstock.tushare.internet.boxoffice import (realtime_boxoffice, day_boxoffice,
                                        day_cinema, month_boxoffice)

from hsstock.tushare.internet.indexes import (bdi)

"""
for fund data
"""
from hsstock.tushare.fund.nav import (get_nav_open, get_nav_close, get_nav_grading,
                              get_nav_history, get_fund_info)

"""
for trader API
"""
from hsstock.tushare.trader.trader import TraderAPI

from hsstock.tushare.stock.minsdata import TsData

"""
for futures API
"""
from hsstock.tushare.futures.intlfutures import (get_intlfuture)


from hsstock.tushare.stock.globals import (global_realtime)


from hsstock.tushare.util.mailmerge import (MailMerge)


"""
for futures API
"""
from hsstock.tushare.futures.domestic import (get_cffex_daily, get_czce_daily,
                                      get_dce_daily, get_future_daily,
                                      get_shfe_daily, get_shfe_vwap)


from hsstock.tushare.coins.market import (coins_tick, coins_bar,
                                  coins_snapshot, coins_trade)

from hsstock.tushare.util.conns import (get_apis, close_apis)