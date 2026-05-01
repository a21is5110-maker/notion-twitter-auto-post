#!/usr/bin/env python3
"""
Threads 朝鑑定誘導 自動投稿スクリプト
@todaysdragon 向け　5〜9時 1時間おき投稿
"""

import os
import re
import sys
import time
import datetime
import requests
from zoneinfo import ZoneInfo

THREADS_API_BASE = "https://graph.threads.net/v1.0"
JST = ZoneInfo("Asia/Tokyo")

ACCESS_TOKEN = os.environ["THREADS_ACCESS_TOKEN"]
USER_ID = os.environ["THREADS_USER_ID"]


def create_container(text: str) -> str:
    url = f"{THREADS_API_BASE}/{USER_ID}/threads"
    resp = requests.post(url, data={
        "media_type": "TEXT",
        "text": text,
        "access_token": ACCESS_TOKEN,
    })
    resp.raise_for_status()
    return resp.json()["id"]


def publish_container(creation_id: str) -> dict:
    url = f"{THREADS_API_BASE}/{USER_ID}/threads_publish"
    resp = requests.post(url, data={
        "creation_id": creation_id,
        "access_token": ACCESS_TOKEN,
    })
    resp.raise_for_status()
    return resp.json()


def post_to_threads(text: str) -> str:
    creation_id = create_container(text)
    time.sleep(5)  # Threads API requires a short wait between create and publish
    result = publish_container(creation_id)
    return result["id"]


def parse_posts(filepath: str) -> dict[int, str]:
    """mdファイルから時間ごとの投稿文を取得する。{hour: text}"""
    with open(filepath, encoding="utf-8") as f:
        content = f.read()

    posts = {}
    pattern = re.compile(
        r"### 🕔 (\d+)時投稿\n\n(.*?)(?=\n---|\Z)", re.DOTALL
    )
    for match in pattern.finditer(content):
        hour = int(match.group(1))
        text = match.group(2).strip()
        # マークダウン装飾（**bold**）を除去
        text = re.sub(r"\*\*(.*?)\*\*", r"\1", text)
        posts[hour] = text
    return posts


def today_post_file() -> str:
    today = datetime.date.today().strftime("%Y-%m-%d")
    path = os.path.join(os.path.dirname(__file__), "posts", f"{today}_asa-kantei-yudo.md")
    return path


def main():
    now = datetime.datetime.now(JST)
    hour = now.hour

    if len(sys.argv) > 1:
        hour = int(sys.argv[1])
        print(f"[DEBUG] 指定時間: {hour}時")

    post_file = today_post_file()
    if not os.path.exists(post_file):
        print(f"[ERROR] 投稿ファイルが見つかりません: {post_file}")
        sys.exit(1)

    posts = parse_posts(post_file)
    if hour not in posts:
        print(f"[ERROR] {hour}時の投稿が見つかりません（対応時間: {sorted(posts.keys())}）")
        sys.exit(1)

    text = posts[hour]
    print(f"[INFO] {hour}時の投稿を送信中...")
    print("-" * 40)
    print(text)
    print("-" * 40)

    post_id = post_to_threads(text)
    print(f"[OK] 投稿完了 → post_id: {post_id}")


if __name__ == "__main__":
    main()
