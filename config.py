import os
from dotenv import load_dotenv

load_dotenv()


def _require(key: str) -> str:
    value = os.getenv(key)
    if not value:
        raise EnvironmentError(f"環境変数 {key} が設定されていません。.env を確認してください。")
    return value


NOTION_TOKEN = _require("NOTION_TOKEN")
NOTION_DATABASE_ID = _require("NOTION_DATABASE_ID")

TWITTER_API_KEY = _require("TWITTER_API_KEY")
TWITTER_API_SECRET = _require("TWITTER_API_SECRET")
TWITTER_ACCESS_TOKEN = _require("TWITTER_ACCESS_TOKEN")
TWITTER_ACCESS_TOKEN_SECRET = _require("TWITTER_ACCESS_TOKEN_SECRET")

POLL_INTERVAL_SECONDS = int(os.getenv("POLL_INTERVAL_SECONDS", "300"))
