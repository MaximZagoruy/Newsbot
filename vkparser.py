import requests
import json
import settings

from db import create_news_items


def get_feed():
    res = requests.get(f'https://api.vk.com/method/wall.get?owner_id=-36180072&count=100&v=5.52&access_token={settings.token_api}')
    res = json.loads(res.content.decode('utf-8')).get('response')
    return create_news_items(res['items'])
