



class CallOption:
    def __init__(self, _ticker, _strike, _u_asset, _maturity_date, _days_till_maturity, _best_kharid, _best_foroosh, _volume, _last_price):
        self.ticker = _ticker
        self.strike = _strike
        self.u_asset = _u_asset
        self.maturity_date = _maturity_date
        self.days_till_maturity = _days_till_maturity
        self.best_kharid = _best_kharid
        self.best_foroosh = _best_foroosh
        self.volume = _volume
        self.last_price = _last_price
        self.option_size = 1000
        self.vajh_tazmin = self.__cal_vajh_tazmin(self.u_asset.get_close_price() , self.strike, self.option_size)
    
    def get_value_at_strike(self, final_price):
        return max(final_price - self.strike, 0)
    
    def get_cost_to_buy(self, needs_vajh_tazmin, sarkhat_or_latest = 'sarkhat'):
        return self.best_foroosh if sarkhat_or_latest == 'sarkhat' else self.last_price

    def get_cost_to_sell(self, needs_vajh_tazmin, sarkhat_or_latest = 'sarkhat'):
        return self.best_kharid if sarkhat_or_latest == 'sarkhat' else self.last_price
    
    def check_name(self, chosen_ticker):
        if(chosen_ticker == self.ticker):
            return True
        return False

    def get_strike_price(self):
        return self.strike

    def get_underlying_asset(self):
        return self.u_asset

    def get_days_till_maturity(self):
        return self.days_till_maturity
    
    def __repr__(self) -> str:
        return self.ticker
    

    def __cal_vajh_tazmin (self, ua_close, strike_price, op_size):
        zarib_gerd = 10000  
        op_loss = max(strike_price - ua_close, 0 ) * op_size
        firs_method = 0.2 * ua_close * op_size - op_loss
        second_method = 0.1 * strike_price * op_size
        final_value = max(firs_method, second_method)
        gerd_value = ((final_value // zarib_gerd) + 1)*zarib_gerd
        return gerd_value