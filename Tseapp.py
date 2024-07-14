
from DataProvider import DataProvider
from MarketInfo import MarketInfo
from Portfolio import Portfolio
from Filter import *
class Tseapp:
    def __init__(self):
        self.data_provider = DataProvider()
        self.market_info = MarketInfo()
        self.portfolio = Portfolio()
        self.cc_filter_high = Covered_Call_filter(90, -3, 5)
        self.cc_filter_med = Covered_Call_filter(60, 3, 5)
        self.arbirage_filter = Aribitrage_Filter( 2.9 , -1, 0)
        self.data_provider.get_info(self.market_info)


        self.market_info.apply_filter(self.cc_filter_high)
        self.market_info.apply_filter(self.cc_filter_med)
        self.market_info.apply_filter(self.arbirage_filter)


        # self.portfolio.add_share(self.market_info.find_stock_with_name("اهرم"),1000)
        self.portfolio.add_call(self.market_info.find_option_with_name("ضهرم5002"),2000)
        self.portfolio.add_call(self.market_info.find_option_with_name("ضهرم5005"),-4000)

        print(self.portfolio.get_value_at_price(20000, 100))
        print(self.portfolio.get_total_cost()/10)
        self.portfolio.plot_chart(.7,20000)

