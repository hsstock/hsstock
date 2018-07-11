# -*- coding: utf-8 -*-
"""
    query_history_change_stocks
    指定涨跌幅，查询本地下载的历史日k数据，返回符合条件的股票
"""

from hsstock.futuquant.quote.open_quote_context import *
from datetime import datetime, timedelta


class QueryHistory(object):

    def __init__(self, quote_ctx):
        self.quote_context =  quote_ctx

    def query_history_change_stocks(self, markets=['HK'], start='2017-01-05', end='2017-12-30', change_min=5.0,
                                change_max=None, stock_type='STOCK', ascend=True):
        '''
        :param markets: 要查询的市场列表, 可以只传单个市场如'HK'字符串
        :param start: 开始时间
        :param end: 截止时间
        :param change_min: 涨跌幅最小值 eg: 1.0% 传值 1.0, None表示忽略
        :param change_max: 涨跌幅最大值
        :param stock_type: 要查询的股票类型, 见 SEC_TYPE_MAP - 'STOCK','IDX','ETF','WARRANT','BOND'
        :param ascend: 结果是否升序排列
        :return: (ret, data), ret == 0返回pd dataframe, 表头为 'code'(股票代码), 'change_rate'(涨跌率*100), 'real_times'(起止真实交易时间字符串)
                              ret != 0 data 为错误字符串
        '''
        if not markets or (not is_str(markets) and not isinstance(markets, list)):
            error_str = "the type of markets param is wrong"
            return RET_ERROR, error_str
        req_markets = markets if isinstance(markets, list) else [markets]

        if change_min is None and change_max is None:
            return RET_ERROR, "param change is wrong"

        # float 比较有偏差 比如 a = 1.0 , b = 1.1, c = (b-a)/a * 100, d = 10 ,  c<=d 结果为False
        if change_min is not None:
            change_min = int(float(change_min) * 1000)
        if change_max is not None:
            change_max = int(float(change_max) * 1000)

        # 汇总得到需要查询的所有股票code
        list_stocks = []
        for mk in req_markets:
            ret, data = self.quote_context.get_stock_basicinfo(mk, stock_type)
            if 0 != ret:
                return ret, data
            for ix, row in data.iterrows():
                list_stocks.append(row['code'])

        # 多点k线数据查询
        dt_last = datetime.now()
        ret_list = []
        ret, data_start = self.quote_context.get_multi_points_history_kline(list_stocks, [start],
                                                                 [KL_FIELD.DATE_TIME, KL_FIELD.CLOSE], 'K_DAY', 'None',
                                                                       KL_NO_DATA_MODE_BACKWARD)
        if ret != 0:
            return ret, data_start
        ret, data_end = self.quote_context.get_multi_points_history_kline(list_stocks, [end],
                                                                 [KL_FIELD.DATE_TIME, KL_FIELD.CLOSE], 'K_DAY', 'None',
                                                                 KL_NO_DATA_MODE_FORWARD)
        if ret != 0:
            return ret, data_end

        # 合并数据
        data = data_start.append(data_end)

        dt = datetime.now() - dt_last
        print('get_multi_points_history_kline - run time = %s秒' % dt.seconds)

        # 返回计算涨跌幅，统计符合条件的股票
        for stock in list_stocks:
            pd_find = data[data.code == stock]
            close_start = 0
            close_end = 0
            real_times = []
            for _, row in pd_find.iterrows():
                if 0 == row['data_valid']:
                    break
                if row['time_point'] == start:
                    close_start = row['close']
                    real_times.append(row['time_key'])
                elif row['time_point'] == end:
                    close_end = row['close']
                    real_times.append(row['time_key'])
            if close_start and close_end:
                change_rate = (close_end - close_start) / float(close_start) * 100000.0
                data_ok = True
                if change_min is not None:
                    data_ok = change_rate >= change_min
                if data_ok and change_max is not None:
                    data_ok = change_rate <= change_max
                if data_ok:
                    ret_list.append({'code': stock, 'change_rate':  float(change_rate / 1000.0), 'real_times': ','.join(real_times),'close_start': close_start,'close_end': close_end})

        # 数据排序
        ret_list = sorted(ret_list, key=lambda x: x['change_rate'], reverse=(not ascend))

        # 组装返回pdframe数据
        col_list = ['code', 'change_rate', 'real_times','close_start','close_end']
        pd_frame = pd.DataFrame(ret_list, columns=col_list)

        return RET_OK, pd_frame



    def export_csv_k1m_file(self, code, start='2017-11-01', end=None):
        '''
        :param code: futu 股票代码 eg HK.00700 / US.AAPL
        :param start:历史数据起始时间
        :param end: 历史数据结束时间
        :return: 0 = 成功 , 其它失败
        '''
        # 得到历史数据
        kl_fileds = [KL_FIELD.DATE_TIME, KL_FIELD.OPEN, KL_FIELD.CLOSE, KL_FIELD.HIGH, KL_FIELD.LOW, KL_FIELD.TRADE_VOL]
        ret, ret_data = self.quote_context.get_history_kline(code, start, end, 'K_1M', 'qfq', kl_fileds)

        if 0 != ret:
            print(ret_data)
            return ret

        # 增加一列，并修改原列名
        ret_data['Date'] = ret_data['time_key']
        ret_data.rename(columns={'time_key': 'Time', 'open': 'Open', 'close': 'Close', 'high': 'High', 'low': 'Low',
                                 'volume': 'TotalVolume'}, inplace=True)
        # 修改Date/Time 列数据
        for ix, row in ret_data.iterrows():
            date_time = str(row['Date'])
            date, time = date_time.split(' ')
            ret_data.loc[ix, 'Date'] = date
            ret_data.loc[ix, 'Time'] = time

        print(ret_data)
        # 保存到csv文件中
        code_name = copy(code)
        csv_file = code_name + '_1min.csv'
        ret_data.to_csv(csv_file, index=False, sep=',',
                        columns=['Date', 'Time', 'Open', 'High', 'Low', 'Close', 'TotalVolume'])
        return RET_OK

    if __name__ == "__main__":
        # 参数配置
        ip = '10.242.45.130'
        port = 11111
        code = 'US.NTES'  # 腾讯
        quote_context = OpenQuoteContext(ip, port)

        # 导出csv文件数据
        export_csv_k1m_file(quote_context, code, '2018-04-01', '2018-05-23')

        # 正常关闭对象
        quote_context.close()




