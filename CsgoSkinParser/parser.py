import time
import requests
import os
import random
import json
from time import sleep
from fake_useragent import UserAgent
import sys
from termcolor import colored, cprint
from colorama import init
from colorama import Fore, Back, Style

init(autoreset=True)

ua = UserAgent()

# config_parser
HEADERS = {
        'User-Agent': None,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'cross-site',
    }

def steam(proxy, log=True):
    data = []
    count = 0
    count_read = 100
    number_proxy = 0
    while True:
        HEADERS['User-Agent'] == ua.random
        proxies = {'https': proxy[number_proxy]}
        try:
            json = requests.get(f"https://steamcommunity.com/market/search/render/?query=&start={count}&count={count_read}&search_descriptions=0&sort_column=popular&sort_dir=desc&appid=730&norender=1", headers=HEADERS, proxies=proxies).json()
        except (requests.exceptions.ProxyError, requests.exceptions.JSONDecodeError, requests.exceptions.SSLError, requests.exceptions.ConnectionError, requests.exceptions.ChunkedEncodingError):
            if number_proxy == len(proxy) - 1:
                number_proxy = 0
            else:
                number_proxy += 1
            continue

        if json is None:
            if number_proxy == len(proxy) - 1:
                number_proxy = 0
            else:
                number_proxy += 1
            continue

        if json["success"]:
            if json["results"]:
                if log:
                    print('\r', end='', flush=True)
                    print(Fore.BLUE + f"[info] Парсинг маркета стима [{count}/{json['total_count']}]", end='', flush=True)
                data.extend(json["results"])
                count += count_read
            else:
                if log:
                    print('\r', end='', flush=True)
                    print(Fore.GREEN + f"[info] Маркет стима успешно спаршен!", end='', flush=True)
                    print()
                return data
        else:
            print(Fore.RED + "[Error] Ошибка при парсинге маркета стима")


def cs_money(log=True):
    data = []
    count = 1

    while True:
        HEADERS['User-Agent'] == ua.random
        json = requests.get("https://cs.money/1.0/market/sell-orders", params={"limit": 60, "offset": count * 60} if count > 1 else {"limit": 60}, headers=HEADERS).json()
        if log:
            print('\r', end='', flush=True)
            print(Fore.BLUE + f"[info] Парсинг cs.money [{count * 60}/...]", end='', flush=True)
        if not json:
            if log:
                print('\r', end='', flush=True)
                print(Fore.GREEN + f"[info] cs.money успешно спаршен!", end='', flush=True)
                print()
            break

        json['items'] = [item for item in json['items'] if float(item["pricing"]["default"]) >= 50]

        data.extend(json['items'])

        count += 1

    return data


def market_csgo(log=True):
    HEADERS['User-Agent'] == ua.random
    r = requests.get(f"https://market.csgo.com/api/v2/prices/RUB.json", headers=HEADERS).json()
    data = [x for x in r['items'] if float(x['price']) >= 50]
    if log:
        print('\r', end='', flush=True)
        print(Fore.GREEN + f"[info] market.csgo.com успешно спаршен!", end='', flush=True)
        print()
    return data

def main(proxy, log=True):
    try:
        market_csgo(log)
        steam(proxy, log)
        cs_money(log)

        if log:
            print('\r', end='', flush=True)
            print(Fore.GREEN + f"[info] Все сайты были успешно спаршены!", end='', flush=True)
            print()
    except Exception as error:
        print('\r', end='', flush=True)
        print(Fore.RED + f"[info] При парсинге сайтов произошла ошибка", flush=True)
        print(error)
        exit(0)