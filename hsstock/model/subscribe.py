# -*- coding: UTF-8 -*-

from datetime import datetime, timedelta

class SubItem(object):
    def __init__(self, stock_code, data_type):
        '''
        :param stock_code:  需要订阅的股票代码
        :param data_type: 需要订阅的数据类型
        :param subt_ime: 订阅时间
        '''
        self.stock_code = stock_code
        self.data_type = data_type
        self.sub_time = datetime.now()

    def __hash__(self):
        return hash((self.stock_code, self.data_type))

    def stringHash(self):
        '''
        Generates an integer key from a sting
        :return:
        '''
        item = self.stock_code + self.data_type

        if len(item) > 4 and (item[0].islower() or item[0].isupper()):
            item = item[1:]
        sum = 0
        for ch in item:
            sum += ord(ch)
        if len(item) > 2:
            sum -= 2* ord(item[-1]) # Subtract last ASCII
        return sum

    def __eq__(self, other):
        return self.stock_code == other.stock_ode & self.data_type == other.data_type



if __name__ == "__main__":
    item = SubItem('US.AAPL', 'QUOTE')
    subdict = {}
    subdict[item.stringHash()] = item
    print(subdict.items())

    item = SubItem('US.NTES', 'QUOTE')
    subdict[item.stringHash()] = item
    print(subdict.items())

    subdict.pop(item.stringHash())
    print(subdict.items())

    item = SubItem('US.AAPL', 'QUOTE')
    ret = item.stringHash() in subdict
    print( ret )

    item = SubItem('US.AAPL2', 'QUOTE')

    ret = item.stringHash() in subdict
    print(ret)


