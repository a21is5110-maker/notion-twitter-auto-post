"""Twitter / X API v2 を使ってツイートを投稿するヘルパー。"""

import tweepy
import config

_client = tweepy.Client(
    consumer_key=config.TWITTER_API_KEY,
    consumer_secret=config.TWITTER_API_SECRET,
    access_token=config.TWITTER_ACCESS_TOKEN,
    access_token_secret=config.TWITTER_ACCESS_TOKEN_SECRET,
)


def post_tweet(text: str) -> str:
    """ツイートを投稿し、Tweet ID を返す。"""
    response = _client.create_tweet(text=text)
    return str(response.data["id"])
