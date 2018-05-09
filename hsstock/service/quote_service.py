# -*- coding: UTF-8 -*-


class LF(object):
    def __init__(self,quote_ctx):
        print('LF')
        self.ctx = quote_ctx

    def get_trading_days(self, market, start_date=None, end_date=None):
        # 获取交易日
        ret_status, ret_data = self.ctx.get_trade_days(market)
        if ret_status == RET_ERROR:
            print(ret_data)
            exit()
        print("TRADING DAYS")
        for x in ret_data:
            print(x)

    def get_stock_basicinfo(self, market, stock_type='STOCK'):
        # 获取股票信息
        print('a')

#     def get_history_kline(self, code, start=None, end=None, ktype='K_DAY', autype='qfq'):
#         # 获取历史K线
#
#     def get_autype_list(self, code_list):
#         # 获取复权因子
#
#     def get_market_snapshot(self, code_list):
#         # 获取市场快照
#
#     def get_plate_list(self, market, plate_class):
#         # 获取板块集合下的子板块列表
#
#     def get_plate_stock(self, market, stock_code):
#         # 获取板块下的股票列表
#
#
#
# class HF(object):
#     def __init__(self):
#         print('HF')
#
#     def get_stock_quote(self, code_list):
#         #  获取报价
#
#     def get_rt_ticker(self, code, num):
#         # 获取逐笔
#
#     def get_cur_kline(self, code, num, ktype=' K_DAY', autype='qfq'):
#         # 获取当前K线
#
#     def get_order_book(self, code):
#         # 获取摆盘
#
#     def get_rt_data(self):
#         #获取分时数据
#
#     def get_broker_queue(self):
#         #获取经纪队列
#
# #回调处理基类
# # StockQuoteHandlerBase # 报价处理基类
# #
# # OrderBookHandlerBase  # 摆盘处理基类
# #
# # CurKlineHandlerBase   # 实时K线处理基类
# #
# # TickerHandlerBase     # 逐笔处理基类
# #
# # RTDataHandlerBase     # 分时数据处理基类
# #
# # BrokerHandlerBase     # 经纪队列处理基类
#
# class Subscribe(Object):
#     def __init__(self):
#         print('subscribe')
#
#     def subscribe(self, stock_code, data_type, push=False):
#         # 订阅
#
#     def unsubscribe(self, stock_code, data_type):
#         # 退订
#
#     def query_subscription(self):
#         # 查询订阅