import requests
import os
from lib.util import log

logger = log.get_logger("sentiment.core")

headers = {
    'accept': 'application/json',
    'Content-Type': 'application/x-www-form-urlencoded'
}


def predict(text):
    try:
        url = os.environ.get("SENTIMENT_URL")
        r = requests.post(url, data={'sentence': text}, headers=headers)
        data = r.json()
        return data['data']['sentiment']
    except Exception as e:
        logger.error(e)
        return "neutral"
