import json
import urllib.parse
from urllib.parse import quote
import re
import requests
import config
import asyncio


def normalization_photo_url(url):
    unq = urllib.parse.unquote(url)
    final_result = unq.replace("%5C%2F", '\\').replace("%3A", ":")
    norm = final_result.replace("\\", r"\/")
    return norm

def edit_user_data_for_photo_url(user_data, url):
    index_photo_url = user_data.index("photo_url")
    start_word = r"photo_url"
    end_word = r".svg"

    result = re.sub(f"{start_word}.*?{end_word}", "", user_data)
    new_user_data = result[:index_photo_url] + "photo_url%22%3A%22" + url + result[index_photo_url:]
    return new_user_data

def formatted_norm_photo_url(normalization_url):
    url = normalization_url.replace(":", "%3A")
    url = url.replace("\\", "%5C").replace("/", "%2F")
    return url

def get_info_from_url(url):
    chat_instance = url.split("chat_instance%3D")[1].split("%26")[0].split("&")[0]
    auth_date = url.split("auth_date%3D")[1].split("%26")[0].split("&")[0]
    hash = url.split("hash%3D")[1].split("%26")[0].split("&")[0]
    signature = url.split("signature%3D")[1].split("%26")[0]
    url_photo = "https" + url.split("photo_url")[1].split("https")[1].split('.svg')[0] + '.svg'
    return {
        'chat_instance': chat_instance,
        'auth_date': auth_date,
        'hash': hash,
        'signature': signature,
        'photo_url': url_photo

    }

def create_user_data(info_for_me, url_photo):
    return {
        "id": info_for_me.id,
        "first_name": info_for_me.first_name,
        "last_name": info_for_me.last_name,
        "language_code": "ru",
        "allows_write_to_pm": True,
        "photo_url": normalization_photo_url(url_photo)
    }

def create_init_data(user_data, chat_instance, signal_id, auth_date, signature, hash, photo_url):
    norm_photo_url = normalization_photo_url(photo_url)
    utf8_text = str(user_data).encode("utf-8")
    percent_encoded_text = quote(utf8_text).replace("%20", "").replace("%27", "%22").replace("True", "true").replace("False", "false")
    user_data_for_init = edit_user_data_for_photo_url(percent_encoded_text, formatted_norm_photo_url(norm_photo_url))

    init_data = {"user": user_data_for_init,
                 "chat_instance": chat_instance,
                 "chat_type": "private",
                 "start_param": signal_id,
                 "auth_date": auth_date,
                 "signature": signature,
                 "hash": hash}

    str_init_data = ""
    num = 0
    for x in init_data:
        num += 1

        str_init_data += f"{x}={init_data[x]}"
        if num != len(init_data):
            str_init_data += "&"

    return str_init_data

async def send_request(request, url, user_data, init_data, signal_id):
    for_output = {}

    captcha_solution = True
    finish_r = None
    if len(dict(json.loads(request.text))) == 2:
        for_output["Captcha"] = '+'
        # Captcha
        site_key = "6LcvH8opAAAAAO1y4uN38bT9mc6MiHuYQe5m742k"
        url_requests = f"http://rucaptcha.com/in.php?key={config.captcha_token}&method=userrecaptcha&googlekey={site_key}&pageurl={url}"
        x = 0
        captcha_solution = False
        while x != config.count_captcha_check:
            x += 1
            id_captcha = requests.get(url_requests).text
            if "OK|" in id_captcha:
                id_captcha = id_captcha.split("|")[1]
                s = 0
                while True:
                    s += 1
                    captcha_token = requests.post(
                        f"http://rucaptcha.com/res.php?key={config.captcha_token}&action=get&id={id_captcha}").text
                    if captcha_token != "CAPCHA_NOT_READY":
                        captcha_token = captcha_token.replace("OK|", "")
                        break

                    await asyncio.sleep(1)
                # get info
                r = requests.post("https://makscontrol.com/bot/webapp/api/open-signal-unlock.php",
                                  # api/open-signal.php
                                  data={
                                      "user": str(user_data).replace(" ", '').replace("'", '"').replace("True", 'true'),
                                      'signal_id': signal_id,
                                      "captcha_token": captcha_token,
                                      "init_data": init_data})
                check = dict(json.loads(r.text))
                if check["status"] == "error" and check["code"] == "3":
                    continue
                else:
                    captcha_solution = True
                    finish_r = r
                    break

    else:
        for_output["Captcha"] = '-'
        finish_r = request

    if captcha_solution:
        info_signal = dict(json.loads(finish_r.text))
        try:
            img_url = "https://makscontrol.com/bot/webapp/imgs/signals/" + info_signal["signal_data"]["img_link"]
            text = info_signal["signal_data"]["text"]
            for_output["Status_send"] = 'True'
            return {"img_url": img_url, "text": text.replace("<BR>", "\n"), 'for_output': for_output}
        except:
            print(f"Ошибка: \nДанные: info_signal = {info_signal}")

    else:
        for_output["Status_send"] = 'False'