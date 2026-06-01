#!/usr/bin/env python3
"""朝のバスネタリサーチ - 教育系バズツイートをNotionに自動保存"""

import os
import sys
import argparse
from dotenv import load_dotenv
import anthropic
from notion_client import Client

from src.content_gen import generate_morning_tweets
from src.notion_client_wrapper import save_tweets_to_notion, ensure_database_schema


def main():
    load_dotenv()

    parser = argparse.ArgumentParser(description="朝のバスネタリサーチ")
    parser.add_argument("--count", type=int, default=5, help="生成するツイート数 (デフォルト: 5)")
    parser.add_argument("--preview", action="store_true", help="Notionに保存せずプレビューのみ")
    args = parser.parse_args()

    anthropic_key = os.environ.get("ANTHROPIC_API_KEY")
    notion_key = os.environ.get("NOTION_API_KEY")
    database_id = os.environ.get("NOTION_DATABASE_ID")

    if not anthropic_key:
        print("エラー: ANTHROPIC_API_KEY が設定されていません (.env を確認してください)")
        sys.exit(1)

    print("=" * 50)
    print("🚌 朝のバスネタリサーチ 起動中...")
    print("=" * 50)

    print(f"\n📝 教育系バズツイートを {args.count} 本生成中...\n")
    claude = anthropic.Anthropic(api_key=anthropic_key)
    tweets = generate_morning_tweets(claude, count=args.count)

    print("\n--- 生成されたツイート ---\n")
    for i, tweet in enumerate(tweets, 1):
        print(f"【{i}】[{tweet.get('category')}] {tweet.get('hook')}")
        print(f"  {tweet.get('content')}")
        print(f"  文字数: {len(tweet.get('content', ''))}")
        print()

    if args.preview:
        print("プレビューモード: Notionへの保存をスキップしました")
        return

    if not notion_key or not database_id:
        print("⚠️  NOTION_API_KEY または NOTION_DATABASE_ID が未設定のため、Notionへの保存をスキップ")
        print("   .env ファイルに設定してください (.env.example 参照)")
        return

    print("\n📦 Notionデータベースに保存中...\n")
    notion = Client(auth=notion_key)

    ensure_database_schema(notion, database_id)
    pages = save_tweets_to_notion(notion, database_id, tweets)

    print(f"\n✅ {len(pages)} 件のツイート案をNotionに保存しました！")
    print("\n次のステップ:")
    print("  1. Notionでツイート案を確認・編集")
    print("  2. 気に入ったものを「投稿済み」に変更してTwitter/Xに投稿")


if __name__ == "__main__":
    main()
