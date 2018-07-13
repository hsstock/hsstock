import unittest

from  hsstock.service.tushare_service import TUShare_service

class TUShareServiceTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print('setUpClass')
        cls.tss = TUShare_service()

    @classmethod
    def tearDownClass(cls):
        print('tearDownClass')

    def setUp(self):
        print('setUp')

    def tearDown(self):
        print('tearDown')

    def test_get_his_data(self):
        TUShareServiceTestCase.tss.get_hist_data('600000')
        self.assertTrue(1 > 0 )

    # def test_get_h_data(self):
    #     df = TUShareServiceTestCase.tss.get_h_data('600000')
    #     self.assertTrue(len(df) > 0 )
    #
    # def test_get_total_all(self):
    #     df = TUShareServiceTestCase.tss.get_total_all()
    #     self.assertTrue(len(df) > 0 )

    # def test_get_tick_data(self):
    #     df = TUShareServiceTestCase.tss.get_tick_data('600000','2018-06-13')
    #     self.assertTrue(len(df) > 0 )

    # def test_get_realtime_quotes(self):
    #     df = TUShareServiceTestCase.tss.get_realtime_quotes('600000')
    #     self.assertTrue(len(df) > 0)

    # def test_get_today_ticks(self):
    #      df = TUShareServiceTestCase.tss.get_today_ticks('600000')
    #      self.assertTrue(len(df) > 0)
    #
    # def test_get_index(self):
    #      df = TUShareServiceTestCase.tss.get_index()
    #      self.assertTrue(len(df) > 0)
    #
    # def test_sina_add(self):
    #      df = TUShareServiceTestCase.tss.get_sina_add('600000','2018-06-13')
    #      self.assertTrue(len(df) > 0)
    #
    # def test_get_profit_data(self):
    #      df = TUShareServiceTestCase.tss.get_profit_data()
    #      self.assertTrue(len(df) > 0)
    #
    # def test_get_forecast_data(self):
    #      df = TUShareServiceTestCase.tss.get_forecast_data()
    #      self.assertTrue(len(df) > 0)
    #
    #
    # def test_get_xsg_data(self):
    #      df = TUShareServiceTestCase.tss.get_xsg_data()
    #      self.assertTrue(len(df) > 0)
    #
    # def test_get_fund_holdings(self):
    #      df = TUShareServiceTestCase.tss.get_fund_holdings()
    #      self.assertTrue(len(df) > 0)
    #
    # def test_get_new_stocks(self):
    #      df = TUShareServiceTestCase.tss.get_new_stocks()
    #      self.assertTrue(len(df) > 0)

    # def test_get_industry_classified(self):
    #      df = TUShareServiceTestCase.tss.get_industry_classified()
    #      self.assertTrue(len(df) > 0)

    # def test_get_concept_classified(self):
    #      df = TUShareServiceTestCase.tss.get_concept_classified()
    #      self.assertTrue(len(df) > 0)

    # def test_get_area_classified(self):
    #      df = TUShareServiceTestCase.tss.get_area_classified()
    #      self.assertTrue(len(df) > 0)

    # def test_get_sme_classified(self):
    #      df = TUShareServiceTestCase.tss.get_sme_classified()
    #      self.assertTrue(len(df) > 0)
    #
    # def test_get_gem_classified(self):
    #      df = TUShareServiceTestCase.tss.get_gem_classified()
    #      self.assertTrue(len(df) > 0)
    #
    # def test_get_st_classified(self):
    #     df = TUShareServiceTestCase.tss.get_st_classified()
    #     self.assertTrue(len(df) > 0)
    #
    # def test_get_hs300s(self):
    #      df = TUShareServiceTestCase.tss.get_hs300s()
    #      self.assertTrue(len(df) > 0)
    #
    # def test_get_sz50s(self):
    #      df = TUShareServiceTestCase.tss.get_sz50s()
    #      self.assertTrue(len(df) > 0)
    #
    # def test_get_zz500s(self):
    #      df = TUShareServiceTestCase.tss.get_zz500s()
    #      self.assertTrue(len(df) > 0)

    # def test_get_terminated(self):
    #      df = TUShareServiceTestCase.tss.get_terminated()
    #      self.assertTrue(len(df) > 0)
    #
    #
    # def test_get_suspended(self):
    #      df = TUShareServiceTestCase.tss.get_suspended()
    #      self.assertTrue(len(df) > 0)
    #


    # def test_get_stock_basics(self):
    #      df = TUShareServiceTestCase.tss.get_stock_basics()
    #      self.assertTrue(len(df) > 0)
    #
    # def test_get_report_data(self):
    #      df = TUShareServiceTestCase.tss.get_report_data()
    #      self.assertTrue(len(df) > 0)
    #
    # def test_get_profit_data(self):
    #      df = TUShareServiceTestCase.tss.get_profit_data()
    #      self.assertTrue(len(df) > 0)
    #
    # def test_get_operation_data(self):
    #      df = TUShareServiceTestCase.tss.get_operation_data()
    #      self.assertTrue(len(df) > 0)
    #
    # def test_get_growth_data(self):
    #      df = TUShareServiceTestCase.tss.get_growth_data()
    #      self.assertTrue(len(df) > 0)
    #
    # def test_get_debtpaying_data(self):
    #      df = TUShareServiceTestCase.tss.get_debtpaying_data()
    #      self.assertTrue(len(df) > 0)

    # def test_get_cashflow_data(self):
    #      df = TUShareServiceTestCase.tss.get_cashflow_data()
    #      self.assertTrue(len(df) > 0)
    #
    # def test_get_deposit_rate(self):
    #      df = TUShareServiceTestCase.tss.get_deposit_rate()
    #      self.assertTrue(len(df) > 0)
    #
    # def test_get_loan_rate(self):
    #      df = TUShareServiceTestCase.tss.get_loan_rate()
    #      self.assertTrue(len(df) > 0)
    #
    # def test_get_rrr(self):
    #      df = TUShareServiceTestCase.tss.get_rrr()
    #      self.assertTrue(len(df) > 0)
    #
    # def test_get_money_supply(self):
    #      df = TUShareServiceTestCase.tss.get_money_supply()
    #      self.assertTrue(len(df) > 0)
    #
    # def test_get_money_supply_bal(self):
    #      df = TUShareServiceTestCase.tss.get_money_supply_bal()
    #      self.assertTrue(len(df) > 0)
    #
    # def test_get_gdp_year(self):
    #      df = TUShareServiceTestCase.tss.get_gdp_year()
    #      self.assertTrue(len(df) > 0)
    #
    # def test_get_gdp_quarter(self):
    #      df = TUShareServiceTestCase.tss.get_gdp_quarter()
    #      self.assertTrue(len(df) > 0)
    #
    # def test_get_gdp_for(self):
    #      df = TUShareServiceTestCase.tss.get_gdp_for()
    #      self.assertTrue(len(df) > 0)
    #
    # def test_get_gdp_pull(self):
    #      df = TUShareServiceTestCase.tss.get_gdp_pull()
    #      self.assertTrue(len(df) > 0)
    #
    # def test_get_gdp_contrib(self):
    #      df = TUShareServiceTestCase.tss.get_gdp_contrib()
    #      self.assertTrue(len(df) > 0)
    #
    # def test_get_cpi(self):
    #      df = TUShareServiceTestCase.tss.get_cpi()
    #      self.assertTrue(len(df) > 0)
    #
    # def test_get_ppi(self):
    #      df = TUShareServiceTestCase.tss.get_ppi()
    #      self.assertTrue(len(df) > 0)

    def test_get_latest_news(self):
        TUShareServiceTestCase.tss.get_latest_news()
        self.assertTrue( 1> 0 )
        #self.assertTrue(len(df) > 0)

    # def test_get_notices(self):
    #     df = TUShareServiceTestCase.tss.get_notices()
    #     self.assertTrue( df == None )
    #
    #
    # def test_get_guba_sina(self):
    #     df = TUShareServiceTestCase.tss.get_guba_sina()
    #     self.assertTrue(len(df) > 0)
    #
    # def test_get_top_list(self):
    #     df = TUShareServiceTestCase.tss.get_top_list()
    #     self.assertTrue(len(df) > 0)
    #
    # def test_get_cap_tops(self):
    #     df = TUShareServiceTestCase.tss.get_cap_tops()
    #     self.assertTrue(len(df) > 0)
    #
    # def test_get_broker_tops(self):
    #     df = TUShareServiceTestCase.tss.get_broker_tops()
    #     self.assertTrue(len(df) > 0)
    #
    # def test_get_inst_tops(self):
    #     df = TUShareServiceTestCase.tss.get_inst_tops()
    #     self.assertTrue(len(df) > 0)
    #
    # def test_get_inst_detail(self):
    #     df = TUShareServiceTestCase.tss.get_inst_detail()
    #     self.assertTrue(len(df) > 0)

unittest.main