
from DataProvider import DataProvider
from MarketInfo import MarketInfo
from Portfolio import Portfolio
from Filter import *
from OpenPositions import *
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
        self.protective_put = Protective_Put_Filter(-10,10,0,-10)
        self.open_postion_record = OpenPostionsRecords()
        self.open_postion_record.add_covered_call(Covered_Call_Position_Record(self.market_info.find_option_with_name('ضهرم7026'),3996,19955,10000,94))
        self.open_postion_record.add_covered_call(Covered_Call_Position_Record(self.market_info.find_option_with_name('ضهرم7025'),2250,16710,6000,77))
        self.open_postion_record.get_current_state()

        self.market_info.apply_filter(self.protective_put)


    def get_arbitrage_filter(self, min_return, min_days_to_mature, min_roi):
        the_filter = Aribitrage_Filter(min_return, min_days_to_mature, min_roi)
        self.market_info.reset_informations()
        self.data_provider.get_info(self.market_info)
        results = self.market_info.apply_filter(the_filter)
        
        return results

    def get_covered_call_filter(self, max_risk,min_days_to_mature,min_ROI):
        the_filter = Covered_Call_filter(min_ROI, max_risk, min_days_to_mature)
        self.market_info.reset_informations()
        self.data_provider.get_info(self.market_info)
        results = self.market_info.apply_filter(the_filter)
        return results
    

    def get_protective_put_filter(self, min_dif,max_dif, min_ROI,min_days_to_mature):
        the_filter = Protective_Put_Filter(min_dif,max_dif,min_days_to_mature,min_ROI)
        self.market_info.reset_informations()
        self.data_provider.get_info(self.market_info)
        results = self.market_info.apply_filter(the_filter)
        return results
