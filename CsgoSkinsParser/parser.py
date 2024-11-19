import asyncio
import json
import time
import urllib.parse
import aiohttp
import requests
from colorama import Fore
from colorama import init
from fake_useragent import UserAgent
import config

init(autoreset=True)

ua = UserAgent()

# config_parser
HEADERS = {
        'User-Agent': ua.random,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'en;q=0.9,en-GB;q=0.8,en-US;q=0.7',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'cross-site',
    }

async def steam(proxy, log=True):
    data = []
    count = 0
    count_read = 100
    number_proxy = 0
    while True:
        HEADERS['User-Agent'] == ua.random
        proxies = {'https': proxy[number_proxy]}
        try:
            json = requests.get(f"https://steamcommunity.com/market/search/render/?query=&start={count}&count={count_read}&search_descriptions=0&sort_column=popular&sort_dir=desc&appid=730&norender=1", headers=HEADERS, proxies=proxies).json()

            if json is None:
                if number_proxy == len(proxy) - 1:
                    number_proxy = 0
                else:
                    number_proxy += 1
                continue
        except (requests.exceptions.ProxyError, requests.exceptions.JSONDecodeError, requests.exceptions.SSLError, requests.exceptions.ConnectionError, requests.exceptions.ChunkedEncodingError):
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
                json["results"] = [x for x in json["results"] if config.max_price >= x['sell_price'] / 100 >= config.min_price]
                json["results"] = [{'name': x['name'],
                                    'sell_price': x['sell_price'] / 100,
                                    'image_url': "https://community.akamai.steamstatic.com/economy/image/" + x['asset_description']['icon_url'],
                                    'url_pay': "https://steamcommunity.com/market/search?q=" + urllib.parse.quote(x['name'])}
                                   for x in json["results"]]
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

async def cs_money(log=True):
    data = []
    count = 1
    requests.post("https://cs.money/user-meta/save", data={'currency': "USD"})
    async with aiohttp.ClientSession() as session:
        while True:
            try:
                async with session.get("https://cs.money/1.0/market/sell-orders", params={"limit": 60, "offset": count * 60} if count > 1 else {"limit": 60}) as response:
                    json = await response.json()
                    if not json or 'items' not in json:
                        if log:
                            print('\r', end='', flush=True)
                            print(Fore.GREEN + f"[info] cs.money успешно спаршен!", end='', flush=True)
                            print()
                        break

                    if log:
                        print('\r', end='', flush=True)
                        print(Fore.BLUE + f"[info] Парсинг cs.money [{count * 60}/...]", end='', flush=True)
                    json['items'] = [{'name': x['asset']['names']['full'],
                                      'sell_price': x['pricing']['computed'],
                                      'image_url': x['asset']['images']['steam'],
                                      'url_pay': "https://cs.money/market/buy"}
                                     for x in json['items'] if config.max_price >= x['pricing']['computed'] >= config.min_price]
                    data.extend(json['items'])
            except:
                pass
            count += 1

    return data


async def market_csgo(log=True):
    r = requests.get(f"https://market.csgo.com/api/v2/prices/USD.json", headers=HEADERS).json()
    print(r)
    data = [x for x in r['items'] if config.max_price >= float(x['price']) >= config.min_price]
    for x in range(len(data)): del data[x]['volume']
    data = [
        {'name': x['market_hash_name'],
         'sell_price': x['price'],
         'image_url': f'https://cdn2.csgo.com/item/image/width=458/{urllib.parse.quote(x["market_hash_name"])}.webp',
         'url_pay': "https://market.csgo.com/ru/?search=" + urllib.parse.quote(x['market_hash_name'])}
        for x in data]
    if log:
        print('\r', end='', flush=True)
        print(Fore.GREEN + f"[info] market.csgo.com успешно спаршен!", end='', flush=True)
        print()
    return data

async def main_parser(proxy=config.proxy, log=True):
    answer = {}
    try:
        answer['https://market.csgo.com/'] = await market_csgo(log)
        if proxy:
            answer['https://steamcommunity.com/market'] = await steam(proxy, log)
        answer['https://cs.money/market/buy'] = await cs_money(log)

        if log:
            print('\r', end='', flush=True)
            print(Fore.GREEN + f"[info] Все сайты были успешно спаршены!", end='', flush=True)
            print()

        return answer
    except Exception as error:
        print('\r', end='', flush=True)
        print(Fore.RED + f"[info] При парсинге сайтов произошла ошибка", end='', flush=True)
        print(error)
        exit(0)