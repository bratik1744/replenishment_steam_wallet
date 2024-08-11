import requests


_priceMin = 0
_priceMax = 1000
num_analysis = 40

steam_comission = 0.87
plati_market_comission = 1.075

time_market_csgo = 30
time_base_sleep_steam = 1.5
time_one_error_sleep_steam = 7
time_two_error_sleep_steam = 60
time_three_error_sleep_steam = 90

usd = requests.get('https://www.cbr-xml-daily.ru/daily_json.js').json()['Valute']['USD']["Value"]
url_market_csgo = f"https://market.csgo.com/ru/?priceMin={_priceMin}&priceMax={int(_priceMax / usd)}&other=csp"
url_steam = "https://steamcommunity.com/market/search?q="

path_data = "data.csv"
path_smoll_data = "smoll_data.csv"

