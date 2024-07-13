from Option import Option



class CallOption(Option):
    def __init__(self, _ticker, _strike, _u_asset, _maturity_date, _days_till_maturity, _best_kharid, _best_foroosh, _volume, _last_price):
        super().__init__(_ticker, _strike, _u_asset, _maturity_date, _days_till_maturity, _best_kharid, _best_foroosh, _volume, _last_price)
        self.vajh_tazmin = self.__cal_vajh_tazmin(self.u_asset.get_close_price() , self.strike, self.option_size)
    
    def get_value_at_price(self, final_price):
        return max(final_price - self.strike, 0)    

    def __cal_vajh_tazmin (self, ua_close, strike_price, op_size):
        zarib_gerd = 10000  
        op_loss = max(strike_price - ua_close, 0 ) * op_size
        firs_method = 0.2 * ua_close * op_size - op_loss
        second_method = 0.1 * strike_price * op_size
        final_value = max(firs_method, second_method)
        gerd_value = ((final_value // zarib_gerd) + 1)*zarib_gerd
        return gerd_value / 1000