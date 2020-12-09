import requests
import os

headers = {
    'accept': 'application/json',
    'Content-Type': 'application/x-www-form-urlencoded'
}


def predict(name):
    try:
        if len(name) <= 3:
            return "unknown"
        url = os.environ.get("SOCIAL_SEX_CLASSIFICATION_URL")
        r = requests.post(url, data={'name': name}, headers=headers)
        data = r.json()
        return data['data']['sex']
    except:
        return "unknown"
