"""
Notion データベースから「投稿待ち」ページを取得し、投稿済みにマークするヘルパー。

想定するデータベース列:
  - Content (title)   : ツイート本文
  - Status (select)   : "Draft" | "Ready" | "Posted"
  - PostedAt (date)   : 投稿日時（自動記入）
"""

from datetime import datetime, timezone
from notion_client import Client
import config


_client = Client(auth=config.NOTION_TOKEN)


def fetch_ready_pages() -> list[dict]:
    """Status が "Ready" のページ一覧を返す。"""
    response = _client.databases.query(
        database_id=config.NOTION_DATABASE_ID,
        filter={
            "property": "Status",
            "select": {"equals": "Ready"},
        },
    )
    return response.get("results", [])


def extract_tweet_text(page: dict) -> str:
    """ページの Content プロパティからテキストを取得する。"""
    props = page.get("properties", {})

    # title 型
    title_prop = props.get("Content", {})
    rich_texts = title_prop.get("title", [])
    if not rich_texts:
        # rich_text 型にもフォールバック
        rich_texts = title_prop.get("rich_text", [])

    return "".join(rt.get("plain_text", "") for rt in rich_texts).strip()


def mark_as_posted(page_id: str) -> None:
    """Status を "Posted" にし、PostedAt に現在時刻を記録する。"""
    now = datetime.now(timezone.utc).isoformat()
    _client.pages.update(
        page_id=page_id,
        properties={
            "Status": {"select": {"name": "Posted"}},
            "PostedAt": {"date": {"start": now}},
        },
    )
