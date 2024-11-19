from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from fake_useragent import UserAgent
import random
import time
import os
import requests
import json
import config

ua = UserAgent()

# Chrome options
chrome_options = ChromeOptions()
chrome_options.add_argument("--disable-infobars")

# WebDriver service
service = ChromeService('chromedriver.exe')
chrome_options.add_argument("user-agent=" + ua.random)
chrome_options.page_load_strategy = 'none'

def has_child_divs(driver):
    try:
        parent_div = driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div/main/div/div/div[2]/div/div[2]/div')
        child_divs = parent_div.find_elements(By.TAG_NAME, 'div')
        return len(child_divs) > 2
    except:
        return True

def get_followers_channel(channel, count=1000, max_followers=10000):
    answer = []
    count_parser = 0
    cursor_set = None
    data = {
        'channelKey': channel,
        'limit': count
    }

    while True:
        if cursor_set is None:
            r = requests.get(f"https://client.warpcast.com/v2/channel-followers?channelKey={data['channelKey']}&limit={data['limit']}").json()
        else:
            r = requests.get(f"https://client.warpcast.com/v2/channel-followers?cursor={cursor_set}&channelKey={data['channelKey']}&limit={data['limit']}").json()
            if 'next' not in r.keys():
                count_parser += len(r["result"]["users"])
                for x in r["result"]["users"]:
                    if x["followerCount"] <= max_followers:
                        answer.append(x["username"])
                break

        cursor_set = r['next']['cursor']
        for x in r["result"]["users"]:
            if x["followerCount"] <= max_followers:
                if "username" in x.keys():
                    answer.append(x["username"])
        count_parser += len(r["result"]["users"])
    print(answer)
    if config.start_with != '':
        try:
            answer = answer[answer.index(config.start_with.lower()) + 1:]
        except:
            print("Произошла ошибка при нахождении пользователя, с которого нужно начать рассылку!")
    return answer


def main(driver):
    # Authorization
    driver.get("https://warpcast.com/")
    try:
        WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, '// *[ @ id = "root"] / div / div / div[2] / div[1] / div / div[2] / div[2] / div[2] / button[2]'))).click()
    except:
        print("Страница не может загрузиться :(")
        exit(0)
    # await authorization
    while True:
        try:
            driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div/main/div/div/nav/div[1]/h2')
            break
        except:
            continue

    print("Начинается парсинг подписчиков для рассылки...")
    users = ['pplpleasr', "x0x0x0x0", "username69"]# get_followers_channel(config.channel)
    print(f"Подписчика канала {config.channel} успешно были спаршенны для рассылки. ({len(users)} шт.)")

    c = 0
    for user in users:
        print(f"Идет рассылка... [{c}/{len(users)}]", end='', flush=True)
        print("\r", end='', flush=True)
        driver.get("https://warpcast.com/" + user)
        try:
            WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '// *[ @ id = "root"] / div / div / div / main / div / div / div[1] / div / div / div[1] / div[2] / button[1]'))).click()
            input = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/div/div/main/div/div/div[2]/div/div[3]/div/div[2]/div/div/div/div')))
            if not has_child_divs(driver):
                for part in config.spam_text.split('\n'):
                    input.send_keys(part)
                    ActionChains(driver).key_down(Keys.SHIFT).key_down(Keys.ENTER).key_up(Keys.SHIFT).key_up(Keys.ENTER).perform()
                WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="root"]/div/div/div/main/div/div/div[2]/div/div[3]/div/button[2]'))).click()
                c += 1
        except:
            continue
    print(f"Рассылка для подписчиков {config.channel} успешно завершенна")
    driver.quit()

driver = webdriver.Chrome(options=chrome_options)
main(driver)
print(f"Пожалуйста авторизуйтесь!")