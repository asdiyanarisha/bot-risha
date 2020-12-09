import oauth2
import json
from urllib.parse import urlencode

host = "https://api.twitter.com/2/"


class Twitter2:
    def __init__(self, consumer_key, consumer_secret, access_token, secret_token):
        consumer = oauth2.Consumer(key=consumer_key, secret=consumer_secret)
        token = oauth2.Token(key=access_token, secret=secret_token)
        self.client = oauth2.Client(consumer, token)

    def search(self, keyword, count=20, cursor=''):

        # request params
        params = {
            "q": keyword,
            "include_reply_count": 1,
            "tweet_mode": "extended",
            "include_user_entities": "true",
            "tweet_search_mode": 'live',
            "count": count
        }

        url = host + 'search/adaptive.json?{}'.format(urlencode(params))

        # checking cursor empty or not
        if cursor != '':
            url = url + "&cursor={}".format(cursor)

        resp, content = self.client.request(url)

        return json.loads(content.decode('utf8'))

    def detail(self, tweet_id):
        params = {
            "include_reply_count": 1
        }
        url = host + "timeline/conversation/{}.json?{}".format(tweet_id, urlencode(params))
        resp, content = self.client.request(url)

        return json.loads(content.decode('utf8'))
