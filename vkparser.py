import requests
import json

from db import create_news_items


def get_feed():
    res = requests.get('https://api.vk.com/method/wall.get?owner_id=-36180072&count=100&v=5.52&access_token=976f55e3faaac76907812e9747747850cf79ef6a2ee0ca76622a839fe0cc9df20400cb355a592ad18ad32')
    res = json.loads(res.content.decode('utf-8')).get('response')
    return create_news_items(res['items'])
