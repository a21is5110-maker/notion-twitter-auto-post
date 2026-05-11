# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## プロジェクト概要

**notion-twitter-auto-post** は、Notion のデータベースに登録されたコンテンツを自動的に Twitter (X) へ投稿するための自動化ツールです。

このリポジトリは現在初期段階にあり、コードはまだ存在しません。実装を始める際は、このファイルを更新してください。

## 想定するアーキテクチャ

このプロジェクトが目指すのは以下のフロー:

```
Notion データベース → （ポーリングまたは Webhook）→ 投稿処理 → Twitter (X) API
```

主な責務:
- **Notion 連携**: Notion API を使用してデータベースのエントリを取得し、投稿済みかどうかを管理する
- **Twitter 投稿**: Twitter API v2 を使用してツイートを送信する
- **スケジューリング**: 定期実行（cron / GitHub Actions など）で自動ポーリングまたはイベント駆動で動作する

## 開発を始める際の指針

### 技術選定が未確定の項目

実装開始前に以下を決定してください:

- **言語・ランタイム**: Python / Node.js / Deno など
- **実行環境**: GitHub Actions / Cloud Functions / ローカル cron など
- **状態管理**: 投稿済みフラグを Notion プロパティで管理するか、外部 DB（例: Firestore, SQLite）で管理するか
- **認証情報の管理**: 環境変数（`.env`）または シークレット管理サービス

### 必要な API 認証情報

- Notion Integration Token と対象データベース ID
- Twitter Developer App の OAuth 2.0 / API キー一式

## 実装後に更新すべき内容

コードが追加されたら、このファイルに以下を追記してください:

- ビルド・テスト・lint の実行コマンド
- 環境変数のセットアップ手順
- ディレクトリ構成と各モジュールの役割
- Notion データベースのスキーマ（投稿管理に使うプロパティ名など）
- デプロイ手順
