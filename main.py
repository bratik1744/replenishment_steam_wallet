from selenium import webdriver
import bs4
import re

import time

import pandas as pd
from tqdm import tqdm

from config import *

import datetime


########################################################################################################################


print(datetime.datetime.now(), "Запуск Chrome")
driver = webdriver.Chrome()

print(datetime.datetime.now(), "получения кода market.csgo")
driver.get(url_market_csgo)
time.sleep(time_market_csgo)
html_code_market_csgo = driver.page_source
soup_market_csgo = bs4.BeautifulSoup(html_code_market_csgo, "html.parser")

print(datetime.datetime.now(), "обработка данных market.csgo")
data = pd.DataFrame(columns=["url_market", "name", "price_market", "url_steam"])
for i in tqdm(soup_market_csgo.find_all("a", attrs={"class": "ng-star-inserted"})[15:(15+num_analysis)]):
    try:
        l1 = "https://market.csgo.com" + i["href"]
        l2 = (i.find_all_next("div", attrs={"class": re.compile("quality.+")})[0].text)
        l3 = float((i.find_all_next("div")[0].div.find_all_next("div")[1].find_all_next("div")[1].find_all_next("div")[
                        1].find_all_next("span")[0].text)[:-2].replace(",", ".")) * plati_market_comission
        l4 = r"https://steamcommunity.com/market/listings/730/" + i["href"].split("/")[-1]
        data.loc[len(data.index)] = [l1, l2, l3, l4]

    except BaseException as e:
        print(datetime.datetime.now(), "\nчто-то пошло не так...\t", e)


########################################################################################################################

print(datetime.datetime.now(), "сбор цен с торговой площадки steam")
lst_price = []
for i in tqdm(data.values):
    try:
        driver.get(i[-1])
        time.sleep(time_base_sleep_steam)
        soup = bs4.BeautifulSoup(driver.page_source, "html.parser")
        if len(soup.find_all("span", attrs={"class": "market_commodity_orders_header_promote"})) >= 2:
            lst_price.append(float(soup.find_all("span", attrs={"class": "market_commodity_orders_header_promote"})[1].text[1:]))
        else:
            lst_price.append(float(soup.find_all("span", attrs={"class": "market_commodity_orders_header_promote"})[3].text[1:]))
    except BaseException:
        try:
            print(datetime.datetime.now(), f"\nпервая ошибка, ожидание {time_one_error_sleep_steam} секунд")
            time.sleep(time_one_error_sleep_steam)
            driver.get(i[-1])
            time.sleep(time_base_sleep_steam)
            soup = bs4.BeautifulSoup(driver.page_source, "html.parser")
            if len(soup.find_all("span", attrs={"class": "market_commodity_orders_header_promote"})) >= 2:
                lst_price.append(float(soup.find_all("span", attrs={"class": "market_commodity_orders_header_promote"})[1].text[1:]))
            else:
                lst_price.append(float(soup.find_all("span", attrs={"class": "market_commodity_orders_header_promote"})[3].text[1:]))
        except BaseException:
            try:
                print(datetime.datetime.now(), f"\nвторя ошибка, ожидание {time_two_error_sleep_steam} секунд")
                time.sleep(time_two_error_sleep_steam)
                driver.get(i[-1])
                time.sleep(time_base_sleep_steam)
                soup = bs4.BeautifulSoup(driver.page_source, "html.parser")
                if len(soup.find_all("span", attrs={"class": "market_commodity_orders_header_promote"})) >= 2:
                    lst_price.append(float(soup.find_all("span", attrs={"class": "market_commodity_orders_header_promote"})[1].text[1:]))
                else:
                    lst_price.append(float(soup.find_all("span", attrs={"class": "market_commodity_orders_header_promote"})[3].text[1:]))
            except BaseException:
                try:
                    print(datetime.datetime.now(), f"\nтретья ошибка, ожидание {time_three_error_sleep_steam} секунд")
                    time.sleep(time_three_error_sleep_steam)
                    driver.get(i[-1])
                    time.sleep(time_base_sleep_steam)
                    soup = bs4.BeautifulSoup(driver.page_source, "html.parser")
                    if len(soup.find_all("span", attrs={"class": "market_commodity_orders_header_promote"})) >= 2:
                        lst_price.append(float(soup.find_all("span", attrs={"class": "market_commodity_orders_header_promote"})[1].text[1:]))
                    else:
                        lst_price.append(float(soup.find_all("span", attrs={"class": "market_commodity_orders_header_promote"})[3].text[1:]))
                except BaseException:
                    lst_price.append(-1)

data["price_steam"] = lst_price

print(datetime.datetime.now(), f"потерянно {len(data[data.price_steam == -1])} предложений")

data = data[data.price_steam != -1]

########################################################################################################################



print(datetime.datetime.now(), "обработка данных")

data["price_steam"] = data["price_steam"] * usd
data["price_market"] = data["price_market"] * usd

data["sale_price"] = data["price_steam"] * steam_comission
data["growth"] = data["sale_price"] - data["price_market"]

data["percent"] = data["growth"] / data["price_market"]

data.sort_values("percent", ascending=False, ignore_index=True, inplace=True)

########################################################################################################################


print(datetime.datetime.now(), "Сохранение Данных")

data.to_csv("data.csv", index=False)
data[data.percent > 0].to_csv("smoll_data.csv", index=False, columns=["price_market", "growth", "sale_price", "percent", "url_market"])