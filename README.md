# replenishment_steam_wallet
this code analyzes the offers on the cs go market and gives out the most profitable ones


# settings in config.py

__price Min - minimum price (rubles)

_priceMax = maximum price (rubles)

num_analysis - the number of offers to analyze (affects the time)

steam_comission - steam commission 

plati_market_commission - commission for replenishment of market csgo

time_market_csgo - waiting time after loading market csgo

time_base_sleep_steam - waiting time after loading the steam trading platform

time_one_error_sleep_steam - waiting time after the first error when loading the steam trading platform

time_two_error_sleep_steam - waiting time after the second error when loading the steam trading platform

time_three_error_sleep_steam - waiting time after the third error when loading the steam trading platform

path_data is the path to the file to save information about all offers.

path_smoll_data - the path to the file for saving information about profitable offers

# information about offers

url_market - link to the product in market csgo

name - product name

price_market - price on market csgo

url_steam - link to the product on the steam trading platform

price_steam - steam price (rubles)

sale_price - the amount that will be credited to the steam wallet (rubles)

growth - profit (rubles)

percentage - profit as a percentage
