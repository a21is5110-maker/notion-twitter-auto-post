# 朝のバスネタリサーチ 🚌

朝の通勤バスで読んでもらえる教育系バズツイートを自動生成し、Notionに保存するツールです。

## セットアップ

### 1. 依存パッケージのインストール

```bash
pip install -r requirements.txt
```

### 2. 環境変数の設定

```bash
cp .env.example .env
```

`.env` を編集して以下を設定：

| 変数名 | 取得先 |
|--------|--------|
| `ANTHROPIC_API_KEY` | [Anthropic Console](https://console.anthropic.com/) |
| `NOTION_API_KEY` | [Notion Integrations](https://www.notion.so/my-integrations) |
| `NOTION_DATABASE_ID` | NotionデータベースのURL末尾のID |

### 3. NotionデータベースIDの取得

NotionでデータベースページのURLを開くと：
```
https://www.notion.so/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx?v=...
```
`?v=` の前の32文字がデータベースIDです。

作成したIntegrationをデータベースページに「接続」してください。

## 使い方

```bash
# 5本のツイート案を生成してNotionに保存
python main.py

# 10本生成
python main.py --count 10

# Notionに保存せずプレビューのみ
python main.py --preview
```

## ワークフロー

```
[main.py 実行]
    ↓
[Claude APIで教育系バズツイート生成]
    ↓
[Notionデータベースに「下書き」として保存]
    ↓
[Notionで確認・編集]
    ↓
[気に入ったものをTwitter/Xに投稿]
    ↓
[Notionのステータスを「投稿済み」に変更]
```

## Notionデータベースのカラム

| カラム | 内容 |
|--------|------|
| Name | ツイートのキャッチポイント |
| Content | ツイート本文（140文字以内） |
| Category | 科学 / 歴史 / 心理学 / 言語 / 経済 / その他 |
| Status | 下書き / 投稿済み / ボツ |
| Date | 生成日 |
