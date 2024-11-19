import asyncio
import json
import requests
from telethon.tl.functions.messages import RequestAppWebViewRequest
from telethon.tl.types import InputBotAppShortName
import config
from function import get_info_from_url, create_user_data, create_init_data, send_request


async def get_info_in_webapp(signal_id, client):
    return_dict = {}

    app_info = await client(
        RequestAppWebViewRequest(
            peer="me",
            app=InputBotAppShortName(await client.get_input_entity("makscontrol_bot"), "Signal"),
            platform="android",
            start_param=signal_id,
        )
    )
    url = app_info.url
    info_url = get_info_from_url(url)

    # info user
    info_for_me = await client.get_me()
    user_data = create_user_data(info_for_me, info_url['photo_url'])

    init_data = create_init_data(user_data,
                                 chat_instance=info_url['chat_instance'],
                                 signal_id=signal_id,
                                 auth_date=info_url['auth_date'],
                                 signature=info_url['signature'],
                                 hash=info_url['hash'],
                                 photo_url=info_url['photo_url']
                                 )

    r = requests.post("https://makscontrol.com/bot/webapp/api/open-signal.php",
                      data={"user": str(user_data).replace(" ", '').replace("'", '"').replace("True", 'true'),
                            'signal_id': signal_id,
                            "init_data": init_data})


    get_r = await send_request(r, url, user_data, init_data, signal_id)
    get_r['for_output']['Full_url'] = url
    return get_r
