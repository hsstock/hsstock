# -*- coding: utf-8 -*-

import unittest
from tests.service.test_quote_service import QuoteServiceTestCase
from tests.service.test_trade_service import TradeServiceTestCase

if __name__ == '__main__':
    suite = unittest.TestCase()

    suite.addTests(unittest.TestLoader().loadTestsFromNames(['TradeServiceTestCase','QuoteServiceTestCase']))

    with open('UnittestTextReport.txt','w+') as f:
        runner = unittest.TextTestRunner(stream=f, verbosity=2)
        runner.run(suite)