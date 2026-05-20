#!/usr/bin/env python3
"""
Notion → X (Twitter) 自動投稿スクリプト

Notionデータベースから未投稿の記事を取得し、Xに投稿します。
投稿済みのアイテムには "Posted" ステータスを付与します。

Notionデータベースに必要なプロパティ:
  - Tweet (title または rich_text): 投稿するテキスト
  - Status (select): "Ready to Post" → 投稿後 "Posted" に変更
  - Posted At (date): 投稿日時を自動記録 (任意)
"""

import os
import sys
import logging
from datetime import datetime, timezone

import tweepy
from notion_client import Client as NotionClient

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
log = logging.getLogger(__name__)

NOTION_TOKEN = os.environ["NOTION_TOKEN"]
NOTION_DATABASE_ID = os.environ["NOTION_DATABASE_ID"]

X_API_KEY = os.environ["X_API_KEY"]
X_API_SECRET = os.environ["X_API_SECRET"]
X_ACCESS_TOKEN = os.environ["X_ACCESS_TOKEN"]
X_ACCESS_SECRET = os.environ["X_ACCESS_SECRET"]

READY_STATUS = os.environ.get("NOTION_READY_STATUS", "Ready to Post")
POSTED_STATUS = os.environ.get("NOTION_POSTED_STATUS", "Posted")
TWEET_PROPERTY = os.environ.get("NOTION_TWEET_PROPERTY", "Tweet")
STATUS_PROPERTY = os.environ.get("NOTION_STATUS_PROPERTY", "Status")
POSTED_AT_PROPERTY = os.environ.get("NOTION_POSTED_AT_PROPERTY", "Posted At")

MAX_TWEET_LENGTH = 280


def get_notion_client() -> NotionClient:
    return NotionClient(auth=NOTION_TOKEN)


def get_x_client() -> tweepy.Client:
    return tweepy.Client(
        consumer_key=X_API_KEY,
        consumer_secret=X_API_SECRET,
        access_token=X_ACCESS_TOKEN,
        access_token_secret=X_ACCESS_SECRET,
    )


def fetch_ready_items(notion: NotionClient) -> list[dict]:
    """ステータスが READY_STATUS のアイテムを全件取得する。"""
    results = []
    cursor = None

    while True:
        kwargs = {
            "database_id": NOTION_DATABASE_ID,
            "filter": {
                "property": STATUS_PROPERTY,
                "select": {"equals": READY_STATUS},
            },
            "sorts": [{"timestamp": "created_time", "direction": "ascending"}],
        }
        if cursor:
            kwargs["start_cursor"] = cursor

        response = notion.databases.query(**kwargs)
        results.extend(response["results"])

        if not response.get("has_more"):
            break
        cursor = response.get("next_cursor")

    return results


def extract_tweet_text(page: dict) -> str | None:
    """ページのプロパティからツイート本文を取り出す。"""
    props = page.get("properties", {})
    prop = props.get(TWEET_PROPERTY)
    if not prop:
        return None

    prop_type = prop.get("type")

    if prop_type == "title":
        parts = prop.get("title", [])
    elif prop_type == "rich_text":
        parts = prop.get("rich_text", [])
    else:
        log.warning("Unsupported property type '%s' for '%s'", prop_type, TWEET_PROPERTY)
        return None

    text = "".join(p.get("plain_text", "") for p in parts).strip()
    return text or None


def mark_as_posted(notion: NotionClient, page_id: str) -> None:
    """投稿済みステータスと日時を Notion に書き戻す。"""
    props: dict = {
        STATUS_PROPERTY: {"select": {"name": POSTED_STATUS}},
    }

    # "Posted At" プロパティが存在すれば日時を記録する
    database = notion.databases.retrieve(NOTION_DATABASE_ID)
    db_props = database.get("properties", {})
    if POSTED_AT_PROPERTY in db_props:
        props[POSTED_AT_PROPERTY] = {
            "date": {"start": datetime.now(timezone.utc).isoformat()}
        }

    notion.pages.update(page_id=page_id, properties=props)


def post_to_x(client: tweepy.Client, text: str) -> str:
    """Xに投稿し、ツイートIDを返す。"""
    if len(text) > MAX_TWEET_LENGTH:
        text = text[: MAX_TWEET_LENGTH - 1] + "…"
    response = client.create_tweet(text=text)
    return str(response.data["id"])


def like_tweet(client: tweepy.Client, tweet_id: str) -> None:
    """自分のツイートにいいね（大好き❤️）をつける。"""
    me = client.get_me()
    client.like(user_id=me.data.id, tweet_id=tweet_id)


def run() -> None:
    notion = get_notion_client()
    x_client = get_x_client()

    items = fetch_ready_items(notion)
    log.info("Found %d item(s) ready to post.", len(items))

    if not items:
        log.info("Nothing to post. Exiting.")
        return

    posted = 0
    failed = 0

    for page in items:
        page_id = page["id"]
        text = extract_tweet_text(page)

        if not text:
            log.warning("Page %s has no tweet text. Skipping.", page_id)
            continue

        log.info("Posting: %.60s…", text)
        try:
            tweet_id = post_to_x(x_client, text)
            mark_as_posted(notion, page_id)
            log.info("Posted tweet %s for page %s.", tweet_id, page_id)
            try:
                like_tweet(x_client, tweet_id)
                log.info("Liked tweet %s ❤️", tweet_id)
            except Exception as like_exc:
                log.warning("Could not like tweet %s: %s", tweet_id, like_exc)
            posted += 1
        except Exception as exc:
            log.error("Failed to post page %s: %s", page_id, exc)
            failed += 1

    log.info("Done. posted=%d, failed=%d", posted, failed)
    if failed:
        sys.exit(1)


if __name__ == "__main__":
    run()
