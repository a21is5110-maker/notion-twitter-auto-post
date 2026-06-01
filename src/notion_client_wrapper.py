from datetime import date
from notion_client import Client


def save_tweets_to_notion(notion: Client, database_id: str, tweets: list[dict]) -> list[str]:
    """Save tweet drafts to Notion database. Returns list of created page URLs."""
    created_pages = []
    today = date.today().isoformat()

    for tweet in tweets:
        page = notion.pages.create(
            parent={"database_id": database_id},
            properties={
                "Name": {
                    "title": [{"text": {"content": tweet.get("hook", "朝ネタ")}}]
                },
                "Content": {
                    "rich_text": [{"text": {"content": tweet.get("content", "")}}]
                },
                "Category": {
                    "select": {"name": tweet.get("category", "その他")}
                },
                "Status": {
                    "select": {"name": "下書き"}
                },
                "Date": {
                    "date": {"start": today}
                },
            },
        )
        url = page.get("url", "")
        created_pages.append(url)
        print(f"  ✓ [{tweet.get('category')}] {tweet.get('hook')}")

    return created_pages


def ensure_database_schema(notion: Client, database_id: str) -> None:
    """Add missing properties to the Notion database if needed."""
    db = notion.databases.retrieve(database_id=database_id)
    existing_props = set(db["properties"].keys())

    required_props = {}

    if "Content" not in existing_props:
        required_props["Content"] = {"rich_text": {}}
    if "Category" not in existing_props:
        required_props["Category"] = {
            "select": {
                "options": [
                    {"name": "科学", "color": "blue"},
                    {"name": "歴史", "color": "orange"},
                    {"name": "心理学", "color": "purple"},
                    {"name": "言語", "color": "green"},
                    {"name": "経済", "color": "yellow"},
                    {"name": "その他", "color": "gray"},
                ]
            }
        }
    if "Status" not in existing_props:
        required_props["Status"] = {
            "select": {
                "options": [
                    {"name": "下書き", "color": "gray"},
                    {"name": "投稿済み", "color": "green"},
                    {"name": "ボツ", "color": "red"},
                ]
            }
        }
    if "Date" not in existing_props:
        required_props["Date"] = {"date": {}}

    if required_props:
        notion.databases.update(database_id=database_id, properties=required_props)
        print(f"  ✓ データベーススキーマを更新しました ({list(required_props.keys())})")
