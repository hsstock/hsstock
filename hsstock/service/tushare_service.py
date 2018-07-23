# -*- coding: UTF-8 -*-

import logging
import time

from sqlalchemy.exc import OperationalError
from hsstock.service.mysql_service import MysqlService
from hsstock.utils.app_logging import setup_logging
from hsstock.utils.date_util import DateUtil
import hsstock.utils.decorator  as tick
from hsstock.utils.app_config import AppConfig
import hsstock.tushare as ts


'''
Tushare是一个免费、开源的python财经数据接口包。主要实现对股票等金融数据从数据采集、清洗加工到数据存储的过程，能够为金融分析人员提供快速、整洁、和多样的便于分析的数据，为他们在数据获取方面极大地减轻工作量，使他们更加专注于策略和模型的研究与实现上。
'''

class TUShare_service(object):

    def __init__(self):
        self.tushare_version = ts.__version__
        setup_logging()
        self.storeservice = MysqlService()
        print('tushare_versin', self.tushare_version)

    @tick.clock()
    def get_hist_data(self,code,start=None,end=None,ktype='D',retry_count=3,pause=0):
        '''
        功能：
            获取个股历史交易数据（包括均线数据），可以通过参数设置获取日k线、周k线、月k线，以及5分钟、15分钟、30分钟和60分钟k线数据。本接口只能获取近3年的日线数据，适合搭配均线数据进行选股和分析，如果需要全部历史数据，请调用下一个接口get_h_data()。

        参数说明：

            code：股票代码，即6位数字代码，或者指数代码（sh=上证指数 sz=深圳成指 hs300=沪深300指数 sz50=上证50 zxb=中小板 cyb=创业板）
            start：开始日期，格式YYYY-MM-DD
            end：结束日期，格式YYYY-MM-DD
            ktype：数据类型，D=日k线 W=周 M=月 5=5分钟 15=15分钟 30=30分钟 60=60分钟，默认为D
            retry_count：当网络异常后重试次数，默认为3
            pause:重试时停顿秒数，默认为0

        返回值说明：

            date：日期
            open：开盘价
            high：最高价
            close：收盘价
            low：最低价
            volume：成交量
            price_change：价格变动
            p_change：涨跌幅
            ma5：5日均价
            ma10：10日均价
            ma20:20日均价
            v_ma5:5日均量
            v_ma10:10日均量
            v_ma20:20日均量
            turnover:换手率[注：指数无此项]
        '''
        try:
            df = ts.get_hist_data(code,start, end, ktype,retry_count, pause)
            print(df)
            if df is None:
                return
            df = df.reset_index(level=[0])
            df['code'] = code
            if ktype == 'D':
                table = 'ts2_hist_data'
            else:
                table = 'ts2_hist_data_' + ktype
            self.storeservice.insert_many(table, df)
        except IOError as err:
            logging.error("OS|error: {0}".format(err))
        except OperationalError as err :
            logging.error("OS|error: {0}".format(err))
        else:
            pass

    @tick.clock()
    def get_h_data(self, code, start=None, end=None, autype='qfq', index=False,retry_count=3, pause=1):
        '''
        功能：
            获取历史复权数据，分为前复权和后复权数据，接口提供股票上市以来所有历史数据，默认为前复权。如果不设定开始和结束日期，则返回近一年的复权数据，从性能上考虑，推荐设定开始日期和结束日期，而且最好不要超过三年以上，获取全部历史数据，请分年段分步获取，取到数据后，请及时在本地存储。获取个股首个上市日期，请参考以下方法

        参数说明：

            code:string,股票代码 e.g. 600848
            start:string,开始日期 format：YYYY-MM-DD 为空时取当前日期
            end:string,结束日期 format：YYYY-MM-DD 为空时取去年今日
            autype:string,复权类型，qfq-前复权 hfq-后复权 None-不复权，默认为qfq
            index:Boolean，是否是大盘指数，默认为False
            retry_count : int, 默认3,如遇网络等问题重复执行的次数
            pause : int, 默认 0,重复请求数据过程中暂停的秒数，防止请求间隔时间太短出现的问题

        返回值说明：

            date : 交易日期 (index)
            open : 开盘价
            high : 最高价
            close : 收盘价
            low : 最低价
            volume : 成交量
            amount : 成交金额
        '''
        try:
            df = ts.get_h_data(code, start, end, autype, index, retry_count, pause)
            if df is None:
                return
            df['code'] = code
            df = df.reset_index(level=[0])
            table = 'ts2_h_data'
            self.storeservice.insert_many(table, df)
        except IOError as err:
            logging.error("OS|error: {0}".format(err))
        except OperationalError as err:
            logging.error("OS|error: {0}".format(err))
        else:
            pass

    @tick.clock()
    def get_today_all(self):
        '''
        功能：
            一次性获取当前交易所有股票的行情数据（如果是节假日，即为上一交易日，结果显示速度取决于网速）

        返回值说明：

            code：代码
            name:名称
            changepercent:涨跌幅
            trade:现价
            open:开盘价
            high:最高价
            low:最低价
            settlement:昨日收盘价
            volume:成交量
            turnoverratio:换手率
            amount:成交量
            per:市盈率
            pb:市净率
            mktcap:总市值
            nmc:流通市值
        '''
        try:
            df = ts.get_today_all()
            if df is None:
                return
            date = time.strftime('%Y-%m-%d', time.localtime())
            df['date'] = date
            df = df.reset_index(level=[0])
            del df['index']
            table = 'ts2_today_all'
            self.storeservice.insert_many(table, df)
        except IOError as err:
            logging.error("OS|error: {0}".format(err))
        except OperationalError as err:
            logging.error("OS|error: {0}".format(err))
        else:
            pass

    @tick.clock()
    def get_tick_data(self,code, date=None, retry_count=3, pause=1):
        '''
        功能：
            获取个股以往交易历史的分笔数据明细，通过分析分笔数据，可以大致判断资金的进出情况。在使用过程中，对于获取股票某一阶段的历史分笔数据，需要通过参入交易日参数并append到一个DataFrame或者直接append到本地同一个文件里。历史分笔接口只能获取当前交易日之前的数据，当日分笔历史数据请调用get_today_ticks()接口或者在当日18点后通过本接口获取。

        参数说明：
            code：股票代码，即6位数字代码
            date：日期，格式YYYY-MM-DD
            retry_count : int, 默认3,如遇网络等问题重复执行的次数
            pause : int, 默认 0,重复请求数据过程中暂停的秒数，防止请求间隔时间太短出现的问题

        返回值说明：

            time：时间
            price：成交价格
            change：价格变动
            volume：成交手
            amount：成交金额(元)
            type：买卖类型【买盘、卖盘、中性盘】
        '''
        try:
            df = ts.get_tick_data(code,date,retry_count, pause)
            if df is None:
                return
            df = df.replace('--', 0)
            df['change'] = df['change'].astype(float)
            df['date'] = DateUtil.getTodayStr()
            df['code'] = code
            df = df.reset_index(level=[0])
            del df['index']
            self.storeservice.insert_many('ts2_tick_data', df)
        except IOError as err:
            logging.error("OS|error: {0}".format(err))
        except OperationalError as err:
            logging.error("OS|error: {0}".format(err))
        else:
            pass

    @tick.clock()
    def get_realtime_quotes(self,codes):
        '''
        功能：
            获取实时分笔数据，可以实时取得股票当前报价和成交信息，其中一种场景是，写一个python定时程序来调用本接口（可两三秒执行一次，性能与行情软件基本一致），然后通过DataFrame的矩阵计算实现交易监控，可实时监测交易量和价格的变化。

        参数说明：
            symbols：6位数字股票代码，或者指数代码（sh=上证指数 sz=深圳成指 hs300=沪深300指数 sz50=上证50 zxb=中小板 cyb=创业板） 可输入的类型：str、list、set或者pandas的Series对象

        返回值说明：

            0：name，股票名字
            1：open，今日开盘价
            2：pre_close，昨日收盘价
            3：price，当前价格
            4：high，今日最高价
            5：low，今日最低价
            6：bid，竞买价，即“买一”报价
            7：ask，竞卖价，即“卖一”报价
            8：volume，成交量 maybe you need do volume/100
            9：amount，成交金额（元 CNY）
            10：b1_v，委买一（笔数 bid volume）
            11：b1_p，委买一（价格 bid price）
            12：b2_v，“买二”
            13：b2_p，“买二”
            14：b3_v，“买三”
            15：b3_p，“买三”
            16：b4_v，“买四”
            17：b4_p，“买四”
            18：b5_v，“买五”
            19：b5_p，“买五”
            20：a1_v，委卖一（笔数 ask volume）
            21：a1_p，委卖一（价格 ask price）
            ...
            30：date，日期；
            31：time，时间；
        '''
        try:
            df = ts.get_realtime_quotes(codes)
            if df is None:
                return
            df = df.replace('--', 0)
            df = df.replace('', 0)
            df['b1_v'] = df['b1_v'].astype(int)
            df['b2_v'] = df['b2_v'].astype(int)
            df['b3_v'] = df['b3_v'].astype(int)
            df['b4_v'] = df['b4_v'].astype(int)
            df['b5_v'] = df['b5_v'].astype(int)
            df['a1_v'] = df['a1_v'].astype(int)
            df['a2_v'] = df['a2_v'].astype(int)
            df['a3_v'] = df['a3_v'].astype(int)
            df['a4_v'] = df['a4_v'].astype(int)
            df['a5_v'] = df['a5_v'].astype(int)
            df['date'] = DateUtil.getTodayStr()
            df = df.reset_index(level=[0])
            del df['index']
            table = 'ts2_realtime_quotes'
            self.storeservice.insert_many(table, df)
        except IOError as err:
            logging.error("OS|error: {0}".format(err))
        except OperationalError as err:
            logging.error("OS|error: {0}".format(err))
        else:
            pass

    @tick.clock()
    def get_today_ticks(self,code,retry_count=3,pause=0):
        '''
        功能：
            获取当前交易日（交易进行中使用）已经产生的分笔明细数据。

        参数说明：
            code：股票代码，即6位数字代码
            retry_count : int, 默认3,如遇网络等问题重复执行的次数
            pause : int, 默认 0,重复请求数据过程中暂停的秒数，防止请求间隔时间太短出现的问题


        返回值说明：

            time：时间
            price：当前价格
            pchange:涨跌幅
            change：价格变动
            volume：成交手
            amount：成交金额(元)
            type：买卖类型【买盘、卖盘、中性盘】
        '''
        try:
            df = ts.get_today_ticks(code,retry_count,pause)
            if df is None:
                return
            df = df.replace('--', 0)
            df['pchange'] = df['pchange'].astype(float)
            df['date'] = DateUtil.getTodayStr()
            df['code'] = code
            df = df.reset_index(level=[0])
            del df['index']
            table = 'ts2_today_ticks'
            self.storeservice.insert_many(table, df)
        except IOError as err:
            logging.error("OS|error: {0}".format(err))
        except OperationalError as err:
            logging.error("OS|error: {0}".format(err))
        else:
            pass

    @tick.clock()
    def get_index(self):
        '''
        功能：
            获取大盘指数行情

        返回值说明：

            code:指数代码
            name:指数名称
            change:涨跌幅
            open:开盘点位
            preclose:昨日收盘点位
            close:收盘点位
            high:最高点位
            low:最低点位
            volume:成交量(手)
            amount:成交金额（亿元）
        '''
        try:
            df = ts.get_index()
            if df is None:
                return
            df['date'] = DateUtil.getTodayStr()
            df = df.reset_index(level=[0])
            del df['index']
            table = 'ts2_index'
            self.storeservice.insert_many(table, df, 'replace')
        except IOError as err:
            logging.error("OS|error: {0}".format(err))
        except OperationalError as err:
            logging.error("OS|error: {0}".format(err))
        else:
            pass

    @tick.clock()
    def get_sina_dd(self,code,date='2018-06-13',vol=400,retry_count=3,pause=0):
        '''
        功能：
            获取大单交易数据，默认为大于等于400手，数据来源于新浪财经。

        参数说明：
            code：股票代码，即6位数字代码
            date:日期，格式YYYY-MM-DD
            vol:手数，默认为400手，输入数值型参数
            retry_count : int, 默认3,如遇网络等问题重复执行的次数
            pause : int, 默认 0,重复请求数据过程中暂停的秒数，防止请求间隔时间太短出现的问题

        返回值说明：

            code：代码
            name：名称
            time：时间
            price：当前价格
            volume：成交手
            preprice ：上一笔价格
            type：买卖类型【买盘、卖盘、中性盘】
        '''
        try:
            df = ts.get_sina_dd(code,date,vol,retry_count,pause)
            if df is None:
                return
            df['date'] = date
            table = 'ts2_sina_dd'
            self.storeservice.insert_many(table, df)
        except IOError as err:
            logging.error("OS|error: {0}".format(err))
        except OperationalError as err:
            logging.error("OS|error: {0}".format(err))
        else:
            pass

    @tick.clock()
    def forecast_data(self,year=2018,quarter=1):
        '''
        功能：
            按年度、季度获取业绩预告数据，接口提供从1998年以后每年的业绩预告数据，需指定年度、季度两个参数。数据在获取的过程中，会打印进度信息(下同)。

        参数说明：

            year:int 年度 e.g:2014
            quarter:int 季度 :1、2、3、4，只能输入这4个季度

        结果返回的数据属性说明如下：

            code,代码
            name,名称
            type,业绩变动类型【预增、预亏等】
            report_date,发布日期
            pre_eps,上年同期每股收益
            range,业绩变动范围
        '''
        try:
            df = ts.forecast_data(year, quarter)
            if df is None:
                return
            df['year'] = year
            df['quarter'] = quarter
            table = 'ts2_forecast_data'
            self.storeservice.insert_many(table, df)
        except IOError as err:
            logging.error("OS|error: {0}".format(err))
        except OperationalError as err:
            logging.error("OS|error: {0}".format(err))
        else:
            pass

    @tick.clock()
    def xsg_data(self,year=2018,month=None,retry_count=3,pause=0):
        '''
        功能：
            以月的形式返回限售股解禁情况，通过了解解禁股本的大小，判断股票上行的压力。可通过设定年份和月份参数获取不同时段的数据。

        参数说明：

            year:年份,默认为当前年
            month:解禁月份，默认为当前月
            retry_count：当网络异常后重试次数，默认为3
            pause:重试时停顿秒数，默认为0

        结果返回的数据属性说明如下：

            code：股票代码
            name：股票名称
            date:解禁日期
            count:解禁数量（万股）
            ratio:占总盘比率
        '''
        try:
            df = ts.xsg_data(year,month,retry_count,pause)
            if df is None:
                return
            table = 'ts2_xsg_data'
            self.storeservice.insert_many(table, df, 'replace')
        except IOError as err:
            logging.error("OS|error: {0}".format(err))
        except OperationalError as err:
            logging.error("OS|error: {0}".format(err))
        else:
            pass

    @tick.clock()
    def fund_holdings(self,year=2018,quarter=1,retry_count=3,pause=0):
        '''
        功能：
            获取每个季度基金持有上市公司股票的数据。

        参数说明：

            year:年份,默认为当前年
            quarter:季度（只能输入1，2，3，4这个四个数字）
            retry_count：当网络异常后重试次数，默认为3
            pause:重试时停顿秒数，默认为0

        结果返回的数据属性说明如下：

            code：股票代码
            name：股票名称
            date:报告日期
            nums:基金家数
            nlast:与上期相比（增加或减少了）
            count:基金持股数（万股）
            clast:与上期相比
            amount:基金持股市值
            ratio:占流通盘比率
        '''
        try:
            df = ts.fund_holdings(year,quarter,retry_count,pause)
            if df is None:
                return
            df['year'] = year
            df['quarter'] = quarter
            table = 'ts2_fund_holdings'
            self.storeservice.insert_many(table, df)
        except IOError as err:
            logging.error("OS|error: {0}".format(err))
        except OperationalError as err:
            logging.error("OS|error: {0}".format(err))
        else:
            pass

    @tick.clock()
    def new_stocks(self,retry_count=3,pause=0):
        '''
        功能：
            获取IPO发行和上市的时间列表，包括发行数量、网上发行数量、发行价格已经中签率信息等。

        参数说明：

            retry_count：当网络异常后重试次数，默认为3
            pause:重试时停顿秒数，默认为0

        结果返回的数据属性说明如下：

            code：股票代码
            name：股票名称
            ipo_date:上网发行日期
            issue_date:上市日期
            amount:发行数量(万股)
            markets:上网发行数量(万股)
            price:发行价格(元)
            pe:发行市盈率
            limit:个人申购上限(万股)
            funds：募集资金(亿元)
            ballot:网上中签率(%)
        '''
        try:
            df = ts.new_stocks(retry_count,pause)
            if df is None:
                return
            table = 'ts2_new_stocks'
            self.storeservice.insert_many(table, df, 'replace')
        except IOError as err:
            logging.error("OS|error: {0}".format(err))
        except OperationalError as err:
            logging.error("OS|error: {0}".format(err))
        else:
            pass

    @tick.clock()
    def get_industry_classified(self):
        '''
        功能：
            在现实交易中，经常会按行业统计股票的涨跌幅或资金进出，本接口按照sina财经对沪深股票进行的行业分类，返回所有股票所属行业的信息。考虑到是一次性在线获取数据，调用接口时会有一定的延时，请在数据返回后自行将数据进行及时存储。sina财经提供的行业分类信息大致如下图所示：

        参数说明：

        结果返回的数据属性说明如下：

            code：股票代码
            name：股票名称
            c_name：行业名称
        '''
        try:
            df = ts.get_industry_classified()
            if df is None:
                return
            table='ts2_industry_classified'
            self.storeservice.insert_many(table, df, 'replace')
        except IOError as err:
            logging.error("OS|error: {0}".format(err))
        except OperationalError as err:
            logging.error("OS|error: {0}".format(err))
        else:
            pass

    @tick.clock()
    def get_concept_classified(self):
        '''
        功能：
            返回股票概念的分类数据，现实的二级市场交易中，经常会以”概念”来炒作，在数据分析过程中，可根据概念分类监测资金等信息的变动情况。本接口是一次性在线获取数据，调用接口时会有一定的延时，请在数据返回后自行将数据进行及时存储。sina财经提供的概念分类信息大致如下图所示：

        参数说明：


        结果返回的数据属性说明如下：

            code：股票代码
            name：股票名称
            c_name：行业名称
        '''
        try:
            df = ts.get_concept_classified()
            if df is None:
                return
            table = 'ts2_concept_classified'
            self.storeservice.insert_many(table, df, 'replace')
        except IOError as err:
            logging.error("OS|error: {0}".format(err))
        except OperationalError as err:
            logging.error("OS|error: {0}".format(err))
        else:
            pass

    @tick.clock()
    def get_area_classified(self,file_path=None):
        '''
        功能：
            按地域对股票进行分类，即查找出哪些股票属于哪个省份。

        参数说明：
            file_path:文件路径，默认为None即由TuShare提供，可以设定自己的股票文件路径

        结果返回的数据属性说明如下：

            code：股票代码
            name：股票名称
            c_name：行业名称
        '''
        try:
            df = ts.get_area_classified()
            if df is None:
                return
            table = 'ts2_area_classified'
            self.storeservice.insert_many(table, df, 'replace')
        except IOError as err:
            logging.error("OS|error: {0}".format(err))
        except OperationalError as err:
            logging.error("OS|error: {0}".format(err))
        else:
            pass

    @tick.clock()
    def get_sme_classified(self,file_path=None):
        '''
        功能：
            获取中小板股票数据，即查找所有002开头的股票

        参数说明：
            file_path:文件路径，默认为None即由TuShare提供，可以设定自己的股票文件路径

        结果返回的数据属性说明如下：

            code：股票代码
            name：股票名称
        '''
        try:
            df = ts.get_sme_classified()
            if df is None:
                return
            table = 'ts2_sme_classified'
            self.storeservice.insert_many(table, df,'replace')
        except IOError as err:
            logging.error("OS|error: {0}".format(err))
        except OperationalError as err:
            logging.error("OS|error: {0}".format(err))
        else:
            pass

    @tick.clock()
    def get_gem_classified(self,file_path=None):
        '''
        功能：
            获取创业板股票数据，即查找所有300开头的股票

        参数说明：
            file_path:文件路径，默认为None即由TuShare提供，可以设定自己的股票文件路径

        结果返回的数据属性说明如下：

            code：股票代码
            name：股票名称
        '''
        try:
            df = ts.get_gem_classified()
            if df is None:
                return
            table = 'ts2_gem_classified'
            self.storeservice.insert_many(table, df, 'replace')
        except IOError as err:
            logging.error("OS|error: {0}".format(err))
        except OperationalError as err:
            logging.error("OS|error: {0}".format(err))
        else:
            pass

    @tick.clock()
    def get_st_classified(self, file_path=None):
        '''
        功能：
            获取风险警示板股票数据，即查找所有st股票

        参数说明：
            file_path:文件路径，默认为None即由TuShare提供，可以设定自己的股票文件路径

        结果返回的数据属性说明如下：

            code：股票代码
            name：股票名称
        '''
        try:
            df = ts.get_st_classified()
            if df is None:
                return
            table = 'ts2_st_classified'
            self.storeservice.insert_many(table, df,'replace')
        except IOError as err:
            logging.error("OS|error: {0}".format(err))
        except OperationalError as err:
            logging.error("OS|error: {0}".format(err))
        else:
            pass

    @tick.clock()
    def get_hs300s(self, file_path=None):
        '''
        功能：
            获取沪深300当前成份股及所占权重

        参数说明：

        结果返回的数据属性说明如下：

            code :股票代码
            name :股票名称
            date :日期
            weight:权重
        '''
        try:
            df = ts.get_hs300s()
            if df is None:
                return
            table = 'ts2_hs300s'
            self.storeservice.insert_many(table, df, 'replace')
        except IOError as err:
            logging.error("OS|error: {0}".format(err))
        except OperationalError as err:
            logging.error("OS|error: {0}".format(err))
        else:
            pass

    @tick.clock()
    def get_sz50s(self, file_path=None):
        '''
        功能：
            获取上证50成份股

        参数说明：

        结果返回的数据属性说明如下：

            code :股票代码
            name :股票名称
        '''
        try:
            df = ts.get_sz50s()
            if df is None:
                return
            table = 'ts2_sz50s'
            self.storeservice.insert_many(table, df, 'replace')
        except IOError as err:
            logging.error("OS|error: {0}".format(err))
        except OperationalError as err:
            logging.error("OS|error: {0}".format(err))
        else:
            pass

    @tick.clock()
    def get_zz500s(self, file_path=None):
        '''
        功能：
            获取中证500成份股

        参数说明：

        结果返回的数据属性说明如下：

            code :股票代码
            name :股票名称
        '''
        try:
            df = ts.get_zz500s()
            if df is None:
                return
            table = 'ts2_zz500s'
            self.storeservice.insert_many(table, df, 'replace')
        except IOError as err:
            logging.error("OS|error: {0}".format(err))
        except OperationalError as err:
            logging.error("OS|error: {0}".format(err))
        else:
            pass

    @tick.clock()
    def get_terminated(self, file_path=None):
        '''
        Forbidden
        功能：
            获取已经被终止上市的股票列表，数据从上交所获取，目前只有在上海证券交易所交易被终止的股票。

        参数说明：

        结果返回的数据属性说明如下：

            code：股票代码
            name：股票名称
            oDate:上市日期
            tDate:终止上市日期
        '''
        return ts.get_terminated()

    @tick.clock()
    def get_suspended(self, file_path=None):
        '''
        Forbidden
        功能：
            获取被暂停上市的股票列表，数据从上交所获取，目前只有在上海证券交易所交易被终止的股票。

        参数说明：

        结果返回的数据属性说明如下：

            code：股票代码
            name：股票名称
            oDate:上市日期
            tDate:终止上市日期
        '''
        return ts.get_suspended()

    @tick.clock()
    def get_stock_basics(self, file_path=None):
        '''
        功能：
            获取沪深上市公司基本情况。属性包括：

        参数说明：

        结果返回的数据属性说明如下：

            code,代码
            name,名称
            industry,所属行业
            area,地区
            pe,市盈率
            outstanding,流通股本(亿)
            totals,总股本(亿)
            totalAssets,总资产(万)
            liquidAssets,流动资产
            fixedAssets,固定资产
            reserved,公积金
            reservedPerShare,每股公积金
            esp,每股收益
            bvps,每股净资
            pb,市净率
            timeToMarket,上市日期
            undp,未分利润
            perundp, 每股未分配
            rev,收入同比(%)
            profit,利润同比(%)
            gpr,毛利率(%)
            npr,净利润率(%)
            holders,股东人数
        '''
        try:
            df = ts.get_stock_basics()
            if df is None:
                return
            table = 'ts2_stock_basics'
            # replace will fail
            #self.storeservice.insert_many(table, df, 'append', True, 'code')
            self.storeservice.insert_many(table, df, 'replace')
            return df
        except IOError as err:
            logging.error("OS|error: {0}".format(err))
        except OperationalError as err:
            logging.error("OS|error: {0}".format(err))
        else:
            pass

    @tick.clock()
    def get_report_data(self, year=2018, quarter=1):
        '''
        功能：
            按年度、季度获取业绩报表数据。数据获取需要一定的时间，网速取决于您的网速，请耐心等待。结果返回的数据属性说明如下：

        参数说明：

        结果返回的数据属性说明如下：

            code,代码
            name,名称
            esp,每股收益
            eps_yoy,每股收益同比(%)
            bvps,每股净资产
            roe,净资产收益率(%)
            epcf,每股现金流量(元)
            net_profits,净利润(万元)
            profits_yoy,净利润同比(%)
            distrib,分配方案
            report_date,发布日期
        '''
        try:
            df = ts.get_report_data(year,quarter)
            if df is None:
                return
            df['year'] = year
            df['quarter'] = quarter
            table = 'ts2_report_data'
            self.storeservice.insert_many(table, df)
        except IOError as err:
            logging.error("OS|error: {0}".format(err))
        except OperationalError as err:
            logging.error("OS|error: {0}".format(err))
        else:
            pass

    @tick.clock()
    def get_profit_data(self, year=2018, quarter=1):
        '''
        功能：
            按年度、季度获取盈利能力数据，结果返回的数据属性说明如下：

        参数说明：

        结果返回的数据属性说明如下：

            code,代码
            name,名称
            roe,净资产收益率(%)
            net_profit_ratio,净利率(%)
            gross_profit_rate,毛利率(%)
            net_profits,净利润(万元)
            esp,每股收益
            business_income,营业收入(百万元)
            bips,每股主营业务收入(元)
        '''
        try:
            df = ts.get_profit_data(year, quarter)
            if df is None:
                return
            df['year'] = year
            df['quarter'] = quarter
            table = 'ts2_profit_data'
            self.storeservice.insert_many(table, df)
        except IOError as err:
            logging.error("OS|error: {0}".format(err))
        except OperationalError as err:
            logging.error("OS|error: {0}".format(err))
        else:
            pass

    @tick.clock()
    def profit_data(self, year=2018, top=25, retry_count=3, pause=0):
        '''
        功能：
            每到季报、年报公布的时段，就经常会有上市公司利润分配预案发布，而一些高送转高分红的股票往往会成为市场炒作的热点。及时获取和统计高送转预案的股票是参与热点炒作的关键，TuShare提供了简洁的接口，能返回股票的送转和分红预案情况。

        参数说明：
            year : 预案公布的年份，默认为2014
            top :取最新n条数据，默认取最近公布的25条
            retry_count：当网络异常后重试次数，默认为3
            pause:重试时停顿秒数，默认为0

        返回值说明：

            code:股票代码
            name:股票名称
            year:分配年份
            report_date:公布日期
            divi:分红金额（每10股）
            shares:转增和送股数（每10股）
        '''
        try:
            df = ts.profit_data(year, top=100)
            if df is None:
                return
            df['year'] = year
            table = 'ts2_pre_profit_data'
            self.storeservice.insert_many(table, df)
        except IOError as err:
            logging.error("OS|error: {0}".format(err))
        except OperationalError as err:
            logging.error("OS|error: {0}".format(err))
        else:
            pass

    @tick.clock()
    def get_operation_data(self, year=2018, quarter=1):
        '''
        功能：
            按年度、季度获取营运能力数据，结果返回的数据属性说明如下：

        参数说明：

        结果返回的数据属性说明如下：

            code,代码
            name,名称
            arturnover,应收账款周转率(次)
            arturndays,应收账款周转天数(天)
            inventory_turnover,存货周转率(次)
            inventory_days,存货周转天数(天)
            currentasset_turnover,流动资产周转率(次)
            currentasset_days,流动资产周转天数(天)
        '''
        try:
            df = ts.get_operation_data(year, quarter)
            if df is None:
                return
            df['year'] = year
            df['quarter'] = quarter
            table = 'ts2_operation_data'
            self.storeservice.insert_many(table, df)
        except IOError as err:
            logging.error("OS|error: {0}".format(err))
        except OperationalError as err:
            logging.error("OS|error: {0}".format(err))
        else:
            pass

    @tick.clock()
    def get_growth_data(self, year=2018, quarter=1):
        '''
        功能：
            按年度、季度获取成长能力数据，结果返回的数据属性说明如下：

        参数说明：

        结果返回的数据属性说明如下：

            code,代码
            name,名称
            mbrg,主营业务收入增长率(%)
            nprg,净利润增长率(%)
            nav,净资产增长率
            targ,总资产增长率
            epsg,每股收益增长率
            seg,股东权益增长率
        '''
        try:
            df = ts.get_growth_data(year, quarter)
            if df is None:
                return
            df['year'] = year
            df['quarter'] = quarter
            table = 'ts2_growth_data'
            self.storeservice.insert_many(table, df)
        except IOError as err:
            logging.error("OS|error: {0}".format(err))
        except OperationalError as err:
            logging.error("OS|error: {0}".format(err))
        else:
            pass

    @tick.clock()
    def get_debtpaying_data(self, year=2018, quarter=1):
        '''
        功能：
            按年度、季度获取偿债能力数据，结果返回的数据属性说明如下

        参数说明：

        结果返回的数据属性说明如下：

            code,代码
            name,名称
            currentratio,流动比率
            quickratio,速动比率
            cashratio,现金比率
            icratio,利息支付倍数
            sheqratio,股东权益比率
            adratio,股东权益增长率
        '''
        try:
            df = ts.get_debtpaying_data(year, quarter)
            if df is None:
                return
            df = df.replace('--', 0)
            df['currentratio'] = df['currentratio'].astype(float)
            df['quickratio'] = df['quickratio'].astype(float)
            df['cashratio'] = df['cashratio'].astype(float)
            df['icratio'] = df['icratio'].astype(float)
            df['sheqratio'] = df['sheqratio'].astype(float)
            df['adratio'] = df['adratio'].astype(float)
            df['year'] = year
            df['quarter'] = quarter
            table = 'ts2_debtpaying_data'
            self.storeservice.insert_many(table, df)
        except IOError as err:
            logging.error("OS|error: {0}".format(err))
        except OperationalError as err:
            logging.error("OS|error: {0}".format(err))
        else:
            pass

    @tick.clock()
    def get_cashflow_data(self, year=2018, quarter=1):
        '''
        功能：
            按年度、季度获取现金流量数据，结果返回的数据属性说明如下：

        参数说明：

        结果返回的数据属性说明如下：

            code,代码
            name,名称
            cf_sales,经营现金净流量对销售收入比率
            rateofreturn,资产的经营现金流量回报率
            cf_nm,经营现金净流量与净利润的比率
            cf_liabilities,经营现金净流量对负债比率
            cashflowratio,现金流量比率
        '''
        try:
            df = ts.get_cashflow_data(year, quarter)
            if df is None:
                return
            df['year'] = year
            df['quarter'] = quarter
            table = 'ts2_cashflow_data'
            self.storeservice.insert_many(table, df)
        except IOError as err:
            logging.error("OS|error: {0}".format(err))
        except OperationalError as err:
            logging.error("OS|error: {0}".format(err))
        else:
            pass

    @tick.clock()
    def get_deposit_rate(self):
        '''
        功能：
            存款利率

        参数说明：

        结果返回的数据属性说明如下：

            date :变动日期
            deposit_type :存款种类
            rate:利率（%）
        '''
        try:
            df = ts.get_deposit_rate()
            if df is None:
                return
            df = df.replace('--', 0)
            df['rate'] = df['rate'].astype(float)
            table = 'ts2_deposit_rate'
            self.storeservice.insert_many(table, df, 'replace')
        except IOError as err:
            logging.error("OS|error: {0}".format(err))
        except OperationalError as err:
            logging.error("OS|error: {0}".format(err))
        else:
            pass

    @tick.clock()
    def get_loan_rate(self):
        '''
        功能：
            贷款利率

        参数说明：

        结果返回的数据属性说明如下：

            date :执行日期
            loan_type :存款种类
            rate:利率（%）
        '''
        try:
            df = ts.get_loan_rate()
            if df is None:
                return
            df = df.replace('--', 0)
            df['rate'] = df['rate'].astype(float)
            table = 'ts2_loan_rate'
            self.storeservice.insert_many(table, df, 'replace')
        except IOError as err:
            logging.error("OS|error: {0}".format(err))
        except OperationalError as err:
            logging.error("OS|error: {0}".format(err))
        else:
            pass

    @tick.clock()
    def get_rrr(self):
        '''
        功能：
            存款准备金率

        参数说明：

        结果返回的数据属性说明如下：

            date :变动日期
            before :调整前存款准备金率(%)
            now:调整后存款准备金率(%)
            changed:调整幅度(%)
        '''
        try:
            df = ts.get_rrr()
            if df is None:
                return
            df = df.replace('--', 0)
            df['changed'] = df['changed'].astype(float)
            table = 'ts2_rrr'
            self.storeservice.insert_many(table, df, 'replace')
        except IOError as err:
            logging.error("OS|error: {0}".format(err))
        except OperationalError as err:
            logging.error("OS|error: {0}".format(err))
        else:
            pass

    @tick.clock()
    def get_money_supply(self):
        '''
        功能：
            货币供应量

        参数说明：

        结果返回的数据属性说明如下：

            month :统计时间
            m2 :货币和准货币（广义货币M2）(亿元)
            m2_yoy:货币和准货币（广义货币M2）同比增长(%)
            m1:货币(狭义货币M1)(亿元)
            m1_yoy:货币(狭义货币M1)同比增长(%)
            m0:流通中现金(M0)(亿元)
            m0_yoy:流通中现金(M0)同比增长(%)
            cd:活期存款(亿元)
            cd_yoy:活期存款同比增长(%)
            qm:准货币(亿元)
            qm_yoy:准货币同比增长(%)
            ftd:定期存款(亿元)
            ftd_yoy:定期存款同比增长(%)
            sd:储蓄存款(亿元)
            sd_yoy:储蓄存款同比增长(%)
            rests:其他存款(亿元)
            rests_yoy:其他存款同比增长(%)
        '''
        try:
            df = ts.get_money_supply()
            if df is None:
                return
            df = df.replace('--', 0)
            df['m2'] = df['m2'].astype(float)
            df['m2_yoy'] = df['m2_yoy'].astype(float)
            df['m1'] = df['m1'].astype(float)
            df['m1_yoy'] = df['m1_yoy'].astype(float)
            df['m0'] = df['m0'].astype(float)
            df['m0_yoy'] = df['m0_yoy'].astype(float)
            df['cd'] = df['cd'].astype(float)
            df['cd_yoy'] = df['cd_yoy'].astype(float)
            df['qm'] = df['qm'].astype(float)
            df['qm_yoy'] = df['qm_yoy'].astype(float)
            df['ftd'] = df['ftd'].astype(float)
            df['ftd_yoy'] = df['ftd_yoy'].astype(float)
            df['sd'] = df['sd'].astype(float)
            df['sd_yoy'] = df['sd_yoy'].astype(float)
            df['rests'] = df['rests'].astype(float)
            df['rests_yoy'] = df['rests_yoy'].astype(float)
            table = 'ts2_money_supply'
            self.storeservice.insert_many(table, df,'replace')
        except IOError as err:
            logging.error("OS|error: {0}".format(err))
        except OperationalError as err:
            logging.error("OS|error: {0}".format(err))
        else:
            pass

    @tick.clock()
    def get_money_supply_bal(self):
        '''
        功能：
            货币供应量(年底余额)

        参数说明：

        结果返回的数据属性说明如下：

            year :统计年度
            m2 :货币和准货币(亿元)
            m1:货币(亿元)
            m0:流通中现金(亿元)
            cd:活期存款(亿元)
            qm:准货币(亿元)
            ftd:定期存款(亿元)
            sd:储蓄存款(亿元)
            rests:其他存款(亿元)
        '''
        try:
            df = ts.get_money_supply_bal()
            if df is None:
                return
            df = df.replace('--', 0)
            df['m2'] = df['m2'].astype(float)
            df['m1'] = df['m1'].astype(float)
            df['m0'] = df['m0'].astype(float)
            df['cd'] = df['cd'].astype(float)
            df['qm'] = df['qm'].astype(float)
            df['ftd'] = df['ftd'].astype(float)
            df['sd'] = df['sd'].astype(float)
            df['rests'] = df['rests'].astype(float)
            table = 'ts2_money_supply_bal'
            self.storeservice.insert_many(table, df,'replace')
        except IOError as err:
            logging.error("OS|error: {0}".format(err))
        except OperationalError as err:
            logging.error("OS|error: {0}".format(err))
        else:
            pass

    @tick.clock()
    def get_gdp_year(self):
        '''
        功能：
            国内生产总值(年度)

        参数说明：

        结果返回的数据属性说明如下：

            year :统计年度
            gdp :国内生产总值(亿元)
            pc_gdp :人均国内生产总值(元)
            gnp :国民生产总值(亿元)
            pi :第一产业(亿元)
            si :第二产业(亿元)
            industry :工业(亿元)
            cons_industry :建筑业(亿元)
            ti :第三产业(亿元)
            trans_industry :交通运输仓储邮电通信业(亿元)
            lbdy :批发零售贸易及餐饮业(亿元)
        '''
        try:
            df = ts.get_gdp_year()
            if df is None:
                return
            table = 'ts2_gdp_year'
            self.storeservice.insert_many(table, df, 'replace')
        except IOError as err:
            logging.error("OS|error: {0}".format(err))
        except OperationalError as err:
            logging.error("OS|error: {0}".format(err))
        else:
            pass

    @tick.clock()
    def get_gdp_quarter(self):
        '''
        功能：
            国内生产总值(年度)

        参数说明：

        结果返回的数据属性说明如下：

            quarter :季度
            gdp :国内生产总值(亿元)
            gdp_yoy :国内生产总值同比增长(%)
            pi :第一产业增加值(亿元)
            pi_yoy:第一产业增加值同比增长(%)
            si :第二产业增加值(亿元)
            si_yoy :第二产业增加值同比增长(%)
            ti :第三产业增加值(亿元)
            ti_yoy :第三产业增加值同比增长(%)
        '''
        try:
            df = ts.get_gdp_quarter()
            if df is None:
                return
            table = 'ts2_gdp_quarter'
            self.storeservice.insert_many(table, df, 'replace')
        except IOError as err:
            logging.error("OS|error: {0}".format(err))
        except OperationalError as err:
            logging.error("OS|error: {0}".format(err))
        else:
            pass

    @tick.clock()
    def get_gdp_for(self):
        '''
        功能：
            三大需求对GDP贡献

        参数说明：

        结果返回的数据属性说明如下：

            year :统计年度
            end_for :最终消费支出贡献率(%)
            for_rate :最终消费支出拉动(百分点)
            asset_for :资本形成总额贡献率(%)
            asset_rate:资本形成总额拉动(百分点)
            goods_for :货物和服务净出口贡献率(%)
            goods_rate :货物和服务净出口拉动(百分点)
        '''
        try:
            df = ts.get_gdp_for()
            if df is None:
                return
            table = 'ts2_gdp_for'
            self.storeservice.insert_many(table, df, 'replace')
        except IOError as err:
            logging.error("OS|error: {0}".format(err))
        except OperationalError as err:
            logging.error("OS|error: {0}".format(err))
        else:
            pass

    @tick.clock()
    def get_gdp_pull(self):
        '''
        功能：
            三大产业对GDP拉动

        参数说明：

        结果返回的数据属性说明如下：

            year :统计年度
            gdp_yoy :国内生产总值同比增长(%)
            pi :第一产业拉动率(%)
            si :第二产业拉动率(%)
            industry:其中工业拉动(%)
            ti :第三产业拉动率(%)
        '''
        try:
            df = ts.get_gdp_pull()
            if df is None:
                return
            table = 'ts2_gdp_pull'
            self.storeservice.insert_many(table, df, 'replace')
        except IOError as err:
            logging.error("OS|error: {0}".format(err))
        except OperationalError as err:
            logging.error("OS|error: {0}".format(err))
        else:
            pass

    @tick.clock()
    def get_gdp_contrib(self):
        '''
        功能：
            三大产业贡献率

        参数说明：

        结果返回的数据属性说明如下：

            year :统计年度
            gdp_yoy :国内生产总值
            pi :第一产业献率(%)
            si :第二产业献率(%)
            industry:其中工业献率(%)
            ti :第三产业献率(%)
        '''
        try:
            df = ts.get_gdp_contrib()
            if df is None:
                return
            table = 'ts2_gdp_contrib'
            self.storeservice.insert_many(table, df, 'replace')
        except IOError as err:
            logging.error("OS|error: {0}".format(err))
        except OperationalError as err:
            logging.error("OS|error: {0}".format(err))
        else:
            pass

    @tick.clock()
    def get_cpi(self):
        '''
        功能：
            居民消费价格指数¶

        参数说明：

        结果返回的数据属性说明如下：

            month :统计月份
            cpi :价格指数
        '''
        try:
            df = ts.get_cpi()
            if df is None:
                return
            table = 'ts2_cpi'
            self.storeservice.insert_many(table, df, 'replace')
        except IOError as err:
            logging.error("OS|error: {0}".format(err))
        except OperationalError as err:
            logging.error("OS|error: {0}".format(err))
        else:
            pass

    @tick.clock()
    def get_ppi(self):
        '''
        功能：
            工业品出厂价格指数

        参数说明：

        结果返回的数据属性说明如下：

            month :统计月份
            ppiip :工业品出厂价格指数
            ppi :生产资料价格指数
            qm:采掘工业价格指数
            rmi:原材料工业价格指数
            pi:加工工业价格指数
            cg:生活资料价格指数
            food:食品类价格指数
            clothing:衣着类价格指数
            roeu:一般日用品价格指数
            dcg:耐用消费品价格指数
        '''
        try:
            df = ts.get_ppi()
            if df is None:
                return
            table = 'ts2_ppi'
            self.storeservice.insert_many(table, df,'replace')
        except IOError as err:
            logging.error("OS|error: {0}".format(err))
        except OperationalError as err:
            logging.error("OS|error: {0}".format(err))
        else:
            pass


    @tick.clock()
    def get_latest_news(self,top=5, show_content=True):
        '''
        功能：
            即时新闻


        参数说明：
            top:int，显示最新消息的条数，默认为80条
            show_content:boolean,是否显示新闻内容，默认False

        结果返回的数据属性说明如下：

            classify :新闻类别
            title :新闻标题
            time :发布时间
            url :新闻链接
            content:新闻内容（在show_content为True的情况下出现）

        '''
        df = None
        try:
            if time.time() - AppConfig.latest_news_pulltime > 1000:
                top = 80
            df = ts.get_latest_news(top, show_content)
            if df is None:
                logging.info('df is None')
                return
            table = 'ts2_latest_news'
            latest_pulltime = None
            pulltime = None
            dropindex = -1
            df.sort_values(by="time", ascending=False)
            for i in range(0,len(df)):
                pulltime = df.iloc[i]['time']
                pulltime = DateUtil.string_toTimestamp(DateUtil.format_date(pulltime))
                if i == 0:
                    latest_pulltime = pulltime
                if pulltime <= AppConfig.latest_news_pulltime:
                    #remove
                    dropindex = i
                    print('dropindex:',dropindex)
                    break
            if dropindex != -1:
                df = df.drop(range(dropindex,len(df),1))
            if len(df) > 0 :
                self.storeservice.insert_many(table, df)
                AppConfig.write_news_pulltime(latest_pulltime,True)
        except IOError as err:
            logging.error("OS|error: {0}".format(err))
        except OperationalError as err:
            logging.error("OS|error: {0}".format(err))
        else:
            pass

    def get_notices(self,code='600000', date='2018-06-15'):
        '''
        功能：
            信息地雷


        参数说明：
            code:股票代码
            date:信息公布日期

        结果返回的数据属性说明如下：

            title:信息标题
            type:信息类型
            date:公告日期
            url:信息内容URL
        '''
        return ts.get_notices()

    def get_guba_sina(self,show_content=False):
        '''
        功能：
            新浪股吧



        参数说明：
            show_content:boolean,是否显示内容，默认False

        结果返回的数据属性说明如下：

            title, 消息标题
            content, 消息内容（show_content=True的情况下）
            ptime, 发布时间
            rcounts,阅读次数
        '''
        return ts.guba_sina(show_content)

    def get_top_list(self,date='2018-06-15',retry_count=3, pause=0):
        '''
        功能：
            每日龙虎榜列表

        参数说明：

            date：日期，格式YYYY-MM-DD
            retry_count：当网络异常后重试次数，默认为3
            pause:重试时停顿秒数，默认为0

        结果返回的数据属性说明如下：

            title, 消息标题
            content, 消息内容（show_content=True的情况下）
            ptime, 发布时间
            rcounts,阅读次数
        '''
        return ts.top_list(date,retry_count,pause)

    def get_cap_tops(self,days=5,retry_count=3, pause=0):
        '''
        功能：
            个股上榜统计
            获取近5、10、30、60日个股上榜统计数据,包括上榜次数、累积购买额、累积卖出额、净额、买入席位数和卖出席位数。

        参数说明：

            days：统计周期5、10、30和60日，默认为5日
            retry_count：当网络异常后重试次数，默认为3
            pause:重试时停顿秒数，默认为0

        结果返回的数据属性说明如下：

            code：代码
            name:名称
            count：上榜次数
            bamount：累积购买额(万)
            samount：累积卖出额(万)
            net：净额(万)
            bcount：买入席位数
            scount：卖出席位数
        '''
        return ts.cap_tops(days,retry_count,pause)

    def get_broker_tops(self,days=5,retry_count=3, pause=0):
        '''
        功能：
            营业部上榜统计
            获取营业部近5、10、30、60日上榜次数、累积买卖等情况。

        参数说明：

            days：统计周期5、10、30和60日，默认为5日
            retry_count：当网络异常后重试次数，默认为3
            pause:重试时停顿秒数，默认为0

        结果返回的数据属性说明如下：

            broker：营业部名称
            count：上榜次数
            bamount：累积购买额(万)
            bcount：买入席位数
            samount：累积卖出额(万)
            scount：卖出席位数
            top3：买入前三股票
        '''
        return ts.broker_tops(days,retry_count,pause)

    def get_inst_tops(self,days=5,retry_count=3, pause=0):
        '''
        功能：
            个股上榜统计
            获取近5、10、30、60日个股上榜统计数据,包括上榜次数、累积购买额、累积卖出额、净额、买入席位数和卖出席位数。

        参数说明：

            days：统计周期5、10、30和60日，默认为5日
            retry_count：当网络异常后重试次数，默认为3
            pause:重试时停顿秒数，默认为0

        结果返回的数据属性说明如下：

            code:代码
            name:名称
            bamount:累积买入额(万)
            bcount:买入次数
            samount:累积卖出额(万)
            scount:卖出次数
            net:净额(万)
        '''
        return ts.inst_tops(days,retry_count,pause)

    def get_inst_detail(self,retry_count=3, pause=0):
        '''
        功能：
            个股上榜统计
            获取近5、10、30、60日个股上榜统计数据,包括上榜次数、累积购买额、累积卖出额、净额、买入席位数和卖出席位数。

        参数说明：

            retry_count：当网络异常后重试次数，默认为3
            pause:重试时停顿秒数，默认为0

        结果返回的数据属性说明如下：

            code:代码
            name:名称
            date:交易日期
            bamount:机构席位买入额(万)
            samount:机构席位卖出额(万)
            type:类型
        '''
        return ts.inst_detail(retry_count,pause)

