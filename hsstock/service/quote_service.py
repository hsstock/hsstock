# -*- coding: UTF-8 -*-

from abc import ABC
from hsstock.futuquant import *

from hsstock.model.subscribe import SubItem
from hsstock.utils.decorator import *
from hsstock.common.constant import *
from hsstock.service.mysql_service import MysqlService


'''
行情API
接口概要
开放接口基于PC客户端获取数据，提供给用户使用。

开放接口分为低频接口、订阅接口和高频接口，以及回get_trading_days调处理基类：

低频接口主要用来获取股票市场静态和全局的数据，让用户得到股票的基本信息，不允许高频调用。

如果要实时获取数据，则需要调用高频接口。

订阅接口是用来管理高频接口使用额度，包括订阅、退订和查询额度。

订阅：在使用高频接口前， 需要订阅想要的数据。订阅成功后，则可以使用高频接口获取；订阅各类数据有额度限制：

用户额度 >= 订阅K线股票数 * K线权重 + 订阅逐笔股票数 * 逐笔权重 + 订阅报价股票数 * 报价权重 + 订阅摆盘股票数 * 摆盘权重

订阅使用的额度不能超过用户额度，用户额度也就是订阅的上限为500个订阅单位

订阅数据	额度权重（所占订阅单位）
K线	2
逐笔	5（牛熊证为1）
报价	1
摆盘	5（牛熊证为1）
分时	2
经纪队列	5（牛熊证为1）
查询额度：用来查询现在各项额度占用情况。用户可以看到每一种类型数据都有订阅了哪些股票；然后利用退订操作来去掉不需要的股票数据。

退订：用户可以退订指定股票和指定数据类型，空出额度。但是退订的时间限制为1分钟，即订阅某支股票某个订阅位1分钟之后才能退订。

如果数据不订阅，直接调用高频接口则会返回失败。 订阅时可选择推送选项。推送开启后，程序就会持续收到客户端推送过来的行情数据。用户可以通过继承回调处理基类，并实现用户自己的子类来使用数据推送功能。

高频接口可以获取实时数据，可以针对小范围内的股票频繁调用；比如需要跟踪某个股票的逐笔和摆盘变化等；在调用之前需要将频繁获取的数据订阅注册。

回调处理基类用于实现数据推送功能，用户在此基类上实现子类并实例化后，当客户端不断推送数据时，程序就会调用对应的对象处理。

'''
class LF(object):
    def __init__(self,quote_ctx):
        self.ctx = quote_ctx
        self.storeservice = MysqlService()

    def is_holiday(self,market,date):
        '''
                判断是否为交易日，返回True or False
        '''
        ret_code, ret_data = self.get_trading_days(market)
        if ret_code == RET_ERROR:
            print(ret_data)
            exit()

        return date not in ret_data

    def get_trading_days(self, market, start_date=None, end_date=None):
        '''
        功能：
            获取交易日

        Parameters:
            market – 市场类型，futuquant.common.constsnt.Market
            start_date – 起始日期
            end_date – 结束日期
        Returns:
            成功时返回(RET_OK, data)，data是字符串数组；失败时返回(RET_ERROR, data)，其中data是错误描述字符串
        '''

        ret_code, ret_data = self.ctx.get_trading_days(market=market)
        if ret_code == RET_ERROR:
            print(ret_data)
            exit()
        # print("TRADING DAYS")
        # for x in ret_data:
        #     print(x)

        return ret_code, ret_data

    def get_stock_basicinfo(self, market, stock_type=SecurityType.STOCK):
        '''
        功能：
            获取指定市场中特定类型的股票基本信息

        Parameters:
            market – 市场类型，futuquant.common.constsnt.Market
            stock_type – 股票类型， futuquant.common.constsnt.SecurityType
        Returns:
            (ret_code, content)
            ret_code 等于RET_OK时， content为Pandas.DataFrame数据, 否则为错误原因字符串, 数据列格式如下
            参数	    类型	说明
            code	str	股票代码
            name	str	名字
            lot_size	int	每手数量
            stock_type	str	股票类型，参见SecurityType
            stock_child_type	str	涡轮子类型，参见WrtType
            stock_owner	str	正股代码
            listing_date	str	上市时间
            stock_id	    int	股票id
        '''
        ret_code, ret_data = self.ctx.get_stock_basicinfo(market, stock_type)
        if ret_code == RET_ERROR:
            print(ret_data)
            exit()
        table = 'ft_stock_basicinfo'
        self.storeservice.insert_many(table, ret_data, 'append')
        return ret_code, ret_data

    def get_multiple_history_kline(self, codelist=[], start=None, end=None, ktype=KLType.K_DAY, autype=AuType.QFQ):
        """
        功能：
            获取多只股票的历史k线数据
        Parameters:
            codelist – 股票代码列表，list或str。例如：[‘HK.00700’, ‘HK.00001’]，’HK.00700,SZ.399001’
            start – 起始时间
            end – 结束时间
            ktype – k线类型，参见KLType
            autype – 复权类型，参见AuType
        Returns:
            成功时返回(RET_OK, [data])，data是DataFrame数据, 数据列格式如下

            参数	        类型	说明
            code	    str	股票代码
            time_key	str	k线时间
            open	    float	开盘价
            close	    float	收盘价
            high	    float	最高价
            low	float	最低价
            pe_ratio	float	市盈率
            turnover_rate	float	换手率
            volume	    int	成交量
            turnover	float	成交额
            change_rate	float	涨跌幅
            last_close	float	昨收价
            失败时返回(RET_ERROR, data)，其中data是错误描述字符串
        """
        ret_code, ret_data = self.ctx.get_multiple_history_kline(codelist,start, end,  ktype, autype)
        print(ret_data)
        if ret_code == RET_ERROR:
            print(ret_data)
            #exit()
        # print(ret_data)
        table = 'ft_history_kline'
        for item in ret_data:
            self.storeservice.insert_many(table, item, 'append')
        return ret_code, ret_data

    def get_history_kline(self, code, start=None, end=None, ktype=KLType.K_DAY, autype=AuType.QFQ,fields=KL_FIELD.ALL):
        ''' 获取历史K线

        :param code: 股票代码
        :param start: 开始时间，string; YYYY-MM-DD；为空时取去当前时间;
        :param end: 结束时间，string; YYYY-MM-DD；为空时取当前时间;
        :param ktype: k线类型，默认为日K
        :param autype: 复权类型，string；”qfq”-前复权，”hfq”-后复权，None-不复权，默认为”qfq”
                fields: 单个或多个K线字段类型，指定需要返回的数据 KL_FIELD.ALL or [KL_FIELD.DATE_TIME, KL_FIELD.OPEN]，默认为KL_FIELD.ALL
                开始结束时间按照闭区间查询，时间查询以k线时间time_key作为比较标准。即满足 start<=Time_key<=end条件的k线作为返回内容，k线时间time_key的设定标准在返回值中说明
        :return:
            ret_code失败时，ret_data返回为错误描述字符串； 客户端无符合条件数据时，ret_code为成功，返回None；
            正常情况下返回K线数据为一个DataFrame包含:

            code： 股票代码；string

            time_key： K线时间 string “YYYY-MM-DD HH:mm:ss”

            open： 开盘价；double

            high： 最高价；double

            close： 收盘价；double

            low： 最低价；double

            pe_ratio： 市盈率；double

            turnover_rate: 换手率；double

            volume： 成交量；long

            turnover ： 成交额；double

            change_rate: 涨跌幅；double

            last_close	float	昨收价

            对于日K线，time_key为当日时间具体到日，比如说2016-12-23日的日K，K线时间为”2016-12-23 00:00:00”

            对于周K线，12月19日到12月25日的周K线，K线时间time_key为” 2016-12-19 00:00:00”

            对于月K线，12月的月K线时间time_key为” 2016-12-01 00:00:00”，即为当月1日时间

            对于分K线，time_key为当日时间具体到分，例如，

            分K类型	覆盖时间举例
            1分K	覆盖9:35:00到9:35:59的分K,time_key为”2016-12-23 09:36:00”
            5分K	覆盖10:05:00到10:09:59的分K,time_key为”2016-12-23 10:10:00”
            15分K	覆盖10:00:00到10:14:59的分K,time_key为”2016-12-23 10:15:00”
            30分K	覆盖10:00:00到10:29:59的分K,time_key为”2016-12-23 10:30:00”
            60分K	覆盖10:00:00到10:59:59的分K,time_key为”2016-12-23 11:00:00”
        失败情况:
            股票代码不合法
            PLS接口返回错误

            US.AAPL返回为空，需要订阅吗？
        '''
        ret_code, ret_data = self.ctx.get_history_kline(code,start,end,ktype,autype,fields)
        if ret_code == RET_ERROR:
            print(ret_data)
            #exit()
        #print(ret_data)
        if ktype == KLType.K_DAY:
            table = 'ft_history_kline'
        else:
            table = 'ft_history_kline_' + ktype
        if not isinstance(ret_data,str):
            if len(ret_data) > 0 :
                self.storeservice.insert_many(table, ret_data, 'append')
        return ret_code, ret_data

    def get_autype_list(self, code_list):
        '''获取复权因子
        
        :param code_list: 股票代码列表，例如，HK.00700，US.AAPL
        :return: ret_code失败时，ret_data返回为错误描述字符串； 客户端无符合条件数据时，ret_code为成功，ret_data返回None； 正常情况下，ret_data为一个dataframe，其中包括：
                code：股票代码；string，例如： ”HK.00700”，“US.AAPL”
                ex_div_date：除权除息日；string，格式YYYY-MM-DD
                split_ratio：拆合股比例； double，例如，对于5股合1股为1/5，对于1股拆5股为5/1
                per_cash_div：每股派现；double
                per_share_div_ratio：每股送股比例； double
                per_share_trans_ratio：每股转增股比例； double
                allotment_ratio：每股配股比例；double
                allotment_price：配股价；double
                stk_spo_ratio：增发比例；double
                stk_spo_price ：增发价格；double
                forward_adj_factorA：前复权因子A；double
                forward_adj_factorB：前复权因子B；double
                backward_adj_factorA：后复权因子A；double
                backward_adj_factorB：后复权因子B；double

                返回数据中不一定包含所有codelist中的代码，调用方自己需要检查，哪些股票代码是没有返回复权数据的，未返回复权数据的股票说明没有找到相关信息。

                复权价格 = 复权因子A * 价格 + 复权因子B

            失败情况：
                1． Codelist中股票代码不合法
                2． 客户端内部或网络错误
        '''
        ret_code, ret_data = self.ctx.get_autype_list(code_list)
        if ret_code == RET_ERROR:
            print(ret_data)
            #exit()
        #print(ret_data)
        table = 'ft_autype'
        self.storeservice.insert_many(table, ret_data, 'append')
        return ret_code, ret_data

    @rate_limit(FREQ.GET_MARKET_SNAPSHOT)
    def get_market_snapshot(self, code_list):
        '''
        功能：获取市场快照

        :param code_list: 股票列表，限制最多200只股票
        :return:    ret_code失败时，ret_data返回为错误描述字符串； 客户端无符合条件数据时，ret_code为成功，ret_data返回None； 正常情况下，ret_data为一个dataframe，其中包括：

            code ：股票代码；string

            update_time： 更新时间(yyyy-MM-dd HH:mm:ss)；string

            last_price ： 最新价格；float

            open_price： 今日开盘价；float

            high_price： 最高价格；float

            low_price： 最低价格；float

            prev_close_price： 昨收盘价格；float

            volume： 成交数量； long

            turnover： 成交金额；float

            turnover_rate： 换手率；float

            suspension： 是否停牌(True表示停牌)；bool

            listing_date ： 上市日期 (yyyy-MM-dd)；string

            circular_market_val： 流通市值；float

            total_market_val: 总市值；float

            wrt_valid： 是否是窝轮；bool

            wrt_conversion_ratio: 换股比率；float

            wrt_type： 窝轮类型；1=认购证 2=认沽证 3=牛证 4=熊证 string

            wrt_strike_price： 行使价格；float

            wrt_maturity_date: 格式化窝轮到期时间； string

            wrt_end_trade: 格式化窝轮最后交易时间；string

            wrt_code: 窝轮对应的正股；string

            wrt_recovery_price: 窝轮回收价；float

            wrt_street_vol: 窝轮街货量；float

            wrt_issue_vol: 窝轮发行量；float

            wrt_street_ratio: 窝轮街货占比；float

            wrt_delta: 窝轮对冲值；float

            wrt_implied_volatility: 窝轮引伸波幅；float

            wrt_premium: 窝轮溢价；float

            lot_size：每手股数；int

            issued_Shares：发行股本；int

            net_asset：资产净值；int

            net_profit：净利润；int

            earning_per_share： 每股盈利；float

            outstanding_shares：流通股本；int

            net_asset_per_share：每股净资产；float

            ey_ratio：收益率；float

            pe_ratio：市盈率；float

            pb_ratio：市净率；float

            price_spread ： 当前摆盘价差亦即摆盘数据的买档或卖档的相邻档位的报价差；float

            返回DataFrame，包含上述字段

            窝轮类型 wrt_type，（字符串类型）：

            窝轮类型	标识
            “CALL”	认购证
            “PUT”	认沽证
            “BULL”	牛证
            “BEAR”	熊证
            “N/A”	未知或服务器没相关数据
            返回数据量不一定与codelist长度相等， 用户需要自己判断

            调用频率限制： 5s一次

            失败情况:

            Codelist中股票代码不合法
            Codelist长度超过规定数量
            客户端内部或网络错误
        '''
        ret_code, ret_data = self.ctx.get_market_snapshot(code_list)
        if ret_code == RET_ERROR:
            print(ret_data)
            exit()
        #print(ret_data)
        table = 'ft_market_snapshot'
        self.storeservice.insert_many(table, ret_data, 'append')
        return ret_code, ret_data

    @rate_limit(FREQ.GET_PLATE_STOCK)
    def get_plate_stock(self, plate_code):
        '''
        功能：
            获取板块下的股票列表

        :param plate_code: 板块代码, string, 例如，”SH.BK0001”，”SH.BK0002”，先利用获取子版块列表函数获取子版块代码
        :return: ret == RET_OK 返回pd dataframe数据，data.DataFrame数据, 数据列格式如下

                ret != RET_OK 返回错误字符串

                参数	    类型	说明
                code	str	股票代码
                lot_size	int	每手股数
                stock_name	str	股票名称
                stock_owner	str	所属正股的代码
                stock_child_type	str	股票子类型，参见WrtType
                stock_type	str	股票类型，参见SecurityType
                list_time	str	上市时间
                stock_id	int	股票id
        '''
        ret_code, ret_data = self.ctx.get_plate_stock(plate_code)
        if ret_code == RET_ERROR:
            print(ret_data)
            exit()
        # print(ret_data)
        table = 'ft_plate_stock'
        self.storeservice.insert_many(table, ret_data, 'append')
        return ret_code, ret_data

    @rate_limit(FREQ.GET_PLATE_LIST)
    def get_plate_list(self, market, plate_class=Plate.ALL):
        '''
        功能： 获取板块集合下的子板块列表

        :param market:  市场标识，注意这里不区分沪，深,输入沪或者深都会返回沪深市场的子板块（这个是和客户端保持一致的）
        :param plate_class: 板块分类, string; 例如，”ALL”, “INDUSTRY”

                    板块分类类型 ，（字符串类型）：

                    板块分类	标识
                    “ALL”	所有板块
                    “INDUSTRY”	行业分类
                    “REGION”	地域分类
                    “CONCEPT”	概念分类
        :return:
                ret == RET_OK 返回pd Dataframe数据，数据列格式如下
                ret != RET_OK 返回错误字符串
                参数	    类型	说明
                code	str	股票代码
                plate_name	str	板块名字
                plate_id	str	板块id
        '''
        ret_code, ret_data = self.ctx.get_plate_list(market,plate_class)
        if ret_code == RET_ERROR:
            print(ret_data)
            exit()
        #print(ret_data)
        table = 'ft_plate_list'
        self.storeservice.insert_many(table, ret_data, 'append')
        return ret_code, ret_data

    def get_global_state(self):
        '''
        功能：获取牛牛程序全局状态
        :return:
        返回： 	(ret, data)
                ret == RET_OK data为包含全局状态的字典，含义如下

                ret != RET_OK data为错误描述字符串

                key	value类型	说明
                market_sz	str	深圳市场状态，参见MarketState
                market_us	str	美国市场状态，参见MarketState
                market_sh	str	上海市场状态，参见MarketState
                market_hk	str	香港市场状态，参见MarketState
                market_hkfuture	str	香港期货市场状态，参见MarketState
                server_ver	str	FutuOpenD版本号
                trd_logined	str	‘1’：已登录交易服务器，‘0’: 未登录交易服务器
                qot_logined	str	‘1’：已登录行情服务器，‘0’: 未登录行情服务器
                timestamp	str	当前格林威治时间戳
        '''
        ret_code, ret_data = self.ctx.get_global_state()
        if ret_code == RET_ERROR:
            print(ret_data)
            exit()
        table = 'ft_global_state'
        self.storeservice.insert_many(table, ret_data, 'append')
        return ret_code, ret_data

    @clock()
    def get_multi_points_history_kline(self,code_list, dates, fields=KL_FIELD.ALL, ktype=KLType.K_DAY):
        '''
        功能：
            获取多支股票多个时间点的指定数据列

        Parameters:
            code_list – 单个或多个股票 ‘HK.00700’ or [‘HK.00700’, ‘HK.00001’]
            dates – 单个或多个日期 ‘2017-01-01’ or [‘2017-01-01’, ‘2017-01-02’]，最多5个时间点
            fields – 单个或多个数据列 KL_FIELD.ALL or [KL_FIELD.DATE_TIME, KL_FIELD.OPEN]
            ktype – K线类型
            autype – 复权类型
            no_data_mode – 指定时间为非交易日时，对应的k线数据取值模式，参见KLNoDataMode
        Returns:
            (ret, data)
            ret == RET_OK 返回pd dataframe数据，固定表头包括’code’(代码) ‘time_point’(指定的日期) ‘data_status’ (KLDataStatus)。数据列格式如下
            ret != RET_OK 返回错误字符串

            参数	        类型	说明
            code	    str	股票代码
            time_point	str	请求的时间
            data_status	str	数据点是否有效，参见KLDataStatus
            time_key	str	k线时间
            open	    float	开盘价
            close	    float	收盘价
            high	    float	最高价
            low	        float	最低价
            pe_ratio	float	市盈率
            turnover_rate	float	换手率
            volume	    int	成交量
            turnover	float	成交额
            change_rate	float	涨跌幅
            last_close	float	昨收价
        '''
        ret_code, ret_data = self.ctx.get_multi_points_history_kline(code_list, dates, fields, ktype)
        if ret_code == RET_ERROR:
            print(ret_data)
            exit()
        print(ret_data)
        return ret_code, ret_data

class HF(object):
    def __init__(self,quote_ctx, subservice):
        print('HF')
        self.ctx = quote_ctx
        self.subservice = subservice

    def get_stock_quote(self, code_list):
        '''
        功能：获取订阅股票报价的实时数据，有订阅要求限制

        Parameters:	code_list – 股票代码列表，必须确保code_list中的股票均订阅成功后才能够执行
        Returns:	(ret, data)
                ret == RET_OK 返回pd dataframe数据，数据列格式如下

                ret != RET_OK 返回错误字符串

                参数	类型	说明
                code	str	股票代码
                data_date	str	日期
                data_time	str	时间
                last_price	float	最新价格
                open_price	float	今日开盘价
                high_price	float	最高价格
                low_price	float	最低价格
                prev_close_price	float	昨收盘价格
                volume	int	成交数量
                turnover	float	成交金额
                turnover_rate	float	换手率
                amplitude	int	振幅
                suspension	bool	是否停牌(True表示停牌)
                listing_date	str	上市日期 (yyyy-MM-dd)
                price_spread	float	当前价差，亦即摆盘数据的买档或卖档的相邻档位的报价差
        '''

        for code in code_list:
            isSubscribed = self.subservice.isSubscribed(code,'QUOTE')
            if isSubscribed == False:
                self.subservice.subscribe(code,'QUOTE')

        ret_code, ret_data = self.ctx.get_stock_quote(code_list)
        if ret_code == RET_ERROR:
            print(ret_data)
            exit()
        #print(ret_data)
        return ret_code, ret_data

    def get_broker_queue(self, code):
        '''
        功能：
            获取股票的经纪队列
        :param code: 股票代码, string, 例如，”HK.00700”
        :return: et, bid_frame_table, ask_frame_table)或(ret, err_message)
                    ret == RET_OK 返回pd dataframe数据，数据列格式如下
                    ret != RET_OK 返回错误字符串
                    bid_frame_table 经纪买盘数据

                    参数	类型	说明
                    code	str	股票代码
                    bid_broker_id	int	经纪买盘id
                    bid_broker_name	str	经纪买盘名称
                    bid_broker_pos	int	经纪档位
                    ask_frame_table 经纪卖盘数据

                    参数	类型	说明
                    code	str	股票代码
                    ask_broker_id	int	经纪卖盘id
                    ask_broker_name	str	经纪卖盘名称
                    ask_broker_pos	int	经纪档位
        '''
        isSubscribed = self.subservice.isSubscribed(code, 'BROKER')
        if isSubscribed == False:
            self.subservice.subscribe(code, 'BROKER')

        ret_code, bid_data, ask_data = self.ctx.get_broker_queue(code)
        if ret_code == RET_ERROR:
            print(bid_data)
            exit()
        # print(bid_data)
        # print(ask_data)
        return ret_code, bid_data, ask_data

    def get_rt_ticker(self, code, num=500):
        '''
        功能： 获取指定股票的实时逐笔。取最近num个逐笔，
        :param code: 股票代码，例如，HK.00700，US.AAPL
        :param num: 最近ticker个数，最多可获取1000个
        :return:
           (ret, data)

            ret == RET_OK 返回pd dataframe数据，数据列格式如下

            ret != RET_OK 返回错误字符串

            参数	类型	说明
            stock_code	str	股票代码
            sequence	int	逐笔序号
            time	str	成交时间
            price	float	成交价格
            volume	int	成交数量（股数）
            turnover	float	成交金额
            ticker_direction	str	逐笔方向
        '''
        isSubscribed = self.subservice.isSubscribed(code,'TICKER')
        if isSubscribed == False:
            self.subservice.subscribe(code,'TICKER')


        ret_code, ret_data = self.ctx.get_rt_ticker(code,num)
        if ret_code == RET_ERROR:
            print(ret_data)
            exit()
        #print(ret_data)
        return ret_code, ret_data

    def get_cur_kline(self, code, num, ktype=SubType.K_DAY, autype=AuType.QFQ):
        '''
        功能：
            实时获取指定股票最近num个K线数据

        Parameters:
            code – 股票代码
            num – k线数据个数，最多1000根
            ktype – k线类型，参见KLType
            autype – 复权类型，参见AuType
        Returns:
            (ret, data)
            ret == RET_OK 返回pd dataframe数据，数据列格式如下
            ret != RET_OK 返回错误字符串

            参数	    类型	说明
            code	str	股票代码
            time_key	str	时间
            open	float	开盘价
            close	float	收盘价
            high	float	最高价
            low	    float	最低价
            volume	int	成交量
            turnover	float	成交额
            pe_ratio	float	市盈率
            turnover_rate	float	换手率
            last_close	    float	昨收价
        '''
        isSubscribed = self.subservice.isSubscribed(code, ktype)
        if isSubscribed == False:
            self.subservice.subscribe(code, ktype)

        ret_code, ret_data = self.ctx.get_cur_kline(code, num, ktype, autype)
        if ret_code == RET_ERROR:
            print(ret_data)
            exit()
        #print(ret_data)
        return ret_code, ret_data

    def get_order_book(self, code):
        '''
        功能：获取实时摆盘数据

               :param code: 股票代码，例如，HK.00700，US.AAPL
        :return:  	(ret, data)
            ret == RET_OK 返回字典，数据格式如下

            ret != RET_OK 返回错误字符串

            {
                'code': 股票代码
                'Ask':[ (ask_price1, ask_volume1，order_num), (ask_price2, ask_volume2, order_num),…]
                'Bid': [ (bid_price1, bid_volume1, order_num), (bid_price2, bid_volume2, order_num),…]
            }

            'Ask'：卖盘， 'Bid'买盘。每个元组的含义是(委托价格，委托数量，委托订单数)
        '''
        isSubscribed = self.subservice.isSubscribed(code, 'ORDER_BOOK')
        if isSubscribed == False:
            self.subservice.subscribe(code, 'ORDER_BOOK')

        ret_code, ret_data = self.ctx.get_order_book(code)
        if ret_code == RET_ERROR:
            print(ret_data)
            exit()
        #print(ret_data)
        return ret_code, ret_data

    def get_rt_data(self,code):
        '''
        功能：获取指定股票的分时数据

        :param code: 股票代码，例如，HK.00700，US.AAPL。
        :return: ret_code失败时，ret_data返回为错误描述字符串； 客户端无符合条件数据时，ret_code为成功，ret_data返回None； 正常情况下，ret_data为一个dataframe，其中包括：

            code: 股票代码；string

            time：时间；string

            data_status：数据状态；bool，正确为True，伪造为False

            opened_mins: 零点到当前多少分钟；int

            cur_price：当前价格；float

            last_close: 昨天收盘的价格；float

            avg_price: 平均价格；float

            volume: 成交量；float

            turnover: 成交额；float
         '''
        isSubscribed = self.subservice.isSubscribed(code, 'RT_DATA')
        if isSubscribed == False:
            self.subservice.subscribe(code, 'RT_DATA')

        ret_code, ret_data = self.ctx.get_rt_data(code)
        if ret_code == RET_ERROR:
            print(ret_data)
            exit()
        #print(ret_data)
        return ret_code, ret_data

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

class Subscribe(object):
    def __init__(self,quote_ctx,total, kline,tiker, quote, order_book,  rt_data, broker):
        print('subscribe')
        self.ctx = quote_ctx
        self.quota = Quota(int(total), int(kline),int(tiker), int(quote), int(order_book),  int(rt_data), int(broker))
        self.subdict = {}

    def subscribe(self, code_list, subtype_list):
        '''
        功能：
            订阅注册需要的实时信息，指定股票和订阅的数据类型即可，港股订阅需要Lv2行情。
        注意：len(code_list) * 订阅的K线类型的数量 <= 100

        Parameters:
            code_list – 需要订阅的股票代码列表
            subtype_list – 需要订阅的数据类型列表，参见SubType
        Returns:
            (ret, err_message)
            ret == RET_OK err_message为None
            ret != RET_OK err_message为错误描述字符串
        '''
        code_list = unique_and_normalize_list(code_list)
        subtype_list = unique_and_normalize_list(subtype_list)

        ret = self.quota.prefeching_cosume(code_list,subtype_list)
        if ret == RET_ERROR:
            print("overquota")
            return RET_OK,None

        ret_code, ret_data = self.ctx.subscribe(code_list, subtype_list)
        if ret_code == RET_ERROR:
            print(ret_data)
            exit()
        #print(ret_data)
        for code in code_list:
            for subtype in subtype_list:
                subitem =  SubItem(code, subtype)
                self.subdict[subitem.stringHash()] = subitem
        self.quota.cosume(code_list, subtype_list)
        return ret_code, ret_data

    def unsubscribe(self, code_list, subtype_list):
        '''
        功能：
            取消订阅

        Parameters:
            code_list – 取消订阅的股票代码列表
            subtype_list – 取消订阅的类型，参见SubType
        Returns:
            (ret, err_message)
            ret == RET_OK err_message为None
            ret != RET_OK err_message为错误描述字符串
        '''
        code_list = unique_and_normalize_list(code_list)
        subtype_list = unique_and_normalize_list(subtype_list)

        ret = self.quota.prefeching_recycle(code_list, subtype_list)
        if ret == RET_ERROR:
            print("overtotal quota")
            return RET_OK, None

        ret_code, ret_data = self.ctx.unsubscribe(code_list, subtype_list)
        if ret_code == RET_ERROR:
            print(ret_data)
            exit()
        #print(ret_data)
        for code in code_list:
            for subtype in subtype_list:
                subitem = SubItem(code, subtype)
                self.subdict.pop(subitem.stringHash())
        self.quota.recycle(code_list,subtype_list)
        return ret_code, ret_data

    def query_subscription(self,is_all_conn=True):
        '''
        功能：
            查询已订阅的实时信息

        param：
            is_all_conn:
             是否返回所有连接的订阅状态,不传或者传False只返回当前连接数据

        return:
            (ret, data)
            ret != RET_OK 返回错误字符串
            ret == RET_OK 返回 定阅信息的字典数据 ，格式如下:
            {
                'total_used': 4,    # 所有连接已使用的定阅额度
                'own_used': 0,       # 当前连接已使用的定阅额度
                'remain': 496,       #  剩余的定阅额度
                'sub_list':          #  每种定阅类型对应的股票列表
                {
                    'BROKER': ['HK.00700', 'HK.02318'],
                    'RT_DATA': ['HK.00700', 'HK.02318']
                }
            }
        '''
        ret_code, ret_data = self.ctx.query_subscription(is_all_conn)
        if ret_code == RET_ERROR:
            print(ret_data)
            exit()
        print( ret_data )
        print( self.subdict.keys() )
        #print(ret_data)
        return ret_code, ret_data

    def isSubscribed(self,stock_code, data_type):
        subitem = SubItem(stock_code, data_type)
        return subitem.stringHash() in self.subdict

class Quota(object):
    def __init__(self,total, kline,ticker, quote, order_book,  rt_data, broker):
        self.total = total
        self.kline = kline
        self.ticker = ticker
        self.quote = quote
        self.order_book = order_book
        self.rt_data = rt_data
        self.broker = broker
        self.remaining_quota = self.total

    def cosume(self,code_list, subtype_list):
        '''
        消耗subtype订阅类型配额,实际配额减少
        :param subtype:
        :return:
        '''
        quota = self._calc_quota(code_list, subtype_list)
        if self.remaining_quota >= quota:
            self.remaining_quota -= quota
        else:
            return RET_ERROR
        return self.remaining_quota

    def prefeching_cosume(self,code_list,subtype_list):
        '''
        预判subtype订阅类型配额是否充足，，实际配额不变
        :param subtype:
        :return:
        '''
        quota = self._calc_quota(code_list, subtype_list)
        if self.remaining_quota >= quota:
            return self.remaining_quota
        else:
            return RET_ERROR

    def recycle(self,code_list,subtype_list):
        '''
        回收subtype订阅类型配额，实际配额增加
        :param subtype:
        :return:
        '''
        quota = self._calc_quota(code_list, subtype_list)
        if self.remaining_quota + quota <= self.total:
            self.remaining_quota += quota
        else:
            return RET_ERROR
        return self.remaining_quota

    def prefeching_recycle(self, code_list,subtype_list):
        '''
        预判回收subtype订阅类型配额是否超额，实际配额不变
        :param subtype:
        :return:
        '''
        quota = self._calc_quota(code_list, subtype_list)
        if self.remaining_quota + quota <= self.total:
            return self.remaining_quota
        else:
            return RET_ERROR

    def _enum_quota(self, subtype):
        quota = 0
        if "TICKER" == subtype:
            quota = self.ticker
        elif "QUOTE" == subtype:
            quota = self.quote
        elif "ORDER_BOOK" == subtype:
            quota = self.order_book
        elif "K_1M" == subtype:
            quota = self.kline
        elif "K_5M" == subtype:
            quota = self.kline
        elif "K_15M" == subtype:
            quota = self.kline
        elif "K_30M" == subtype:
            quota = self.kline
        elif "K_60M" == subtype:
            quota = self.kline
        elif "K_DAY" == subtype:
            quota = self.kline
        elif "K_WEEK" == subtype:
            quota = self.kline
        elif "K_MON" == subtype:
            quota = self.kline
        elif "RT_DATA" == subtype:
            quota = self.rt_data
        elif "BROKER" == subtype:
            quota = self.broker
        else:
            pass
        return int(quota)

    def _calc_quota(self, code_list, subtype_list):
        quota = 0
        for subtype in subtype_list:
            quota += self._enum_quota(subtype)
        quota *= len(code_list)
        return quota

class HSHandler(ABC):
    def __init__(self):
        self.storeservice = MysqlService()

class HSStockQuoteHandler(HSHandler,StockQuoteHandlerBase):
    def __init__(self):
        super(HSStockQuoteHandler,self).__init__()

    '''
    功能：异步处理推送的订阅股票的报价。
    '''
    def on_recv_rsp(self, rsp_str):
        ret_code, data = super(HSStockQuoteHandler, self).on_recv_rsp(rsp_str)
        if ret_code != RET_OK:
            print("HSStockQuoteHandler: error, msg: %s" % data)
            return RET_ERROR, data

        print("HSStockQuoteHandler ", data)  # HSStockQuoteHandler自己的处理逻辑
        if len(data) > 0:
            table = 'ft_stockquote'
            self.storeservice.insert_many(table, data, 'append')

        return RET_OK, data

class HSOrderBookHandler(HSHandler,OrderBookHandlerBase):

    def __init__(self):
        super(HSOrderBookHandler, self).__init__()

    '''
    功能：异步处理推送的实时摆盘。
    '''
    def on_recv_rsp(self, rsp_str):
        ret_code, data = super(HSOrderBookHandler, self).on_recv_rsp(rsp_str)
        if ret_code != RET_OK:
            print("HSOrderBookHandler: error, msg: %s" % data)
            return RET_ERROR, data

        print("HSOrderBookHandler ", data)  # HSOrderBookHandler自己的处理逻辑
        # 不是DataFrame
        # table = 'ft_orderbook'
        # self.storeservice.insert_many(table, data, 'append')
        # {'code': ('SH.000063',),
        #  'Bid': [(0.0, 0, 0), (0.0, 0, 0), (0.0, 0, 0), (0.0, 0, 0), (0.0, 0, 0), (0.0, 0, 0), (0.0, 0, 0), (0.0, 0, 0),
        #          (0.0, 0, 0), (0.0, 0, 0)],
        #  'Ask': [(0.0, 0, 0), (0.0, 0, 0), (0.0, 0, 0), (0.0, 0, 0), (0.0, 0, 0), (0.0, 0, 0), (0.0, 0, 0), (0.0, 0, 0),
        #          (0.0, 0, 0), (0.0, 0, 0)]}

        return RET_OK, data

class HSCurKlineHandler(HSHandler,CurKlineHandlerBase):

    def __init__(self):
        super(HSCurKlineHandler, self).__init__()

    '''
    功能：异步处理推送的k线数据。
    '''
    def on_recv_rsp(self, rsp_str):
        ret_code, data = super(HSCurKlineHandler, self).on_recv_rsp(rsp_str)
        if ret_code != RET_OK:
            print("HSCurKlineHandler: error, msg: %s" % data)
            return RET_ERROR, data

        print("HSCurKlineHandler ", data)  # HSCurKlineHandler自己的处理逻辑
        if len(data) > 0:
            table = 'ft_curkline'
            self.storeservice.insert_many(table, data, 'append')

        return RET_OK, data

class HSTickerHandler(HSHandler,TickerHandlerBase):

    def __init__(self):
        super(HSTickerHandler, self).__init__()

    '''
    功能：异步处理推送的逐笔数据。
    '''
    def on_recv_rsp(self, rsp_str):
        ret_code, data = super(HSTickerHandler, self).on_recv_rsp(rsp_str)
        if ret_code != RET_OK:
            print("HSTickerHandler: error, msg: %s" % data)
            return RET_ERROR, data

        print("HSTickerHandler ", data)  # HSTickerHandler自己的处理逻辑
        if len(data) > 0:
            table = 'ft_ticker'
            self.storeservice.insert_many(table, data, 'append')

        return RET_OK, data

class HSRTDataHandler(HSHandler,RTDataHandlerBase):

    def __init__(self):
        super(HSRTDataHandler, self).__init__()

    '''
    功能：异步处理推送的分时数据。
    '''
    def on_recv_rsp(self, rsp_str):
        ret_code, data = super(HSRTDataHandler, self).on_recv_rsp(rsp_str)
        if ret_code != RET_OK:
            print("HSRTDataHandler: error, msg: %s" % data)
            return RET_ERROR, data

        print("HSRTDataHandler ", data)  # HSRTDataHandler自己的处理逻辑

        if len(data) > 0:
            table = 'ft_rtdata'
            self.storeservice.insert_many(table, data, 'append')

        return RET_OK, data

class HSBrokerHandler(HSHandler,BrokerHandlerBase):

    def __init__(self):
        super(HSBrokerHandler, self).__init__()

    '''
    功能：异步处理推送的经纪数据。
    '''
    def on_recv_rsp(self, rsp_str):
        ret_code, code, data = super(HSBrokerHandler, self).on_recv_rsp(rsp_str)
        if ret_code != RET_OK:
            print("HSBrokerHandler: error, msg: %s" % code)
            return RET_ERROR, code

        print("HSBrokerHandler ", data)  # HSBrokerHandler自己的处理逻辑

        if len(data) > 0:
            table = 'ft_broker'
            bid = data[0]
            ask = data[1]
            self.storeservice.insert_many(table, bid, 'append')
            self.storeservice.insert_many(table, ask, 'append')

        return RET_OK, data