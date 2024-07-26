
from DataProvider import DataProvider
from MarketInfo import MarketInfo
from Portfolio import Portfolio
from Filter import *
class Tseapp:
    def __init__(self):
        self.data_provider = DataProvider()
        self.market_info = MarketInfo()
        self.portfolio7 = Portfolio()
        self.portfolio6 = Portfolio()
        self.portfolio5 = Portfolio()
        self.cc_filter_high = Covered_Call_filter(90, -7, 5)
        self.cc_filter_med = Covered_Call_filter(50, 2, 5)
        self.arbirage_filter = Aribitrage_Filter(0, -1, 30)
        self.data_provider.get_info(self.market_info)

        self.optimize_arbitrage_5003 = Optimize_Arbitrage_Filter(0, 0, 0, self.market_info.find_option_with_name("ضهرم5003"))
        self.market_info.apply_filter(self.cc_filter_high)
        self.market_info.apply_filter(self.cc_filter_med)
        self.market_info.apply_filter(self.arbirage_filter)
        self.market_info.apply_filter(self.optimize_arbitrage_5003)


        self.portfolio5.add_share(self.market_info.find_stock_with_name("اهرم"),32000)
        self.portfolio5.add_call(self.market_info.find_option_with_name("ضهرم5004"),-32000)
        # self.portfolio5.add_call(self.market_info.find_option_with_name("ضهرم5003"),-18000)
        # # self.portfolio5.add_call(self.market_info.find_option_with_name("ضهرم5004"),10000)
        # self.portfolio5.add_put(self.market_info.find_option_with_name("طهرم5002"),14000)
        # self.portfolio5.add_put(self.market_info.find_option_with_name("طهرم5003"),4000)
        # self.portfolio5.plot_chart(.7,20000)



    def get_arbitrage_filter(self, min_return, min_days_to_mature, min_roi):
        the_filter = Aribitrage_Filter(min_return, min_days_to_mature, min_roi)
        self.market_info.reset_informations()
        self.data_provider.get_info(self.market_info)
        results = self.market_info.apply_filter(the_filter)
        return results
