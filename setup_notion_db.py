#!/usr/bin/env python3
"""
Notionデータベースのセットアップ確認スクリプト。
必要なプロパティが存在するかチェックし、不足があれば案内する。
"""

import os
import sys

from dotenv import load_dotenv
from notion_client import Client

load_dotenv()

REQUIRED_PROPERTIES = {
    "タイトル": "title",
    "ツイート本文": "rich_text",
    "ステータス": "select",
    "投稿予定日時": "date",
}


def check_database() -> None:
    token = os.environ.get("NOTION_TOKEN")
    db_id = os.environ.get("NOTION_DATABASE_ID")

    if not token or not db_id:
        print("エラー: NOTION_TOKEN と NOTION_DATABASE_ID を .env に設定してください")
        sys.exit(1)

    client = Client(auth=token)
    try:
        db = client.databases.retrieve(database_id=db_id)
    except Exception as e:
        print(f"データベース取得失敗: {e}")
        sys.exit(1)

    existing = db["properties"]
    print(f"データベース名: {db['title'][0]['plain_text']}")
    print()

    ok = True
    for name, expected_type in REQUIRED_PROPERTIES.items():
        if name in existing:
            actual_type = existing[name]["type"]
            status = "✅" if actual_type == expected_type else f"⚠️ (型が {actual_type})"
        else:
            status = "❌ 存在しません"
            ok = False
        print(f"  {status}  {name}")

    print()
    if ok:
        print("✅ データベース設定は正常です。")
    else:
        print("❌ 不足プロパティがあります。Notionで追加してください。")
        print()
        print("ステータスの選択肢として「未投稿」と「投稿済み」を追加してください。")


if __name__ == "__main__":
    check_database()
