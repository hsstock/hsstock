# -*- coding: UTF-8 -*-

from abc import ABC, abstractclassmethod
from hsstock.futuquant import *
from hsstock.service.quote_service import *
from hsstock.utils.decorator import *
from hsstock.common.constant import *

class Trade(ABC):
    def __init__(self,trade_ctx):
        self.ctx = trade_ctx
        self.storeservice = MysqlService()

    def get_acc_list(self):
        '''
        功能：
            获取交易业务账户列表。要调用交易接口前，必须先获取此列表，后续交易接口根据不同市场传入不同的交易业务账户ID，传0默认第一个账户

        :return(ret_code,ret_data:
            ret_code为RET_OK时，ret_data为DataFrame数据，否则为错误原因字符串，DataFrame数据如下

        参数	    类型	说明
        acc_id	int	交易业务账户
        trd_env	str	交易环境，TrdEnv.REAL(真实环境)或TrdEnv.SIMULATE(仿真环境)
        '''
        ret_code, ret_data = self.ctx.get_acc_list()
        if ret_code is True:
            table = 'ft_acc'
            self.storeservice.insert_many(table, ret_data, 'append')
        return ret_code, ret_data

    @rate_limit(FREQ.UNLOCK_TRADE)
    def unlock_trade(self, password=None, password_md5=None,is_unlock=True):
        '''
        功能：解锁交易

        Parameters:
            password – str，交易密码，如果password_md5不为空就使用传入的password_md5解锁，否则使用password转MD5得到password_md5再解锁
            password_md5 – str，交易密码的MD5转16进制字符串(全小写)，解锁交易必须要填密码，锁定交易忽略
            is_unlock – bool，解锁或锁定，True解锁，False锁定
        Return(ret_code, ret_data):
            ret == RET_OK时, data为None，如果之前已经解锁过了，data为提示字符串，指示出已经解锁
            ret != RET_OK时， data为错误字符串
        '''

        ret_code, ret_data = self.ctx.unlock_trade(password, password_md5)
        return ret_code, ret_data

    def accinfo_query(self,trd_env=TrdEnv.REAL,acc_id = 0 ):
        '''
        功能：获取账户资金数据。获取账户的资产净值、证券市值、现金、购买力等资金数据。

        :param
            trd_env – str，交易环境 TrdEnv ，TrdEnv.REAL(真实环境)或TrdEnv.SIMULATE(仿真环境)
            acc_id – int，交易业务账户ID，传0默认第一个账户
        :return(ret_code,ret_data):
            ret_code为RET_OK时，ret_data为DataFrame数据，否则为错误原因字符串，DataFrame数据如下：

                参数	            类型	    说明
                power	        float	购买力，即可使用用于买入的资金
                total_assets	float	资产净值
                cash	        float	现金
                market_val	    float	证券市值
                frozen_cash	    float	冻结金额
                avl_withdrawal_cash	float	可提金额
        '''
        ret_code, ret_data = self.ctx.accinfo_query(trd_env,acc_id)
        if ret_code is True:
            table = 'ft_accinfo'
            self.storeservice.insert_many(table, ret_data, 'append')
        return ret_code, ret_data

    def position_list_query(self, code='', pl_ratio_min=None, pl_ratio_max=None, trd_env=TrdEnv.REAL, acc_id=0):
        '''
        功能：
            获取账户持仓列表。获取账户的证券持仓列表。
        :param code: str，代码过滤，只返回包含这个代码的数据，没传不过滤，返回所有
        :param pl_ratio_min:  float，过滤盈亏比例下限，高于此比例的会返回，如0.1，返回盈亏比例大于10%的持仓
        :param pl_ratio_max: float，过滤盈亏比例上限，低于此比例的会返回，如0.2，返回盈亏比例小于20%的持仓
        :param trd_env:  str，交易环境，TrdEnv.REAL(真实环境)或TrdEnv.SIMULATE(仿真环境)
        :param acc_id:  int，交易业务账户ID，传0默认第一个账户
        Return(ret_code, ret_data):
            ret_code为RET_OK时，ret_data为DataFrame数据，否则为错误原因字符串，DataFrame数据如下：
            参数	            类型	说明
            position_side	str	持仓方向，PositionSide.LONG(多仓)或PositionSide.SHORT(空仓)
            code	        str	代码
            stock_name	    str	名称
            qty	            float	持有数量，2位精度，期权单位是”张”，下同
            can_sell_qty	float	可卖数量
            nominal_price	float	市价，3位精度(A股2位)
            cost_price	    float	成本价，无精度限制
            cost_price_valid	bool	成本价是否有效，True有效，False无效
            market_val	    float	市值，3位精度(A股2位)
            pl_ratio	    float	盈亏比例，无精度限制
            pl_ratio_valid	bool	盈亏比例是否有效，True有效，False无效
            pl_val	        float	盈亏金额，3位精度(A股2位)
            pl_val_valid	bool	盈亏金额是否有效，True有效，False无效
            today_pl_val	float	今日盈亏金额，3位精度(A股2位)，下同
            today_buy_qty	float	今日买入总量
            today_buy_val	float	今日买入总额
            today_sell_qty	float	今日卖出总量
            today_sell_val	float	今日卖出总额
        '''
        ret_code, ret_data = self.ctx.position_list_query(code, pl_ratio_min, pl_ratio_max, trd_env, acc_id)
        if ret_code is True:
            table = 'ft_position'
            self.storeservice.insert_many(table, ret_data, 'append')
        return ret_code, ret_data

    @rate_limit(FREQ.PLACE_ORDER)
    def place_order(self, price, qty, code, trd_side=TrdSide.NONE, order_type=OrderType.NORMAL, adjust_limit=0, trd_env=TrdEnv.SIMULATE, acc_id=0):
        '''
        功能：下单交易

        :param price: float，订单价格，3位精度(A股2位)，当订单是市价单或竞价单类型，忽略该参数传值
        :param qty:  float，订单数量，2位精度，期权单位是”张”
        :param code:  str，代码
        :param trd_side:  str，交易方向，参考TrdSide类的定义
        :param order_type: str，订单类型，参考OrderType类的定义
        :param adjust_limit: float，港股有价位表，订单价格必须在规定的价位上，OpenD会对传入价格自动调整到合法价位上，此参数指定价格调整方向和调整幅度百分比限制，正数代表向上调整，负数代表向下调整，具体值代表调整幅度限制，如：0.015代表向上调整且幅度不超过1.5%；-0.01代表向下调整且幅度不超过1%
        :param trd_env: – str，交易环境，TrdEnv.REAL(真实环境)或TrdEnv.SIMULATE(仿真环境)
        :param acc_id: – int，交易业务账户ID，传0默认第一个账户

        Return(ret_code, ret_data):
            ret_code为RET_OK时，ret_data为DataFrame数据，否则为错误原因字符串，DataFrame数据跟下面的 order-list-query (获取订单列表)相同
        '''
        ret_code, ret_data = self.ctx.place_order(price, qty, code, trd_side, order_type, adjust_limit,trd_env,acc_id)
        return ret_code, ret_data

    def order_list_query(self, order_id="", status_filter_list=[],  code='', start='', end='', trd_env=TrdEnv.REAL,acc_id=0):
        '''
        功能：
            获取订单列表。获取账户的交易订单列表。

        :param order_id: – str，订单号过滤，只返回此订单号的数据，没传不过滤，返回所有
        :param status_filter_list: – str数组，订单状态过滤，只返回这些状态的订单数据，没传不过滤，返回所有，参考 OrderStatus 类的定义
        :param code: – str，代码过滤，只返回包含这个代码的数据，没传不过滤，返回所有
        :param start: – str，开始时间，严格按YYYY-MM-DD HH:MM:SS或YYYY-MM-DD HH:MM:SS.MS格式传
        :param end:  – str，结束时间，严格按YYYY-MM-DD HH:MM:SS或YYYY-MM-DD HH:MM:SS.MS格式传
        :param trd_env: – str，交易环境，TrdEnv.REAL(真实环境)或TrdEnv.SIMULATE(仿真环境)
        :param acc_id: – int，交易业务账户ID，传0默认第一个账户
        Return(ret_code, ret_data):
            ret_code为RET_OK时，ret_data为DataFrame数据，否则为错误原因字符串，DataFrame数据如下：

            参数      	类型	说明
            trd_side	str	交易方向，参考 TrdSide 类的定义
            order_type	str	订单类型，参考 OrderType 类的定义
            order_status	str	订单状态，参考 OrderStatus 类的定义
            order_id	str	订单号
            code	    str	代码
            stock_name	str	名称
            qty	        float	订单数量，2位精度，期权单位是”张”
            price	    float	订单价格，3位精度(A股2位)
            create_time	str	创建时间，严格按YYYY-MM-DD HH:MM:SS或YYYY-MM-DD HH:MM:SS.MS格式传
            updated_time	str	最后更新时间，严格按YYYY-MM-DD HH:MM:SS或YYYY-MM-DD HH:MM:SS.MS格式传
            dealt_qty	float	成交数量，2位精度，期权单位是”张”
            dealt_avg_price	float	成交均价，无精度限制
            last_err_msg	str	最后的错误描述，如果有错误，会有此描述最后一次错误的原因，无错误为
        '''


        ret_code, ret_data = self.ctx.order_list_query(order_id, status_filter_list, code, start, end, trd_env,acc_id)
        if ret_code is True:
            table = 'ft_orders'
            self.storeservice.insert_many(table, ret_data, 'append')
        return ret_code, ret_data

    @rate_limit(FREQ.MODIFY_ORDER)
    def modify_order(self, modify_order_op, order_id, qty, price, adjust_limit=0, trd_env=TrdEnv.REAL, acc_id=0):
        '''
        功能：
            修改订单。修改订单，包括修改订单的价格和数量(即以前的改单)、撤单、失效、生效、删除等
        :param modify_order_op: – str，改单操作类型，参考 ModifyOrderOp_ 类的定义
        :param order_id: – str，订单号
        :param qty: – float，(改单有效)新的订单数量，2位精度，期权单位是”张”
        :param price: – float，(改单有效)新的订单价格，3位精度(A股2位)
        :param adjust_limit: – folat，(改单有效)港股有价位表，订单价格必须在规定的价位上，OpenD会对传入价格自动调整到合法价位上，此参数指定价格调整方向和调整幅度百分比限制，正数代表向上调整，负数代表向下调整，具体值代表调整幅度限制，如：0.015代表向上调整且幅度不超过1.5%；-0.01代表向下调整且幅度不超过1%
        :param trd_env: – str，交易环境 TrdEnv ，TrdEnv.REAL(真实环境)或TrdEnv.SIMULATE(仿真环境)
        :param acc_id: – int，交易业务账户ID，传0默认第一个账户
        Return(ret_code, ret_data):
            ret_code为RET_OK时，ret_data为DataFrame数据，否则为错误原因字符串，DataFrame数据如下：

            参数	        类型	    说明
            trd_env	    str	    交易环境 TrdEnv ，TrdEnv.REAL(真实环境)或TrdEnv.SIMULATE(仿真环境)
            order_id    str	    订单号
        '''
        ret_code, ret_data = self.ctx.modify_order(modify_order_op, order_id, qty, price, adjust_limit, trd_env, acc_id)
        return ret_code, ret_data

    def deal_list_query(self, code="", trd_env=TrdEnv.REAL, acc_id=0):
        '''
        功能：
            获取成交列表。获取账户的交易成交列表。
        :param code: – str，代码过滤，只返回包含这个代码的数据，没传不过滤，返回所有
        :param trd_env: – str，交易环境 TrdEnv ，TrdEnv.REAL(真实环境)或TrdEnv.SIMULATE(仿真环境)
        :param acc_id:  – int，交易业务账户ID，传0默认第一个账户
        Return(ret_code, ret_data):
            ret_code为RET_OK时，ret_data为DataFrame数据，否则为错误原因字符串，DataFrame数据如下：

            参数	        类型	说明
            trd_side	str	交易方向，参考 TrdSide 类的定义
            deal_id 	str	成交号
            order_id	str	订单号
            code	    str	代码
            stock_name	str	名称
            qty	        float	成交数量，2位精度，期权单位是”张”
            price	    float	成交价格，3位精度(A股2位)
            create_time	str	创建时间，严格按YYYY-MM-DD HH:MM:SS或YYYY-MM-DD HH:MM:SS.MS格式传
            counter_broker_id	int	对手经纪号，港股有效
            counter_broker_name	str	对手经纪名称，港股有效

            ['trd_env', 'code', 'stock_name', 'deal_id', 'order_id',
                        'qty', 'price', 'trd_side', 'create_time', 'counter_broker_id',
                        'counter_broker_name', 'trd_market',
                        ]
        '''
        ret_code, ret_data = self.ctx.deal_list_query(code,trd_env,acc_id)
        if ret_code is True:
            table = 'ft_deals'
            self.storeservice.insert_many(table, ret_data, 'append')
        return ret_code, ret_data

    @rate_limit(FREQ.HISTORY_ORDER_LIST_QUERY)
    def history_order_list_query(self,status_filter_list=[], code='', start='', end='', trd_env=TrdEnv.REAL, acc_id=0):
        '''
        功能：
            获取历史订单列表。获取账户的历史交易订单列表。

        :param status_filter_list: – str数组，订单状态过滤，只返回这些状态的订单数据，没传不过滤，返回所有，参考OrderStatus类的定义
        :param code: – str，代码过滤，只返回包含这个代码的数据，没传不过滤，返回所有
        :param start: - str，开始时间，严格按YYYY-MM-DD HH:MM:SS或YYYY-MM-DD HH:MM:SS.MS格式传
        :param end: – str，结束时间，严格按YYYY-MM-DD HH:MM:SS或YYYY-MM-DD HH:MM:SS.MS格式传
        :param trd_env: – str，交易环境 TrdEnv ，TrdEnv.REAL(真实环境)或TrdEnv.SIMULATE(仿真环境)
        :param acc_id: – int，交易业务账户ID，传0默认第一个账户
        Return(ret_code, ret_data):
            ret_code为RET_OK时，ret_data为DataFrame数据，否则为错误原因字符串，DataFrame数据跟上面的 order-list-query (获取订单列表)相同
        '''
        ret_code, ret_data = self.ctx.history_order_list_query(status_filter_list, code, start, end, trd_env, acc_id)
        if ret_code is True:
            table = 'ft_history_orders'
            self.storeservice.insert_many(table, ret_data, 'append')
        return ret_code, ret_data

    @rate_limit(FREQ.HISTORY_DEAL_LIST_QUERY)
    def history_deal_list_query(self, code='', start='', end='', trd_env=TrdEnv.REAL,acc_id=0):
        '''
        功能：获取历史成交列表。获取账户的历史交易成交列表。
        :param code: str，代码过滤，只返回包含这个代码的数据，没传不过滤，返回所有
        :param start: str，开始时间，严格按YYYY-MM-DD HH:MM:SS或YYYY-MM-DD HH:MM:SS.MS格式传
        :param end: str，结束时间，严格按YYYY-MM-DD HH:MM:SS或YYYY-MM-DD HH:MM:SS.MS格式传
        :param trd_env:  str，交易环境 TrdEnv ，TrdEnv.REAL(真实环境)或TrdEnv.SIMULATE(仿真环境)
        :param acc_id:  int，交易业务账户ID，传0默认第一个账户
        :return: ret_code为RET_OK时，ret_data为DataFrame数据，否则为错误原因字符串，DataFrame数据跟上面的 deal-list-query (获取成交列表)相同。
        '''
        ret_code, ret_data = self.ctx.history_deal_list_query(code, start, end, trd_env, acc_id)
        if ret_code is True:
            table = 'ft_history_deals'
            self.storeservice.insert_many(table, ret_data, 'append')
        return ret_code, ret_data

class HSTradeDeal(TradeDealHandlerBase):
    '''
    deal update push
    '''
    def on_recv_rsp(self, rsp_pb):
        '''
        响应成交推送。OpenD会主动推送新的成交数据过来，需要客户端响应处理

        :param rsp_pb:  – class，成交推送协议pb对象
        :Return(ret_code, ret_data):
 	        ret_code为RET_OK时，ret_data为DataFrame数据，否则为错误原因字符串，DataFrame数据跟上面的 deal-list-query (获取成交列表)相同
        '''
        ret, content =  super(HSTradeDeal,self).on_recv_rsp(rsp_pb)

        if ret == RET_OK:
            print("HSTradeDeal content={}".format(content))

            if len(content) > 0:
                table = 'ft_trade_deal'
                self.storeservice.insert_many(table, content, 'append')

        return ret, content

class HSTradeOrder(TradeOrderHandlerBase):
    '''
    order update push
    '''
    def on_recv_rsp(self,rsp_pb):
        ret, content = super(HSTradeOrder,self).on_recv_rsp(rsp_pb)

        if ret == RET_OK:
            print('*HSTradeOrder content={}'.format(content))

            if len(content) > 0:
                table = 'ft_trade_order'
                self.storeservice.insert_many(table, content, 'append')
        return ret, content