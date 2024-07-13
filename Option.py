class Option:
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
        self.vajh_tazmin = 0

    def get_cost_to_buy(self, sarkhat_or_latest = 'sarkhat'):
        buy_price =  self.best_foroosh if sarkhat_or_latest == 'sarkhat' else self.last_price
        return buy_price

    def get_cost_to_sell(self, needs_vajh_tazmin,  sarkhat_or_latest = 'sarkhat'):
        sell_price =  self.best_kharid if sarkhat_or_latest == 'sarkhat' else self.last_price
        if(not needs_vajh_tazmin):
            return sell_price
        else:
            return (-1) * self.vajh_tazmin
    
    def get_value_at_price(self, final_price, had_vajh_tazmin= False, sarkhat_or_latest= 'sarkhat'):
        pass

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