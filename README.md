# Notion → X 自動投稿

NotionデータベースのアイテムをXに自動投稿するスクリプトです。  
GitHub Actionsで定期実行（デフォルト: 毎日9:00 JST）します。

## Notionデータベースのセットアップ

データベースに以下のプロパティを追加してください。

| プロパティ名 | 種類 | 説明 |
|---|---|---|
| `Tweet` | タイトル または テキスト | 投稿する文章（280字以内） |
| `Status` | セレクト | `Ready to Post` → 投稿後 `Posted` に変更 |
| `Posted At` | 日付 | 投稿日時（任意） |

投稿したいアイテムの `Status` を **"Ready to Post"** に設定してください。

## 必要なAPIキー

### Notion
1. [Notion Integrations](https://www.notion.so/my-integrations) でインテグレーションを作成
2. `NOTION_TOKEN` を取得
3. 対象データベースでインテグレーションに権限を付与
4. データベースURLから `NOTION_DATABASE_ID` を取得

### X (Twitter) API v2
1. [X Developer Portal](https://developer.twitter.com/) でアプリを作成
2. **Read and Write** 権限を有効化
3. API Key / Secret、Access Token / Secret を取得

## ローカル実行

```bash
# 依存ライブラリのインストール
pip install -r requirements.txt

# 環境変数を設定
cp .env.example .env
# .env を編集して各キーを入力

# 実行 (python-dotenv がある場合)
pip install python-dotenv
python -c "from dotenv import load_dotenv; load_dotenv()" && python post_to_x.py

# または direnv / export で環境変数を設定してから
python post_to_x.py
```

## GitHub Actions セットアップ

リポジトリの **Settings → Secrets and variables → Actions** に以下を登録してください。

| Secret名 | 値 |
|---|---|
| `NOTION_TOKEN` | Notionインテグレーショントークン |
| `NOTION_DATABASE_ID` | NotionデータベースID |
| `X_API_KEY` | X API Key |
| `X_API_SECRET` | X API Key Secret |
| `X_ACCESS_TOKEN` | X Access Token |
| `X_ACCESS_SECRET` | X Access Token Secret |

## 実行スケジュールの変更

`.github/workflows/auto-post.yml` の `cron` を編集してください。

```yaml
# 例: 毎日 12:00 JST (= 03:00 UTC)
- cron: "0 3 * * *"
```

## カスタマイズ

環境変数でプロパティ名や投稿ステータスを変更できます。

| 環境変数 | デフォルト | 説明 |
|---|---|---|
| `NOTION_TWEET_PROPERTY` | `Tweet` | ツイート本文のプロパティ名 |
| `NOTION_STATUS_PROPERTY` | `Status` | ステータスのプロパティ名 |
| `NOTION_READY_STATUS` | `Ready to Post` | 投稿対象のステータス値 |
| `NOTION_POSTED_STATUS` | `Posted` | 投稿後に設定するステータス値 |
| `NOTION_POSTED_AT_PROPERTY` | `Posted At` | 投稿日時のプロパティ名 |
