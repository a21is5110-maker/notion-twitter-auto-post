"""
秘書よべ — Notion → Twitter 自動投稿ボット

使い方:
  python main.py          # ポーリングループを開始
  python main.py --once   # 一度だけ実行して終了
"""

import argparse
import logging
import schedule
import time

import config
import notion_helper
import twitter_helper

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
log = logging.getLogger(__name__)


def run_once() -> None:
    """Notion から Ready ページを取得してツイートし、Posted にマークする。"""
    pages = notion_helper.fetch_ready_pages()
    if not pages:
        log.info("投稿待ちのページはありません。")
        return

    for page in pages:
        page_id = page["id"]
        text = notion_helper.extract_tweet_text(page)

        if not text:
            log.warning("ページ %s にテキストがないためスキップします。", page_id)
            continue

        if len(text) > 280:
            log.warning(
                "ページ %s のテキストが 280 文字を超えています（%d 文字）。先頭 280 文字で投稿します。",
                page_id,
                len(text),
            )
            text = text[:280]

        try:
            tweet_id = twitter_helper.post_tweet(text)
            log.info("ツイート投稿成功 (tweet_id=%s): %s", tweet_id, text[:50])
            notion_helper.mark_as_posted(page_id)
            log.info("Notion ページ %s を Posted にマークしました。", page_id)
        except Exception as exc:
            log.error("ページ %s の投稿に失敗しました: %s", page_id, exc)


def main() -> None:
    parser = argparse.ArgumentParser(description="Notion → Twitter 自動投稿ボット")
    parser.add_argument(
        "--once",
        action="store_true",
        help="一度だけ実行して終了する（スケジューラーを起動しない）",
    )
    args = parser.parse_args()

    if args.once:
        run_once()
        return

    interval = config.POLL_INTERVAL_SECONDS
    log.info("秘書よべ 起動。%d 秒ごとに Notion をチェックします。", interval)

    run_once()
    schedule.every(interval).seconds.do(run_once)

    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    main()
