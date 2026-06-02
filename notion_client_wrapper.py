import os
from notion_client import Client


class NotionWrapper:
    """Notion DBから投稿予定の占いコンテンツを取得し、投稿済みに更新する。"""

    STATUS_PENDING = "未投稿"
    STATUS_POSTED = "投稿済み"

    def __init__(self):
        self.client = Client(auth=os.environ["NOTION_TOKEN"])
        self.database_id = os.environ["NOTION_DATABASE_ID"]

    def fetch_pending_posts(self) -> list[dict]:
        """ステータスが「未投稿」のページを全件取得する。"""
        results = []
        cursor = None

        while True:
            kwargs = {
                "database_id": self.database_id,
                "filter": {
                    "property": "ステータス",
                    "select": {"equals": self.STATUS_PENDING},
                },
                "sorts": [{"property": "投稿予定日時", "direction": "ascending"}],
            }
            if cursor:
                kwargs["start_cursor"] = cursor

            response = self.client.databases.query(**kwargs)
            results.extend(response["results"])

            if not response["has_more"]:
                break
            cursor = response["next_cursor"]

        return results

    def mark_as_posted(self, page_id: str) -> None:
        """指定ページのステータスを「投稿済み」に更新する。"""
        self.client.pages.update(
            page_id=page_id,
            properties={
                "ステータス": {"select": {"name": self.STATUS_POSTED}},
            },
        )

    def extract_tweet_text(self, page: dict) -> str:
        """NotionページからTwitter投稿テキストを抽出する。"""
        props = page["properties"]

        # 「ツイート本文」プロパティを優先使用
        if "ツイート本文" in props:
            rich_texts = props["ツイート本文"].get("rich_text", [])
            text = "".join(rt["plain_text"] for rt in rich_texts).strip()
            if text:
                return text

        # フォールバック: タイトルを使用
        title_prop = props.get("タイトル") or props.get("Name") or {}
        title_parts = title_prop.get("title", [])
        return "".join(tp["plain_text"] for tp in title_parts).strip()
