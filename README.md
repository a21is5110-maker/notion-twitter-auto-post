# 秘書よべ — Notion → Twitter 自動投稿ボット

Notion データベースの「投稿待ち」ページを自動検出し、Twitter / X に投稿します。

## セットアップ

### 1. Notion データベースの準備

以下のプロパティを持つデータベースを作成してください。

| プロパティ名 | 型     | 説明                              |
|------------|--------|----------------------------------|
| Content    | Title  | ツイート本文（280 文字以内推奨）    |
| Status     | Select | `Draft` / `Ready` / `Posted`     |
| PostedAt   | Date   | 投稿日時（ボットが自動記入）        |

### 2. API キーの取得

- **Notion**: [Notion Integrations](https://www.notion.so/my-integrations) でインテグレーションを作成し、データベースに接続する
- **Twitter / X**: [Developer Portal](https://developer.twitter.com/) で App を作成し、OAuth 1.0a の認証情報を取得する（Read and Write 権限が必要）

### 3. 環境変数の設定

```bash
cp .env.example .env
# .env をエディタで開き、各 API キーを入力する
```

### 4. 依存関係のインストール

```bash
pip install -r requirements.txt
```

## 使い方

### ポーリングループで起動（常駐モード）

```bash
python main.py
```

デフォルトでは 5 分（300 秒）ごとに Notion をチェックします。
`POLL_INTERVAL_SECONDS` 環境変数で変更できます。

### 一度だけ実行

```bash
python main.py --once
```

## 動作フロー

```
Notion DB (Status=Ready)
        ↓ fetch
  ツイート本文を抽出
        ↓ post
  Twitter に投稿
        ↓ mark
  Status を Posted に更新、PostedAt を記録
```

## ファイル構成

```
.
├── main.py           # エントリーポイント・スケジューラー
├── notion_helper.py  # Notion API ラッパー
├── twitter_helper.py # Twitter API ラッパー
├── config.py         # 環境変数の読み込み
├── requirements.txt
└── .env.example
```
