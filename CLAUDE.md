# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Copy and fill in environment variables before running
cp .env.example .env

# Run once (single post)
python main.py once

# Run on a schedule (posts every POST_INTERVAL_HOURS hours, default 3)
python main.py schedule

# Verify Notion DB properties are correctly configured
python setup_notion_db.py
```

## Architecture

This is a single-process Python script with no web server or database of its own.

**Flow:** `main.py` → `NotionWrapper.fetch_pending_posts()` → `TwitterWrapper.post()` → `NotionWrapper.mark_as_posted()`

**Fallback:** When no "未投稿" pages exist in Notion, `fortune_content.generate_tweet()` produces a random fortune or promo tweet from hardcoded templates.

**Key design decisions:**
- State is stored entirely in Notion (ステータス: 未投稿/投稿済み). There is no local state file.
- `main.py once` runs the post loop exactly once and exits — suitable for cron. `main.py schedule` blocks forever using the `schedule` library.
- `NotionWrapper.extract_tweet_text()` prefers the "ツイート本文" rich_text property, falling back to the page title.
- Tweet text longer than `MAX_TWEET_LENGTH` (default 140) is truncated with `…` appended.

## Environment Variables

All required vars are validated at startup in `main.py`. The script exits immediately with an error if any are missing. See `.env.example` for the full list.
