# -*- coding: UTF-8 -*-

from abc import ABC, abstractclassmethod

from futuquant.open_context import *


'''
交易接口有频率限制，30秒内不能超过20次交易请求
'''

'''
def unlock_trade(self,trade_password, trade_password_md5=None):
def login_new_account(self,user_id, login_password_md5, trade_password, trade_password_md5=None):
def place_order(self, price, qty, strcode, orderside, ordertype=0, envtype=0,
                                                 order_deal_push=False, price_mode=PriceRegularMode.IGNORE):
def set_order_status(self,status, orderid=0, envtype=0):
def change_order(self,price, qty, orderid=0, envtype=0):
def accinfo_query(self,envtype=0):
def order_list_query(self, orderid="", statusfilter="",  strcode='', start='', end='', envtype=0):
def position_list_query(self, strcode='', stocktype='', pl_ratio_min='', pl_ratio_max='', envtype=0):
def deal_list_query(self, envtype=0):
def history_order_list_query(self,statusfilter='', strcode='', start='', end='', envtype=0):
def history_deal_list_query(self, strcode, start, end, envtype=0):
def subscribe_order_deal_push(self, order_list, order_deal_push=True, envtype=0):
'''

class Trade(ABC):
    def __init__(self,trade_ctx):
        self.ctx = trade_ctx

    def unlock_trade(self, trade_password, trade_password_md5=None):
        '''
        功能：交易解锁。

        :param trade_password: 用户交易密码。
        :param trade_password_md5: 交易密码32位MD5加密16进制表示，trade_password和trade_password_md5同时传入时，只使用trade_password_md5
        :return: ret_code失败时，ret_data返回为错误描述字符串； 正常情况下，ret_code为0, ret_data返回None。

        失败情况：
            交易密码错误
            客户端内部或网络错误
        '''
        ret_code, ret_data = self.ctx.unlock_trade(trade_password, trade_password_md5)
        print(ret_code, ret_data)

    def login_new_account(self, user_id, login_password_md5, trade_password, trade_password_md5=None):
        '''
        功能：切换牛牛号登录
        :param user_id: 需要切换的牛牛号
        :param login_password_md5: 登录密码32位MD5加密16进制表示
        :param trade_password: 交易密码明文
        :param trade_password_md5: 交易密码32位MD5加密16进制表示，trade_password和trade_password_md5同时传入时，只使用trade_password_md5
        :return: ret = RET_OK表示切换成功。

注           :切换牛牛号登录会导致API接口断开重连。
        '''
        ret_code, ret_data = self.ctx.login_new_account(user_id, login_password_md5, trade_password,
                                                        trade_password_md5=None)
        print(ret_code, ret_data)



class HKTrade(Trade):
    def __init__(self,trade_ctx):
        super(HKTrade,self).__init__(trade_ctx)


    def place_order(self, price, qty, strcode, orderside, ordertype=0, envtype=0,
                                                     order_deal_push=False, price_mode=PriceRegularMode.IGNORE):
        '''
        功能：港股下单接口，自动订阅订单推送。

        :param price: 交易价格。
        :param qty: 交易数量。
        :param strcode: 股票代码。例如：“HK.00700”。
        :param orderside: 交易方向。如下表所示。
        :param ordertype: 交易类型。与美股不同！如下表所示。
        :param envtype: 交易环境参数。如下表所示。
        :param order_deal_push: 是否订阅成交推送
        :param price_mode: 报价调整模式，在提交订单前，将price调整至符合价位表要求的数值
        :return:
            ret_code失败时，ret_data返回为错误描述字符串； 正常情况下，ret_code为0，ret_data为一个dataframe, 其中包括：

                返回字符串	    说明	    返回字符串	说明
                code	        股票ID	stock_name	股票名称
                dealt_avg_price	成交均价	dealt_qty	成交数量
                qty	            订单数量	orderid	    订单ID
                order_type	    交易类型	price	    交易价格
                status	        订单状态(具体状态如下)
                submited_time	提交时间
                updated_time	更新时间
                order_side	交易方向

                status	订单类型	status	订单类型
                0	服务器处理中	1	等待成交
                2	部分成交	    3	全部成交
                4	已失效	    5	下单失败
                6	已撤单	    7	已删除
                8	等待开盘	    21	本地已发送
                22	本地已发送，服务器返回下单失败、没产生订单
                23	本地已发送，等待服务器返回超时

                order_side	交易方向
                0	买入
                1	卖出

                order_type	交易类型
                    0	增强限价单(普通交易)
                    1	竞价单(竞价交易)
                    3	竞价限价单(竞价限价)
            失败情况：

                参数错误
                客户端内部或网络错误
                不满足下单条件

        orderside	交易方向
            0	买入
            1	卖出
        ordertype	交易类型
            0	增强限价单(普通交易)
            1	竞价单(竞价交易)
            3	竞价限价单(竞价限价)
        envtype	交易环境参数
            0	真实交易
            1	仿真交易
        '''
        ret_code, ret_data = self.ctx.place_order(price, qty, strcode, orderside, ordertype, envtype,
                                                     order_deal_push, price_mode)
        print(ret_code, ret_data)

    def set_order_status(self,status, orderid=0, envtype=0):
        '''
        功能：更改某指定港股订单状态。

        :param status: 更改状态的类型。如下表所示。
        :param orderid: 订单ID。
        :param envtype: 交易环境参数。如下表所示。
                status	更改状态的类型
                    0	撤单
                    1	失效
                    2	生效
                    3	删除
                envtype	交易环境参数
                    0	真实交易
                    1	仿真交易
        :return:    ret_code失败时，ret_data返回为错误描述字符串； 正常情况下，ret_code为0，ret_data为一个dataframe, 其中包括：
            envtype: 交易环境参数。0是真实交易，1是仿真交易
            orderid: 订单ID。

        失败情况：
            参数错误
            客户端内部或网络错误
            订单不存在
        '''
        ret_code, ret_data = self.ctx.set_order_status(status, orderid, envtype)
        print(ret_code, ret_data)

    def change_order(self,price, qty, orderid=0, envtype=0):
        '''
        功能：修改某指定港股订单。

        :param price: 交易价格。
        :param qty: 交易数量。
        :param orderid: 订单ID。
        :param envtype: 交易环境参数。如下表所示。
            envtype	交易环境参数
                0	真实交易
                1	仿真交易
        :return:ret_code失败时，ret_data返回为错误描述字符串； 正常情况下，ret_code为0，ret_data为一个dataframe, 其中包括：

            envtype: 交易环境参数。0是真实交易，1是仿真交易

            orderid: 订单ID。

        失败情况：

            参数错误
            客户端内部或网络错误
            订单不存在
        '''
        ret_code, ret_data = self.ctx.change_order(price, qty, orderid, envtype)
        print(ret_code, ret_data)

    def accinfo_query(self,envtype=0):
        '''
        功能：查询港股账户信息。

        :param envtype:交易环境参数。如下表所示。
            envtype	交易环境参数
                0	真实交易
                1	仿真交易
        :return:ret_code失败时，ret_data返回为错误描述字符串； 正常情况下，ret_code为0，ret_data为一个dataframe, 其中包括：

                返回字符串	说明	返回字符串	说明
                ZQSZ	证券市值	XJJY	现金结余
                KQXJ	可取现金	DJZJ	冻结资金
                ZSJE	追收金额	ZGJDE	最高借贷额
                YYJDE	已用借贷额	GPBZJ	股票保证金
                ZCJZ	资产净值
                Power	现金账号的购买力，不适用于融资账号(因每支股票的融资额不同，融资账户的购买力由购买的股票决定)
        失败情况：

                参数错误
                客户端内部或网络错误
        '''
        ret_code, ret_data = self.ctx.accinfo_query(envtype)
        print(ret_code, ret_data)

    def order_list_query(self, orderid="", statusfilter="",  strcode='', start='', end='', envtype=0):
        '''
        功能：查询港股今日订单列表。
        :param orderid:指定订单id查询，为空或0为不指定。
        :param statusfilter:状态过滤字符串，为空返回全部订单，”,”分隔需要返回的状态，如”1,2,3”返回的是等待成交，部分成交以及全部成交的订单，状态如下表所示
                    statusfilter	返回订单的状态	statusfilter	返回订单的状态
                    0	服务器处理中	1	等待成交
                    2	部分成交	3	全部成交
                    4	已失效	5	下单失败
                    6	已撤单	7	已删除
                    8	等待开盘	21	本地已发送
                    22	本地已发送，服务器返回下单失败、没产生订单
                    23	本地已发送，等待服务器返回超时
        :param strcode:股票代码过滤，例如”hk.00700”，为空为不限制。
        :param start: 下单时间过滤，格式”hh:mm:ss”, 过滤时间开始点，为空为00:00:00
        :param end: 下单时间过滤，格式”hh:mm:ss”, 过滤时间结束点，为空为23:59:59。
        :param envtype:交易环境参数。如下表所示。
                envtype	交易环境参数
                0	真实交易
                1	仿真交易
        :return:ret_code失败时，ret_data返回为错误描述字符串； 正常情况下，ret_code为0，ret_data为一个dataframe, 其中包括：

                返回字符串	        说明	    返回字符串	说明
                code	            股票ID	stock_name	股票名称
                dealt_avg_price	    成交均价	dealt_qty	成交数量
                qty	                订单数量	orderid	    订单ID
                order_type	        交易类型	price	    交易价格
                status	            订单状态(具体状态如下)
                submited_time	提交时间
                updated_time	更新时间
                order_side	交易方向
                status	订单类型	status	订单类型
                0	服务器处理中	1	等待成交
                2	部分成交	    3	全部成交
                4	已失效	    5	下单失败
                6	已撤单	    7	已删除
                8	等待开盘	    21	本地已发送
                22	本地已发送，服务器返回下单失败、没产生订单
                23	本地已发送，等待服务器返回超时

                order_side	交易方向
                    0	买入
                    1	卖出
                order_type	交易类型
                    0	增强限价单(普通交易)
                    1	竞价单(竞价交易)
                    3	竞价限价单(竞价限价)
        失败情况：
                参数错误
                客户端内部或网络错误
        '''
        ret_code, ret_data = self.ctx.order_list_query(orderid, statusfilter, strcode, start, end, envtype)
        print(ret_code, ret_data)

    def position_list_query(self, strcode='', stocktype='', pl_ratio_min='', pl_ratio_max='', envtype=0):
        '''
        查询持仓列表
        :param strcode: 股票代码过滤，例如”hk.00700”，为空为不限制。
        :param stocktype: 股票类型
                    正股	“STOCK”
                    指数	“IDX”
                    ETF基金	“ETF”
                    涡轮牛熊	“WARRANT”
                    债券	“BOND”
        :param pl_ratio_min:盈亏比例过滤，“10”表示只返回盈亏比例10%以上（包括10%）的持仓，为空为不限制。
        :param pl_ratio_max: 盈亏比例过滤，“10”表示只返回盈亏比例10%以下（包括10%）的持仓，为空为不限制。
        :param envtype: 交易环境参数。如下表所示。
            envtype	交易环境参数
                0	真实交易
                1	仿真交易
        :return:    ret_code失败时，ret_data返回为错误描述字符串； 正常情况下，ret_code为0，ret_data为一个dataframe, 其中包括：

            返回字符串	说明	    返回字符串	说明
            code	    股票ID	stock_name	股票名称
            qty	        持有数量
            can_sell_qty可卖数量
            cost_price	成本价
            cost_price_valid	成本价是否有效(非0有效)
            market_val	市值
            nominal_price	市价
            pl_ratio	盈亏比例
            pl_ratio_valid	盈亏比例是否有效(非0有效)
            pl_val	盈亏金额
            pl_val_valid	盈亏金额是否有效(非0有效)
            today_buy_qty	今日买入数量
            today_buy_val	今日买入金额
            today_pl_val	今日盈亏金额
            today_sell_qty	今日卖出数量
            today_sell_val	今日卖出金额
        失败情况：

            参数错误
            客户端内部或网络错误
        '''
        ret_code, ret_data = self.ctx.position_list_query(strcode, stocktype, pl_ratio_min, pl_ratio_max, envtype)
        print(ret_code, ret_data)

    def deal_list_query(self, envtype=0):
        '''
        功能：查询港股今日成交列表。
        :param self:
        :param envtype: 交易环境参数。如下表所示。
            envtype	交易环境参数
                0	真实交易
                1	仿真交易
        :return: ret_code失败时，ret_data返回为错误描述字符串； 正常情况下，ret_code为0，ret_data为一个dataframe, 其中包括：

                code: 股票代码。

                stock_name: 股票名称。

                dealid: 成交ID。

                orderid: 订单ID。

                price: 交易价格。

                qty: 交易数量。

                orderside: 交易方向，0表示买入，1表示卖出。

                time: 成交时间。

        失败情况：

                参数错误
                客户端内部或网络错误
        '''
        ret_code, ret_data = self.ctx.deal_list_query(envtype)
        print(ret_code, ret_data)

    def history_order_list_query(self,statusfilter='', strcode='', start='', end='', envtype=0):
        '''
        功能：查询历史订单列表, 30秒内不能超过5次请求, 时间段最多90自然日。
        :param self:
        :param statusfilter: 状态过滤字符串，为空返回全部订单，”,”分隔需要返回的状态，如”1,2,3”返回的是等待成交，部分成交以及全部成交的订单，状态如下表所示
            statusfilter	返回订单的状态	statusfilter	返回订单的状态
            0	服务器处理中	1	等待成交
            2	部分成交    	3	全部成交
            4	已失效	    5	下单失败
            6	已撤单	    7	已删除
            8	等待开盘	    21	本地已发送
            22	本地已发送，服务器返回下单失败、没产生订单
            23	本地已发送，等待服务器返回超时
        :param strcode: 股票代码过滤，例如”hk.00700”，为空为不限制。
        :param start: 历史订单查询起始时间，格式”yy-mm-dd”。
        :param end: 历史订单查询截止时间，格式”yy-mm-dd”。 起止时间参数组合如下表所示：
                start	end	查询时间段
                空	非空	end前90天
                非空	空	start后90天
                空	空	90天前至当天
        :param envtype: 交易环境参数。如下表所示。
            envtype	交易环境参数
                0	真实交易
                1	仿真交易
        :return:
            ret_code失败时，ret_data返回为错误描述字符串； 正常情况下，ret_code为0，ret_data为一个dataframe, 其中包括：

            返回字符串	说明	返回字符串	说明
            code	股票ID	stock_name	股票名称
            orderid | 订单ID	dealt_qty	成交数量
            order_type	交易类型	price	交易价格
            status	订单状态(具体状态如下)	submited_time	提交时间
            updated_time	更新时间	order_side	交易方向
            qty	订单数量
            status	订单类型	status	订单类型
            0	服务器处理中	1	等待成交
            2	部分成交	    3	全部成交
            4	已失效	    5	下单失败
            6	已撤单	    7	已删除
            8	等待开盘	    21	本地已发送
            22	本地已发送，服务器返回下单失败、没产生订单
            23	本地已发送，等待服务器返回超时
            order_side	交易方向
                0	买入
                1	卖出
            order_type	交易类型
                0	增强限价单(普通交易)
                1	竞价单(竞价交易)
                3	竞价限价单(竞价限价)
        失败情况：

            参数错误
            客户端内部或网络错误
        '''
        ret_code, ret_data = self.ctx.history_order_list_query(statusfilter, strcode, start, end, envtype)
        print(ret_code, ret_data)

    def history_deal_list_query(self, strcode='', start='', end='', envtype=0):
        '''
        功能：查询历史订单列表, 30秒内不能超过5次请求, 时间段最多90自然日。
        :param strcode: 股票代码过滤，例如”hk.00700”，为空为不限制。
        :param start: 历史订单查询其实时间，格式”yy-mm-dd”, 为空则为end字段前90天。
        :param end:  历史订单查询其实时间，格式”yy-mm-dd”, 为空则为start字段后90天，若start为空，则end为当天。
        :param envtype: 交易环境参数。如下表所示。
            envtype	交易环境参数
                0	真实交易
                1	仿真交易
        :return: ret_code失败时，ret_data返回为错误描述字符串； 正常情况下，ret_code为0，ret_data为一个dataframe, 其中包括：

            code: 股票代码。

            stock_name: 股票名称。

            dealid: 成交ID。

            orderid: 订单ID。

            price: 交易价格。

            qty: 交易数量。

            order_side: 交易方向，0表示买入，1表示卖出。

            time: 成交时间。

        失败情况：

            参数错误
            客户端内部或网络错误
        '''
        ret_code, ret_data = self.ctx.history_deal_list_query(strcode, start, end, envtype)
        print(ret_code, ret_data)

    def subscribe_order_deal_push(self, order_list, order_deal_push=True, envtype=0):
        '''
        功能：订阅订单成交推送。
        :param order_list: 订阅的订单ID，多个或单个，列表或字符串（字符串用英文逗号分割），单独传空表示订阅全部订单，包括后来新增的。
        :param order_deal_push: 是否订阅成交推送。
        :param envtype: 交易环境参数
                0	真实交易
                1	仿真交易
        :return: ret_code失败时，ret_data返回为错误描述字符串； 正常情况下，ret_code为0。

        失败情况：
            参数错误
            客户端内部或网络错误
        '''
        ret_code = self.ctx.subscribe_order_deal_push(order_list, order_deal_push, envtype)
        print(ret_code)

class USTrade(Trade):
    def __init__(self,trade_ctx):
        super(USTrade,self).__init__(trade_ctx)

    def unlock_trade(self,trade_password, trade_password_md5=None):
        '''
        功能：交易解锁。

        :param trade_password: 用户交易密码。
        :param trade_password_md5: 交易密码32位MD5加密16进制表示，trade_password和trade_password_md5同时传入时，只使用trade_password_md5
        :return: ret_code失败时，ret_data返回为错误描述字符串； 正常情况下，ret_code为0, ret_data返回None。

        失败情况：
            交易密码错误
            客户端内部或网络错误
        '''
        ret_code, ret_data = self.ctx.unlock_trade(trade_password,trade_password_md5)
        print(ret_code, ret_data)

    def place_order(self, price, qty, strcode, orderside, ordertype=1, envtype=0,
                                                     order_deal_push=False):
        '''
        下单接口

        功能：美股下单接口。美股暂时不支持仿真交易，自动订阅订单推送。
        :param price: 交易价格。
        :param qty: 交易数量。
        :param strcode: 股票代码。例如：“HK.00700”。
        :param orderside: 交易方向。如下表所示。
        :param ordertype: 交易类型。与港股不同！如下表所示。
        :param envtype: 环境参数，0是真实环境，1是仿真环境
        :param order_deal_push: 是否订阅成交推送
        :return:
            ret_code失败时，ret_data返回为错误描述字符串； 正常情况下，ret_code为0，ret_data为一个dataframe, 其中包括：

                返回字符串	    说明	    返回字符串	说明
                code	        股票ID	stock_name	股票名称
                dealt_avg_price	成交均价	dealt_qty	成交数量
                qty	            订单数量	orderid	    订单ID
                order_type	    交易类型	price	    交易价格
                status	        订单状态(具体状态如下)
                submited_time	提交时间
                updated_time	更新时间
                order_side	交易方向

                status	订单类型	status	订单类型
                0	服务器处理中	1	等待成交
                2	部分成交	    3	全部成交
                4	已失效	    5	下单失败
                6	已撤单	    7	已删除
                8	等待开盘	    21	本地已发送
                22	本地已发送，服务器返回下单失败、没产生订单
                23	本地已发送，等待服务器返回超时

                order_side	交易方向
                0	买入
                1	卖出

                order_type	交易类型
                    1	市价单
                    2	限价
                    51	盘前交易、限价
                    52	盘后交易、限价
            失败情况：

                参数错误
                客户端内部或网络错误
                不满足下单条件

        '''
        ret_code, ret_data = self.ctx.place_order(price, qty, strcode, orderside, ordertype, envtype,
                                                     order_deal_push)
        print(ret_code, ret_data)

    def set_order_status(self,status, orderid=0, envtype=0):
        '''
        功能：更改某指定美股订单状态。美股暂时不支持仿真交易。

        :param status: 美股暂时只支持撤单，status的值只能为0。
        :param orderid: 订单ID。
        :param envtype: 交易环境参数
                    0	真实交易
                    1	仿真交易
        :return:    ret_code失败时，ret_data返回为错误描述字符串； 正常情况下，ret_code为0，ret_data为一个dataframe, 其中包括：

                返回字符串	说明	    返回字符串	说明
                code	    股票ID	stock_name	股票名称
                dealt_avg_price	成交均价
                dealt_qty	成交数量
                qty	        订单数量
                orderid	    订单ID
                order_type	交易类型
                price	    交易价格
                status	    订单状态(具体状态如下)
                submited_time	提交时间
                updated_time	更新时间
                order_side	    交易方向
                status	        订单类型	status	订单类型
                0	服务器处理中	1	等待成交
                2	部分成交	    3	全部成交
                4	已失效	    5	下单失败
                6	已撤单	    7	已删除
                8	等待开盘	    21	本地已发送
                22	本地已发送，服务器返回下单失败、没产生订单
                23	本地已发送，等待服务器返回超时
                order_side	交易方向
                    0	买入
                    1	卖出
                order_type	交易类型
                    1	市价单
                    2	限价
                    51	盘前交易、限价
                    52	盘后交易、限价
        失败情况：
                参数错误
                客户端内部或网络错误
                订单不存在
        '''
        ret_code, ret_data = self.ctx.set_order_status(status, orderid, envtype)
        print(ret_code, ret_data)


    def change_order(self, price, qty, orderid=0, envtype=0):
        '''
        功能：修改某指定美股订单。美股暂时不支持仿真交易。

        :param price: 交易价格。
        :param qty: 交易数量。
        :param orderid: 订单ID。
        :param envtype: 交易环境参数。如下表所示。
            envtype	交易环境参数
                0	真实交易
                1	仿真交易
        :return:ret_code失败时，ret_data返回为错误描述字符串； 正常情况下，ret_code为0，ret_data为一个dataframe, 其中包括：

            envtype: 交易环境参数。0是真实交易，1是仿真交易

            orderid: 订单ID。

        失败情况：

            参数错误
            客户端内部或网络错误
            订单不存在
        '''
        ret_code, ret_data = self.ctx.change_order(price, qty, orderid, envtype)
        print(ret_code, ret_data)


    def accinfo_query(self,envtype=0):
        '''
        功能：查询美股账户信息。美股暂时不支持仿真环境

        :param envtype:交易环境参数。如下表所示。
            envtype	交易环境参数
                0	真实交易
                1	仿真交易
        :return:ret_code失败时，ret_data返回为错误描述字符串； 正常情况下，ret_code为0，ret_data为一个dataframe, 其中包括：

                返回字符串	说明	返回字符串	说明
                Power	购买力	ZCJZ	资产净值
                ZQSZ	证券市值	XJJY	现金结余
                KQXJ	可取现金	DJZJ	冻结资金
                ZSJE	追收金额	ZGJDE	最高借贷额
                YYJDE	已用借贷额	GPBZJ	股票保证金
        失败情况：

                参数错误
                客户端内部或网络错误
        '''
        ret_code, ret_data = self.ctx.accinfo_query(envtype)
        print(ret_code, ret_data)


    def order_list_query(self, orderid="", statusfilter="",  strcode='', start='', end='', envtype=0):
        '''
        功能：查询美股今日订单列表。美股暂时不支持仿真环境。

        :param orderid:指定订单id查询，为空或0为不指定。
        :param statusfilter:状态过滤字符串，默认为空返回全部订单，”,”分隔需要返回的状态，如”1,2,3”返回的是等待成交，部分成交以及全部成交的订单，如下表所示
                    statusfilter	返回订单的状态	statusfilter	返回订单的状态
                    0	服务器处理中	1	等待成交
                    2	部分成交	3	全部成交
                    4	已失效	5	下单失败
                    6	已撤单	7	已删除
                    8	等待开盘	21	本地已发送
                    22	本地已发送，服务器返回下单失败、没产生订单
                    23	本地已发送，等待服务器返回超时
        :param strcode:股票代码过滤，例如”hk.00700”，为空为不限制。
        :param start: 下单时间过滤，格式”hh:mm:ss”, 过滤时间开始点，为空为00:00:00。
        :param end: 下单时间过滤，格式”hh:mm:ss”, 过滤时间结束点，为空为23:59:59。
        :param envtype:交易环境参数。如下表所示。
                envtype	交易环境参数
                0	真实交易
                1	仿真交易
        :return:ret_code失败时，ret_data返回为错误描述字符串； 正常情况下，ret_code为0，ret_data为一个dataframe, 其中包括：

                返回字符串	说明	返回字符串	说明
                code	股票ID	stock_name	股票名称
                dealt_avg_price	成交均价	dealt_qty	成交数量
                qty	订单数量	orderid	订单ID
                order_type	交易类型	price	交易价格
                status	订单状态(具体状态如下)	submited_time	提交时间
                updated_time	更新时间	order_side	交易方向
                status	订单类型	status	订单类型
                    0	服务器处理中	1	等待成交
                    2	部分成交	3	全部成交
                    4	已失效	5	下单失败
                    6	已撤单	7	已删除
                    8	等待开盘	21	本地已发送
                    22	本地已发送，服务器返回下单失败、没产生订单
                    23	本地已发送，等待服务器返回超时
                order_side	交易方向
                    0	买入
                    1	卖出
                order_type	交易类型
                    1	市价单
                    2	限价
                    51	盘前交易、限价
                    52	盘后交易、限价
        失败情况：

                参数错误
                客户端内部或网络错误
        '''
        ret_code, ret_data = self.ctx.order_list_query(orderid, statusfilter, strcode, start, end, envtype)
        print(ret_code, ret_data)

    def position_list_query(self, strcode='', stocktype='', pl_ratio_min='', pl_ratio_max='', envtype=0):
        '''
        功能：查询美股持仓列表。美股暂时不支持仿真环境。

        :param strcode: 股票代码过滤，例如”hk.00700”，为空为不限制。
        :param stocktype: 股票类型
                    正股	“STOCK”
                    指数	“IDX”
                    ETF基金	“ETF”
                    涡轮牛熊	“WARRANT”
                    债券	“BOND”
        :param pl_ratio_min:盈亏比例过滤，“10”表示只返回盈亏比例10%以上（包括10%）的持仓，为空为不限制。
        :param pl_ratio_max: 盈亏比例过滤，“10”表示只返回盈亏比例10%以下（包括10%）的持仓，为空为不限制。
        :param envtype: 交易环境参数。如下表所示。
            envtype	交易环境参数
                0	真实交易
                1	仿真交易
        :return:    ret_code失败时，ret_data返回为错误描述字符串； 正常情况下，ret_code为0，ret_data为一个dataframe, 其中包括：

            返回字符串	说明	    返回字符串	说明
            code	    股票ID	stock_name	股票名称
            qty	        持有数量
            can_sell_qty可卖数量
            cost_price	成本价
            cost_price_valid	成本价是否有效(非0有效)
            market_val	市值
            nominal_price	市价
            pl_ratio	盈亏比例
            pl_ratio_valid	盈亏比例是否有效(非0有效)
            pl_val	盈亏金额
            pl_val_valid	盈亏金额是否有效(非0有效)
            today_buy_qty	今日买入数量
            today_buy_val	今日买入金额
            today_pl_val	今日盈亏金额
            today_sell_qty	今日卖出数量
            today_sell_val	今日卖出金额
        失败情况：

            参数错误
            客户端内部或网络错误
        '''
        ret_code, ret_data = self.ctx.position_list_query(strcode, stocktype, pl_ratio_min, pl_ratio_max, envtype)
        print(ret_code, ret_data)

    def deal_list_query(self, envtype=0):
        '''
        功能：查询美股今日成交列表。美股暂时不支持仿真环境。
        :param envtype: 交易环境参数。如下表所示。
            envtype	交易环境参数
                0	真实交易
                1	仿真交易
        :return: ret_code失败时，ret_data返回为错误描述字符串； 正常情况下，ret_code为0，ret_data为一个dataframe, 其中包括：

                code: 股票代码。

                stock_name: 股票名称。

                dealid: 成交ID。

                orderid: 订单ID。

                price: 交易价格。

                qty: 交易数量。

                orderside: 交易方向，0表示买入，1表示卖出。

                time: 成交时间。

        失败情况：

                参数错误
                客户端内部或网络错误
        '''
        ret_code, ret_data = self.ctx.deal_list_query(envtype)
        print(ret_code, ret_data)


    def history_order_list_query(self,statusfilter='', strcode='', start='', end='', envtype=0):
        '''
        功能：查询历史订单列表, 30秒内不能超过5次交易请求, 时间段最多90自然日。

        :param statusfilter: 状态过滤字符串，为空返回全部订单，”,”分隔需要返回的状态，如”1,2,3”返回的是等待成交，部分成交以及全部成交的订单，状态如下表所示
            statusfilter	返回订单的状态	statusfilter	返回订单的状态
            0	服务器处理中	1	等待成交
            2	部分成交    	3	全部成交
            4	已失效	    5	下单失败
            6	已撤单	    7	已删除
            8	等待开盘	    21	本地已发送
            22	本地已发送，服务器返回下单失败、没产生订单
            23	本地已发送，等待服务器返回超时
        :param strcode: 股票代码过滤，例如”hk.00700”，为空为不限制。
        :param start: 历史订单查询起始时间，格式”yy-mm-dd”。
        :param end: 历史订单查询截止时间，格式”yy-mm-dd”。 起止时间参数组合如下表所示：
                start	end	查询时间段
                空	非空	end前90天
                非空	空	start后90天
                空	空	90天前至当天
        :param envtype: 交易环境参数。如下表所示。
            envtype	交易环境参数
                0	真实交易
                1	仿真交易
        :return:
            ret_code失败时，ret_data返回为错误描述字符串； 正常情况下，ret_code为0，ret_data为一个dataframe, 其中包括：

            返回字符串	说明	返回字符串	说明
                code	股票ID	stock_name	股票名称
                orderid | 订单ID	dealt_qty	成交数量
                order_type	交易类型	price	交易价格
                status	订单状态(具体状态如下)	submited_time	提交时间
                updated_time	更新时间	order_side	交易方向
                qty	订单数量
            status	订单类型	status	订单类型
            0	服务器处理中	1	等待成交
            2	部分成交	    3	全部成交
            4	已失效	    5	下单失败
            6	已撤单	    7	已删除
            8	等待开盘	    21	本地已发送
            22	本地已发送，服务器返回下单失败、没产生订单
            23	本地已发送，等待服务器返回超时
            order_side	交易方向
                0	买入
                1	卖出
            order_type	交易类型
                1	市价单
                2	限价
                51	盘前交易、限价
                52	盘后交易、限价
        失败情况：

            参数错误
            客户端内部或网络错误
        '''
        ret_code, ret_data = self.ctx.history_order_list_query(statusfilter, strcode, start, end, envtype)
        print(ret_code, ret_data)

    def history_deal_list_query(self, strcode='', start='', end='', envtype=0):
        '''
        功能：查询历史订单列表, 30秒内不能超过5次请求, 时间段最多90自然日。

        :param strcode: 股票代码过滤，例如”hk.00700”，为空为不限制。
        :param start: 历史订单查询其实时间，格式”yy-mm-dd”, 为空则为end字段前90天。
        :param end:  历史订单查询其实时间，格式”yy-mm-dd”, 为空则为start字段后90天，若start为空，则end为当天。
        :param envtype: 交易环境参数。如下表所示。
            envtype	交易环境参数
                0	真实交易
                1	仿真交易
        :return: ret_code失败时，ret_data返回为错误描述字符串； 正常情况下，ret_code为0，ret_data为一个dataframe, 其中包括：

            code: 股票代码。

            stock_name: 股票名称。

            dealid: 成交ID。

            orderid: 订单ID。

            price: 交易价格。

            qty: 交易数量。

            order_side: 交易方向，0表示买入，1表示卖出。

            time: 成交时间。

        失败情况：

            参数错误
            客户端内部或网络错误
        '''
        ret_code, ret_data = self.ctx.history_deal_list_query(strcode, start, end, envtype)
        print(ret_code, ret_data)

    def subscribe_order_deal_push(self, order_list, order_deal_push=True, envtype=0):
        '''
        功能：订阅订单成交推送。

        :param order_list: 订阅的订单ID，多个或单个，列表或字符串（字符串用英文逗号分割），单独传空表示订阅全部订单，包括后来新增的。
        :param order_deal_push: 是否订阅成交推送。
        :param envtype: 交易环境参数
                0	真实交易
                1	仿真交易
        :return: ret_code失败时，ret_data返回为错误描述字符串； 正常情况下，ret_code为0。

        失败情况：
            参数错误
            客户端内部或网络错误
        '''
        ret_code = self.ctx.subscribe_order_deal_push(order_list, order_deal_push, envtype)
        print(ret_code)
