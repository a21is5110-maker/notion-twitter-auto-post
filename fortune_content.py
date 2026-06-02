"""占い集客向けのツイートテンプレート集。Notionにコンテンツがない場合のフォールバックとして使用。"""

import random
from datetime import date

ZODIAC_SIGNS = [
    "おひつじ座", "おうし座", "ふたご座", "かに座",
    "しし座", "おとめ座", "てんびん座", "さそり座",
    "いて座", "やぎ座", "みずがめ座", "うお座",
]

FORTUNE_KEYWORDS = [
    ("金運", "💰"), ("恋愛運", "💕"), ("仕事運", "✨"), ("健康運", "🌿"),
    ("対人運", "🤝"), ("総合運", "⭐"),
]

LUCKY_COLORS = ["赤", "青", "緑", "白", "金", "紫", "ピンク", "オレンジ"]
LUCKY_ITEMS = ["水晶", "アメジスト", "ローズクォーツ", "タイガーアイ", "ムーンストーン"]

CTA_TEMPLATES = [
    "▶ 詳しい鑑定はプロフィールのリンクから✨",
    "▶ 個別鑑定のご予約はDMまで💌",
    "▶ もっと詳しく知りたい方はリンクから🔮",
    "▶ 無料相談受付中！お気軽にDMを📩",
]

DAILY_TEMPLATES = [
    """{sign}の今日の運勢 {keyword_emoji}

{keyword_name}が特に輝く一日です。
ラッキーカラーは「{lucky_color}」。
{cta}

#占い #{sign} #今日の運勢""",

    """✨ 今日の一言占い ✨

{sign}さんへ――
「{lucky_item}」があなたを守ってくれる日。
{keyword_name}に良い変化が訪れそう。

{cta}

#スピリチュアル #占い #開運""",

    """🔮 {today} の運勢 🔮

{sign} → {keyword_name}：◎

今日のキーワードは「{lucky_color}」と「つながり」。
小さな縁を大切に。

{cta}

#占い #今日の運勢 #開運""",
]

PROMO_TEMPLATES = [
    """✨ 占いで人生が変わった！ ✨

「仕事を変えるか迷っていたけど、鑑定後に決断できた」
「恋愛のモヤモヤが一瞬で晴れた」

あなたの悩みも一緒に解決しましょう。
{cta}

#占い #人生相談 #スピリチュアル""",

    """🌙 迷っているあなたへ 🌙

占いは「答えを決める」ものではなく
「自分の本音に気づく」ツールです。

今この瞬間の自分の気持ち、一緒に確認しませんか？
{cta}

#占い #自己理解 #スピリチュアル""",

    """💎 鑑定実績 500名突破！ 💎

タロット・星座・数秘術を組み合わせた
オリジナルの鑑定で、多くの方に喜んでいただいています。

初回限定 無料相談実施中✨
{cta}

#タロット #星占い #数秘術""",
]


def generate_daily_fortune() -> str:
    """ランダムな今日の運勢ツイートを生成する。"""
    sign = random.choice(ZODIAC_SIGNS)
    keyword_name, keyword_emoji = random.choice(FORTUNE_KEYWORDS)
    lucky_color = random.choice(LUCKY_COLORS)
    lucky_item = random.choice(LUCKY_ITEMS)
    cta = random.choice(CTA_TEMPLATES)
    template = random.choice(DAILY_TEMPLATES)
    today = date.today().strftime("%m/%d")

    return template.format(
        sign=sign,
        keyword_name=keyword_name,
        keyword_emoji=keyword_emoji,
        lucky_color=lucky_color,
        lucky_item=lucky_item,
        cta=cta,
        today=today,
    )


def generate_promo_tweet() -> str:
    """集客向けプロモーションツイートを生成する。"""
    cta = random.choice(CTA_TEMPLATES)
    template = random.choice(PROMO_TEMPLATES)
    return template.format(cta=cta)


def generate_tweet(promo_ratio: float = 0.3) -> str:
    """promo_ratio の確率でプロモ、それ以外は運勢ツイートを返す。"""
    if random.random() < promo_ratio:
        return generate_promo_tweet()
    return generate_daily_fortune()
