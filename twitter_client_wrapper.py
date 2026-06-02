import os
import tweepy


class TwitterWrapper:
    """Twitter API v2 を使ってツイートを投稿する。"""

    def __init__(self):
        self.client = tweepy.Client(
            consumer_key=os.environ["TWITTER_API_KEY"],
            consumer_secret=os.environ["TWITTER_API_SECRET"],
            access_token=os.environ["TWITTER_ACCESS_TOKEN"],
            access_token_secret=os.environ["TWITTER_ACCESS_TOKEN_SECRET"],
        )
        self.max_length = int(os.environ.get("MAX_TWEET_LENGTH", "140"))

    def post(self, text: str) -> str:
        """ツイートを投稿し、ツイートIDを返す。"""
        if len(text) > self.max_length:
            text = text[: self.max_length - 1] + "…"

        response = self.client.create_tweet(text=text)
        return str(response.data["id"])
