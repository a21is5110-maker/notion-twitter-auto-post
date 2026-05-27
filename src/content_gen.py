import anthropic
import json

SYSTEM_PROMPT = """あなたは教育系SNSコンテンツの専門家です。
朝の通勤バスで読んでもらえる、短くて面白い教育系ツイート案を作成します。

条件：
- 140文字以内（日本語）
- 「へえ！」「知らなかった！」と思わせる雑学・豆知識
- 科学、歴史、言語、心理学、経済など幅広いジャンル
- リツイートされやすい驚きの事実
- ハッシュタグ2〜3個付き（#雑学 #豆知識 など）
- 絵文字を効果的に使用"""


def generate_morning_tweets(client: anthropic.Anthropic, count: int = 5) -> list[dict]:
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=2048,
        system=SYSTEM_PROMPT,
        messages=[
            {
                "role": "user",
                "content": f"""朝のバス通勤者向けに、教育系バズツイートを{count}本作成してください。

以下のJSON形式で返してください：
{{
  "tweets": [
    {{
      "content": "ツイート本文（140文字以内、ハッシュタグ含む）",
      "category": "カテゴリ（科学/歴史/心理学/言語/経済/その他）",
      "hook": "このツイートのキャッチポイント（一言）"
    }}
  ]
}}

バリエーションを持たせ、異なるカテゴリから選んでください。""",
            }
        ],
    )

    text = response.content[0].text
    start = text.find("{")
    end = text.rfind("}") + 1
    data = json.loads(text[start:end])
    return data.get("tweets", [])
