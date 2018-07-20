# -*- coding: utf-8 -*-

__author__ = 'allen.hu'

class Environment(object):
    def __init__(self):
        self.trading_days = {}      # {'market':['2017-07-20,today']}
        self.stock_basicinfos = {}  # {'market_securitytype':df}
        self.plates = {}            # {'market':df}
        self.plate_stocks = {}      # {'plate_code':df}
        self.global_state = {}      # {}
        self.accs = None            # df
        self.account_info_real = None       # df
        self.account_info_simulate = None   # df
        self.account_info_positions = None  # df
        self.curr_order = None              # df
        self.orders  = None                 # df
        self.deals = None                   # df





