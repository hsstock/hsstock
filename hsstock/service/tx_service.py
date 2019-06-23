import requests
import random
import hashlib
import pandas as pd
import six as six
import numpy as np

from hsstock.service.mysql_service import MysqlService
from hsstock.utils.date_util import DateUtil
from hsstock.utils.date_util import *


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
                    # 开始数据解析
                    self._gen_warp_df(warp_self, symbol)
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
    def _gen_warp_df(self, warp_self, symbol):
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
class TXParser(object):
    """tx数据源解析类，被类装饰器HSDataParseWrap装饰"""

    def __init__(self, market, symbol, sub_market, json_dict):
        """
        :param symbol: 请求的symbol str对象
        :param sub_market: 子市场（交易所）类型
        :param json_dict: 请求返回的json数据
        """
        if json_dict['code'] == 0:
            if market == 'us':
                data = json_dict['data'][market+symbol + sub_market]
            else:
                data = json_dict['data'][symbol]

            if 'qfqday' in data.keys():
                data = data['qfqday']
            else:
                data = data['day']

            # 为HSDataParseWrap准备类必须的属性序列
            if len(data) > 0:
                # 时间日期序列，时间格式为2017-07-26格式字符串
                self.time_key = [item[0] for item in data]
                # 开盘价格序列
                self.open = [item[1] for item in data]
                # 收盘价格序列
                self.close = [item[2] for item in data]
                # 最高价格序列
                self.high = [item[3] for item in data]
                # 最低价格序列
                self.low = [item[4] for item in data]
                # 成交量序列
                self.volume = [item[5] for item in data]
                # 代码
                code = str.upper(market) + '.' + symbol
                self.code = [code for _ in data]


def _create_random_tmp(salt_count, seed):
    """
    从seed种子字符池中随机抽取salt_count个字符，返回生成字符串,
    注意抽取属于有放回抽取方法
    :param salt_count: 生成的字符序列的长度
    :param seed: 字符串对象，做为生成序列的种子字符池
    :return: 返回生成字符串
    """
    # TODO random.choice有放回抽取方法, 添加参数支持无放回抽取模式
    sa = [random.choice(seed) for _ in range(salt_count)]
    salt = ''.join(sa)
    return salt

def create_random_with_num_low(salt_count):
    """
    种子字符池 = "abcdefghijklmnopqrstuvwxyz0123456789",
    从种子字符池中随机抽取salt_count个字符, 返回生成字符串,
    :param salt_count: 生成的字符序列的长度
    :return: 返回生成字符串
    """
    seed = "abcdefghijklmnopqrstuvwxyz0123456789"
    return _create_random_tmp(salt_count, seed)

def random_from_list(array):
    """从参数array中随机取一个元素"""
    # 在array长度短的情况下，测试比np.random.choice效率要高
    return array[random.randrange(0, len(array))]

def _create_random_tmp(salt_count, seed):
    """
    从seed种子字符池中随机抽取salt_count个字符，返回生成字符串,
    注意抽取属于有放回抽取方法
    :param salt_count: 生成的字符序列的长度
    :param seed: 字符串对象，做为生成序列的种子字符池
    :return: 返回生成字符串
    """
    # TODO random.choice有放回抽取方法, 添加参数支持无放回抽取模式
    sa = [random.choice(seed) for _ in range(salt_count)]
    salt = ''.join(sa)
    return salt

def create_random_with_num(salt_count):
    """
    种子字符池 = "0123456789", 从种子字符池中随机抽取salt_count个字符, 返回生成字符串,
    :param salt_count: 生成的字符序列的长度
    :return: 返回生成字符串
    """
    seed = "0123456789"
    return _create_random_tmp(salt_count, seed)

def _md5_obj():
    """根据python版本返回md5实例"""
    md5_obj = hashlib.md5()
    return md5_obj

def md5_from_binary(binary):
    """对字符串进行md5, 返回md5后32位字符串对象"""
    m = _md5_obj()
    m.update(binary.encode('utf-8'))
    return m.hexdigest()

class TXService(object):

    K_NET_BASE = "http://ifzq.gtimg.cn/appstock/app/%sfqkline/get?p=1&param=%s,day,,,%d," \
                 "qfq&_appName=android&_dev=%s&_devId=%s&_mid=%s&_md5mid=%s&_appver=4.2.2&_ifChId=303&_screenW=%d" \
                 "&_screenH=%d&_osVer=%s&_uin=10000&_wxuin=20000&__random_suffix=%d"

    K_DEV_MODE_LIST = ["A0001", "OPPOR9", "OPPOR9", "VIVOX5",
                       "VIVOX6", "VIVOX6PLUS", "VIVOX9", "VIVOX9PLUS"]
    # 预先设置模拟手机请求的os version
    K_OS_VERSION_LIST = ["4.3", "4.2.2", "4.4.2", "5.1.1"]

    def __init__(self):
        self.storeservice = MysqlService()



    def get_history_data(self,code,days):
        dev_mod = random_from_list(TXService.K_DEV_MODE_LIST)
        os_ver = random_from_list(TXService.K_OS_VERSION_LIST)
        width=1080
        height=1920
        market='us'
        sub_market='.oq'
        symbol='TSLA'
        cuid = create_random_with_num_low(40)

        cuid_md5 = md5_from_binary(cuid)

        random_suffix = create_random_with_num(5)


        url = TXService.K_NET_BASE % ( \
                market, market+symbol+sub_market, days, \
                dev_mod, cuid, cuid, cuid_md5, width, height, os_ver, int(random_suffix, 10))


        resp = requests.get(url)

        kl_pd = TXParser('us',code,'.oq', resp.json()).df

        if kl_pd is not None and len(kl_pd) > 0:
            table = 'ft4_kline'
            tindex = self.storeservice.find_tindex(code, 'hk')
            if tindex != -1:
                table += ('_' + str(tindex))
            table = 'ft_kline_1_1'
            lastdate = kl_pd['time_key'][len(kl_pd)-1]
            self.storeservice.insert_many(table, kl_pd, 'append')

            print(lastdate)

            return lastdate

        return None

if __name__ == '__main__':
    tx = TXService()
    tx.get_history_data('.DJUSBS',300)


