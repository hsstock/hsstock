# -*- coding: UTF-8 -*-
import time

from hsstock.common.constant import *
from hsstock.utils.lang_util import *

class FreqItem(object):
    def __init__(self, limitnumber, lasttime):
        '''
        :param limitnumber: 某函数的限制次数
        :param lasttime: 最后调用时间
        '''
        self.limitnumber = limitnumber
        self.lasttime = lasttime
        self.use_number = 0 # 当前周期内已经调用次数

    def __hash__(self):
        return hash((self.act))

@Singleton
class FreqLimit(object):

    def __init__(self):
        self.limits = {}
        self.limits[FREQ.UNLOCK_TRADE] = FreqItem(FREQLIMIT[FREQ.UNLOCK_TRADE], 0)
        self.limits[FREQ.PLACE_ORDER] = FreqItem(FREQLIMIT[FREQ.PLACE_ORDER], 0)
        self.limits[FREQ.MODIFY_ORDER] = FreqItem(FREQLIMIT[FREQ.MODIFY_ORDER], 0)
        self.limits[FREQ.CHANGE_ORDER] = FreqItem(FREQLIMIT[FREQ.CHANGE_ORDER], 0)
        self.limits[FREQ.HISTORY_DEAL_LIST_QUERY] = FreqItem(FREQLIMIT[FREQ.HISTORY_DEAL_LIST_QUERY], 0)
        self.limits[FREQ.HISTORY_ORDER_LIST_QUERY] = FreqItem(FREQLIMIT[FREQ.HISTORY_ORDER_LIST_QUERY], 0)
        self.limits[FREQ.GET_MARKET_SNAPSHOT] = FreqItem(FREQLIMIT[FREQ.GET_MARKET_SNAPSHOT], 0)
        self.limits[FREQ.GET_PLATE_LIST] = FreqItem(FREQLIMIT[FREQ.GET_PLATE_LIST], 0)
        self.limits[FREQ.GET_PLATE_STOCK] = FreqItem(FREQLIMIT[FREQ.GET_PLATE_STOCK], 0)
        self.limits[FREQ.TOTAL_SECONDS] = FreqItem(FREQLIMIT[FREQ.TOTAL_SECONDS], 0)


    def rate_limit(self,act):
        """

        :param act: 函数名称
        :return:  True 限制调用， False 不限制
        """
        t = time.time()
        t = int(t)
        if self.limits[act].lasttime == 0:
            self.limits[act].lasttime = t
            self.limits[act].use_number += 1
        else:
            if (t - self.limits[act].lasttime) > FREQLIMIT[FREQ.TOTAL_SECONDS]:
                self.limits[act].lasttime = 0
                self.limits[act].use_number = 1
            else:
                if self.limits[act].use_number < self.limits[act].limitnumber:
                    self.limits[act].use_number += 1
                else:
                    return True
        return False

