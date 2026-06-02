#!/usr/bin/env python3
"""
notion-twitter-auto-post
Notionの占いコンテンツを定期的にTwitterへ自動投稿し、占い客を集客する。
"""

import logging
import os
import sys
import time

import schedule
from dotenv import load_dotenv

from fortune_content import generate_tweet
from notion_client_wrapper import NotionWrapper
from twitter_client_wrapper import TwitterWrapper

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
log = logging.getLogger(__name__)


def post_once(notion: NotionWrapper, twitter: TwitterWrapper) -> None:
    """Notionから1件取得して投稿する。なければフォールバックコンテンツを投稿。"""
    pending = notion.fetch_pending_posts()

    if pending:
        page = pending[0]
        text = notion.extract_tweet_text(page)
        if not text:
            log.warning("ページ %s のツイート本文が空のためスキップ", page["id"])
            return
        tweet_id = twitter.post(text)
        notion.mark_as_posted(page["id"])
        log.info("Notion投稿完了: tweet_id=%s | %s", tweet_id, text[:40])
    else:
        # Notionにコンテンツがない場合は生成コンテンツを投稿
        text = generate_tweet()
        tweet_id = twitter.post(text)
        log.info("生成コンテンツ投稿完了: tweet_id=%s | %s", tweet_id, text[:40])


def run_scheduler(notion: NotionWrapper, twitter: TwitterWrapper) -> None:
    interval_hours = int(os.environ.get("POST_INTERVAL_HOURS", "3"))
    log.info("スケジューラ起動: %d時間ごとに投稿します", interval_hours)

    # 起動直後に1回実行
    post_once(notion, twitter)

    schedule.every(interval_hours).hours.do(post_once, notion=notion, twitter=twitter)

    while True:
        schedule.run_pending()
        time.sleep(60)


def main() -> None:
    required_vars = [
        "NOTION_TOKEN",
        "NOTION_DATABASE_ID",
        "TWITTER_API_KEY",
        "TWITTER_API_SECRET",
        "TWITTER_ACCESS_TOKEN",
        "TWITTER_ACCESS_TOKEN_SECRET",
    ]
    missing = [v for v in required_vars if not os.environ.get(v)]
    if missing:
        log.error("環境変数が設定されていません: %s", ", ".join(missing))
        sys.exit(1)

    notion = NotionWrapper()
    twitter = TwitterWrapper()

    mode = sys.argv[1] if len(sys.argv) > 1 else "schedule"

    if mode == "once":
        post_once(notion, twitter)
    elif mode == "schedule":
        run_scheduler(notion, twitter)
    else:
        print("使い方: python main.py [once|schedule]")
        sys.exit(1)


if __name__ == "__main__":
    main()
