
import requests
import numpy as np


from khayyam import  JalaliDatetime
from Stock import Stock
from CallOption import CallOption
from PutOption import PutOption


class DataProvider:
    def __init__(self):
        self.headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'}
        self.main_market_info_link = 'https://cdn.tsetmc.com/api/ClosingPrice/GetMarketWatch?market=0&industrialGroup=&paperTypes[0]=1'
        self.etf_market_info_link = 'https://cdn.tsetmc.com/api/ClosingPrice/GetMarketWatch?market=0&industrialGroup=&paperTypes[0]=8'
        self.payeh_market_info_link = 'https://cdn.tsetmc.com/api/ClosingPrice/GetMarketWatch?market=0&industrialGroup=&paperTypes[0]=2'
        self.options_market_info_link = 'https://cdn.tsetmc.com/api/ClosingPrice/GetMarketWatch?market=0&industrialGroup=&paperTypes[0]=6'

        self.etf_spread = 0.235
        self.stock_spread = 1.25

    def get_info(self, market_info):
        self.__get_etf_info(market_info)
        self.__get_main_market_info(market_info)
        self.__get_payeh_market_info(market_info)
        self.__get_options_info(market_info)
        market_info.find_relations()
        print("===============================")
        print("data was downloaded successfuly")
        print("===============================")

    def __get_etf_info(self, market_info):
        the_file = self.__get_raw_file(self.etf_market_info_link)
        self.__get_info_from_raw_file_stock(the_file, market_info, self.etf_spread)

    def __get_main_market_info(self, market_info):
        the_file = self.__get_raw_file(self.main_market_info_link)
        self.__get_info_from_raw_file_stock(the_file, market_info, self.stock_spread)

    def __get_payeh_market_info(self, market_info):
        the_file = self.__get_raw_file(self.payeh_market_info_link)
        self.__get_info_from_raw_file_stock(the_file, market_info, self.stock_spread)
    
    def __get_options_info(self, market_info):
        the_file = self.__get_raw_file(self.options_market_info_link)
        self.__get_info_from_raw_file_option(the_file, market_info)

    def __get_raw_file(self, link):
        raw_file_1 = requests.get(url= link, headers=self.headers)
        file_1 = np.array(raw_file_1.text.split('},{'))
        return file_1
    


    def __get_info_from_raw_file_stock(self, file, market_info, spread):
        for i in range(len(file)):
            sh_ticker =  str(file[i].split('"lva":"')[1].split('\",\"')[0])
            sh_full_name = str(file[i].split('"lvc":"')[1].split('\",\"')[0])

            sh_sarkhat_kharid = int(file[i].split('"pmd":')[1].split(',')[0][:-2])
            sh_sarkhat_foroosh = int(file[i].split('"pmo":')[1].split(',')[0][:-2])
            sh_last_price = int(file[i].split('"pdv":')[1].split(',')[0][:-2])
            sh_close_price = int(file[i].split('"pcl":')[1].split(',')[0][:-2])
            sh_min_price = int(file[i].split('"pmn":')[1].split(',')[0][:-2])
            sh_max_price = int(file[i].split('"pmx":')[1].split(',')[0][:-2])
            sh_hajm = int(file[i].split('"qtj":')[1].split(',')[0][:-2])

            market_info.add_stock(Stock(sh_ticker, sh_full_name, sh_close_price, sh_max_price, sh_min_price, sh_last_price, sh_hajm, sh_sarkhat_kharid, sh_sarkhat_foroosh, spread))



    def __get_option_type(self, name):
        if(name[0] == 'ض'):
            return  'call'
        elif(name[0] == 'ط'):
            return 'put'
        return None


    def __get_date_from_formatted_text(self, the_date):
        now = JalaliDatetime.today()
        splited_date = the_date.replace("/","")
        if(len(splited_date) == 8):
            then = JalaliDatetime(splited_date[0:4],splited_date[4:6],splited_date[6:8], 0, 0, 0, 0)
        else:
            then = then = JalaliDatetime(splited_date[0:2],splited_date[2:4],splited_date[4:6], 0, 0, 0, 0)
        op_days_till_mature = (then - now).days

        return op_days_till_mature, then

    def __decode_option_info_from_full_name(self, op_type, op_details_str, market_info):
        
        if(op_type == "call"):
            op_underlying_asset_name = str(op_details_str.split('خ ')[1].split('-')[0])
        if(op_type == "put"):
            op_underlying_asset_name = str(op_details_str.split('ف ')[1].split('-')[0])

        op_strike_price = int(op_details_str.split('-')[1].split('-')[0])
        op_strike_date = str(op_details_str.split('-')[2].split("\"")[0])
        
        op_days_till_mature, then = self.__get_date_from_formatted_text(op_strike_date)

        underlying_asset = market_info.find_stock_with_name(op_underlying_asset_name)

        return underlying_asset, op_days_till_mature, op_strike_price, then


    def __get_option_pricing_info(self, section):
        op_sarkhat_kharid = int(section.split('"pmd":')[1].split(',')[0][:-2])
        op_sarkhat_foroosh = int(section.split('"pmo":')[1].split(',')[0][:-2])
        op_last_price = int(section.split('"pdv":')[1].split(',')[0][:-2])
        op_hajm = int(section.split('"qtj":')[1].split(',')[0][:-2])

        return op_sarkhat_kharid, op_sarkhat_foroosh, op_last_price, op_hajm
    
    def __get_info_from_raw_file_option(self, file, market_info):
        
        for i in range(len(file)):
            op_name =  str(file[i].split('"lva":"')[1].split('\",\"')[0])
            op_type = self.__get_option_type(op_name)
            if(op_type == None):
                continue
            
            op_details_str = str(file[i].split('"lvc":')[1].split(',')[0])
            underlying_asset, op_days_till_mature, op_strike_price, then = self.__decode_option_info_from_full_name(op_type, op_details_str, market_info)
            op_sarkhat_kharid, op_sarkhat_foroosh, op_last_price, op_hajm = self.__get_option_pricing_info(file[i])

            if(underlying_asset == None):
                print("couldn't find underlying asset with name", op_name)
                continue

            if(op_type == 'call'):
                market_info.add_call_option(CallOption(op_name, op_strike_price, underlying_asset, then, op_days_till_mature, op_sarkhat_kharid, op_sarkhat_foroosh, op_hajm, op_last_price))
            elif(op_type == 'put'):
                market_info.add_put_option(PutOption(op_name, op_strike_price, underlying_asset, then, op_days_till_mature, op_sarkhat_kharid, op_sarkhat_foroosh, op_hajm, op_last_price))
