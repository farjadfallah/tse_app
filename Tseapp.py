
from DataProvider import DataProvider
from MarketInfo import MarketInfo
from Portfolio import Portfolio
from Filter import *
class Tseapp:
    def __init__(self):
        self.data_provider = DataProvider()
        self.market_info = MarketInfo()
        self.portfolio = Portfolio()
        self.cc_filter = Covered_Call_filter(55, 5, 5)
        self.data_provider.get_info(self.market_info)

        self.market_info.apply_filter(self.cc_filter)


        self.portfolio.add_share(self.market_info.find_stock_with_name("اهرم"),1000)
        self.portfolio.add_put(self.market_info.find_option_with_name("طهرم5003"),1000)
        self.portfolio.add_call(self.market_info.find_option_with_name("ضهرم5003"),-1000)
        self.portfolio.plot_chart(.8,2500)
