# Threads 朝鑑定誘導 自動投稿ツール
**@todaysdragon** 向け　5〜9時 1時間おき自動投稿

---

## セットアップ

### 1. 依存パッケージのインストール
```bash
pip install -r requirements.txt
```

### 2. 環境変数の設定
```bash
cp .env.example .env
# .env を編集して THREADS_ACCESS_TOKEN と THREADS_USER_ID を入力
```

#### アクセストークンの取得方法
1. [Meta Developer Portal](https://developers.facebook.com/) でアプリを作成
2. **Threads API** を有効化
3. `threads_basic` + `threads_content_publish` の権限を付与
4. 短期トークンを長期トークン（60日）に交換

#### ユーザーIDの確認
```bash
curl "https://graph.threads.net/v1.0/me?fields=id,username&access_token=YOUR_TOKEN"
```

---

## 投稿ファイルの作成

`posts/` フォルダに以下の命名規則でファイルを作成：
```
posts/YYYY-MM-DD_asa-kantei-yudo.md
```

---

## 手動実行（テスト）

```bash
# 環境変数を読み込んで実行
export $(cat .env | xargs)

# 現在時刻の投稿を送信
python poster.py

# 時間を指定して実行（テスト用）
python poster.py 5
```

---

## cron による自動実行（毎日5〜9時）

```bash
crontab -e
```

以下を追加（`/path/to/` は実際のパスに変更）：
```cron
0 5 * * * cd /path/to/notion-twitter-auto-post && export $(cat .env | xargs) && python poster.py >> logs/post.log 2>&1
0 6 * * * cd /path/to/notion-twitter-auto-post && export $(cat .env | xargs) && python poster.py >> logs/post.log 2>&1
0 7 * * * cd /path/to/notion-twitter-auto-post && export $(cat .env | xargs) && python poster.py >> logs/post.log 2>&1
0 8 * * * cd /path/to/notion-twitter-auto-post && export $(cat .env | xargs) && python poster.py >> logs/post.log 2>&1
0 9 * * * cd /path/to/notion-twitter-auto-post && export $(cat .env | xargs) && python poster.py >> logs/post.log 2>&1
```
