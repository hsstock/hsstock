import requests
import random
import hashlib
import pandas as pd
import six as six
import numpy as np

from hsstock.service.mysql_service import MysqlService
from hsstock.utils.date_util import DateUtil

def date_str_to_int(date_str, split='-', fix=True):
    """
    eg. 2016-01-01 -> 20160101
    不使用时间api，直接进行字符串解析，执行效率高
    :param date_str: %Y-%m-%d形式时间str对象
    :param split: 年月日的分割符，默认'-'
    :param fix: 是否修复日期不规范的写法，eg. 2016-1-1 fix 2016-01-01
    :return: int类型时间
    """
    if fix and split == '-':
        # 只针对%Y-%m-%d形式格式标准化日期格式
        date_str = fix_date(date_str)
    string_date = date_str.replace(split, '')
    return int(string_date)


def fix_date(date_str):
    """
    修复日期不规范的写法:
                eg. 2016-1-1 fix 2016-01-01
                eg. 2016:01-01 fix 2016-01-01
                eg. 2016,01 01 fix 2016-01-01
                eg. 2016/01-01 fix 2016-01-01
                eg. 2016/01/01 fix 2016-01-01
                eg. 2016/1/1 fix 2016-01-01
                eg. 2016:1:1 fix 2016-01-01
                eg. 2016 1 1 fix 2016-01-01
                eg. 2016 01 01 fix 2016-01-01
                .............................
    不使用时间api，直接进行字符串解析，执行效率高，注意fix_date内部会使用fmt_date
    :param date_str: 检测需要修复的日期str对象或者int对象
    :return: 修复了的日期str对象
    """
    if date_str is not None:
        # 如果是字符串先统一把除了数字之外的都干掉，变成干净的数字串
        if isinstance(date_str, six.string_types):
            # eg, 2016:01-01, 201601-01, 2016,01 01, 2016/01-01 -> 20160101
            date_str = ''.join(list(filter(lambda c: c.isdigit(), date_str)))
        # 再统一确定%Y-%m-%d形式
        date_str = fmt_date(date_str)
        y, m, d = date_str.split('-')
        if len(m) == 1:
            # 月上补0
            m = '0{}'.format(m)
        if len(d) == 1:
            # 日上补0
            d = '0{}'.format(d)
        date_str = "%s-%s-%s" % (y, m, d)
    return date_str

def fmt_date(convert_date):
    """
    将时间格式如20160101转换为2016-01-01日期格式, 注意没有对如 201611
    这样的做fix适配，外部需要明确知道参数的格式，针对特定格式，不使用时间api，
    直接进行字符串解析，执行效率高
    :param convert_date: 时间格式如20160101所示，int类型或者str类型对象
    :return: %Y-%m-%d日期格式str类型对象
    """
    if isinstance(convert_date, float):
        # float先转换int
        convert_date = int(convert_date)
    convert_date = str(convert_date)

    if len(convert_date) > 8 and convert_date.startswith('20'):
        # eg '20160310000000000'
        convert_date = convert_date[:8]

    if '-' not in convert_date:
        if len(convert_date) == 8:
            # 20160101 to 2016-01-01
            convert_date = "%s-%s-%s" % (convert_date[0:4],
                                         convert_date[4:6], convert_date[6:8])
        elif len(convert_date) == 6:
            # 201611 to 2016-01-01
            convert_date = "%s-0%s-0%s" % (convert_date[0:4],
                                           convert_date[4:5], convert_date[5:6])
        else:
            raise ValueError('fmt_date: convert_date fmt error {}'.format(convert_date))
    return convert_date

class HSDataParseWrap(object):
    """
        做为类装饰器封装替换解析数据统一操作，装饰替换init
    """

    def __call__(self, cls):
        """只做为数据源解析类的装饰器，统一封装通用的数据解析规范及流程"""
        if isinstance(cls, six.class_types):
            # 只做为类装饰器使用
            init = cls.__init__

            def wrapped(*args, **kwargs):
                try:
                    # 拿出被装饰的self对象
                    warp_self = args[0]
                    warp_self.df = None
                    # 调用原始init
                    init(*args, **kwargs)
                    symbol = args[1]
                    start = args[2]
                    # 开始数据解析
                    self._gen_warp_df(warp_self, symbol, start)
                except Exception as e:
                    print(e)
                    #logging.exception(e)

            # 使用wrapped替换原始init
            cls.__init__ = wrapped

            wrapped.__name__ = '__init__'
            # 将原始的init赋予deprecated_original，必须要使用这个属性名字，在其它地方，如HSParamBase会寻找原始方法找它
            wrapped.deprecated_original = init
            return cls
        else:
            raise TypeError('HSDataParseWrap just for class warp')

    # noinspection PyMethodMayBeStatic
    def _gen_warp_df(self, warp_self, symbol,start):
        """
        封装通用的数据解析规范及流程
        :param warp_self: 被封装类init中使用的self对象
        :param symbol: 请求的symbol str对象
        :return:
        """

        # 规范原始init函数中必须为类添加了如下属性
        must_col = ['code','open', 'close', 'high', 'low', 'volume', 'time_key']
        # 检测所有的属性都有
        all_has = all([hasattr(warp_self, col) for col in must_col])
        if all_has:
            # 将时间序列转换为pd时间
            dates_pd = pd.to_datetime(warp_self.time_key)
            # 构建df，index使用dates_pd
            warp_self.df = pd.DataFrame(index=dates_pd)
            for col in must_col:
                # 所以必须有的类属性序列设置给df的列
                warp_self.df[col] = getattr(warp_self, col)

            # 从收盘价格序列shift出昨收价格序列
            warp_self.df['last_close'] = warp_self.df['close'].shift(1)
            warp_self.df.drop(warp_self.df[warp_self.df.last_close.isnull()].index, inplace=True)

            warp_self.df.drop(warp_self.df[warp_self.df.time_key < start].index, inplace=True)

            # 添加日期int列
            warp_self.df['time_key'] = warp_self.df['time_key'].apply(lambda x: DateUtil.string_toDate(x))
            # 添加周几列date_week，值为0-4，分别代表周一到周五
#             warp_self.df['date_week'] = warp_self.df['date'].apply(
#                 lambda x: week_of_date(str(x), '%Y%m%d'))

            # 类型转换
            warp_self.df['close'] = warp_self.df['close'].astype(float)
            warp_self.df['high'] = warp_self.df['high'].astype(float)
            warp_self.df['low'] = warp_self.df['low'].astype(float)
            warp_self.df['open'] = warp_self.df['open'].astype(float)
            warp_self.df['volume'] = warp_self.df['volume'].astype(float)
            warp_self.df['volume'] = warp_self.df['volume'].astype(np.int64)
            warp_self.df['last_close'] = warp_self.df['last_close'].astype(float)
            # noinspection PyTypeChecker
            warp_self.df['change_rate'] = np.where(warp_self.df['last_close'] == 0, 0,
                                                (warp_self.df['close'] - warp_self.df['last_close']) / warp_self.df[
                                                    'last_close'] * 100)

            warp_self.df['change_rate'] = warp_self.df['change_rate'].apply(lambda x: round(x, 3))
            # 给df加上name
            warp_self.df.name = symbol


@HSDataParseWrap()
class SNUSParser(object):
    """snus数据源解析类，被类装饰器AbuDataParseWrap装饰"""

    # noinspection PyUnusedLocal
    def __init__(self, symbol, start, json_dict):
        """
        :param symbol: 请求的symbol str对象
        :param start: 开始日期
        :param json_dict: 请求返回的json数据
        """
        data = json_dict
        # 为AbuDataParseWrap准备类必须的属性序列
        if len(data) > 0:
            # 时间日期序列
            self.time_key = [item['d'] for item in data]
            # 开盘价格序列
            self.open = [item['o'] for item in data]
            # 收盘价格序列
            self.close = [item['c'] for item in data]
            # 最高价格序列
            self.high = [item['h'] for item in data]
            # 最低价格序列
            self.low = [item['l'] for item in data]
            # 成交量序列
            self.volume = [item['v'] for item in data]
            # 代码
            code = 'US.' + symbol
            self.code = [code for _ in data]



class SNService(object):

    K_NET_BASE = "http://stock.finance.sina.com.cn/usstock/api/json_v2.php/US_MinKService.getDailyK?" \
                 "symbol=%s&___qn=3n"

    TIME_OUT = (10, 60)

    def __init__(self):
        self.storeservice = MysqlService()



    def get_history_data(self,code,start, days):

        url = SNService.K_NET_BASE % code


        resp = requests.get(url,timeout=SNService.TIME_OUT)

        kl_pd = SNUSParser(code,start,resp.json()).df

        if kl_pd is not None and len(kl_pd) > 0:
            table = 'ft_kline'
            tindex = self.storeservice.find_tindex(code, 'hk')
            if tindex != -1:
                table += ('_' + str(tindex))
            #table = 'ft_kline_1_1'
            lastdate = kl_pd['time_key'][len(kl_pd)-1]
            self.storeservice.insert_many(table, kl_pd, 'append')
            print(lastdate)
            return lastdate
        else:
            return None


if __name__ == '__main__':
    tx = SNService()
    tx.get_history_data('PHB',300)


