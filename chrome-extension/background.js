const NOTE_ARTICLE_PATTERN = /^https:\/\/note\.com\/[^/]+\/n\/[^/]+/;

// ===== ユーティリティ =====

function getTodayKey() {
  const jst = new Date(Date.now() + 9 * 60 * 60 * 1000);
  return `${jst.getUTCFullYear()}-${String(jst.getUTCMonth()+1).padStart(2,'0')}-${String(jst.getUTCDate()).padStart(2,'0')}`;
}

async function isAlreadyPosted(key) {
  const { postedUrls = [] } = await chrome.storage.local.get('postedUrls');
  return postedUrls.includes(key);
}

async function markAsPosted(key) {
  const { postedUrls = [] } = await chrome.storage.local.get('postedUrls');
  if (!postedUrls.includes(key)) {
    postedUrls.push(key);
    if (postedUrls.length > 200) postedUrls.shift();
    await chrome.storage.local.set({ postedUrls });
  }
}

// ===== 恋みくじ 自動投稿 =====

// 暦データをインラインで保持（fortune/data.js と同期）
const FORTUNE_DATA = {
  "2026-06-01": {
    date: "2026年6月1日（月）", kyusei: "六白金星", eto: "甲午", rokuyo: "先負",
    special: ["🦊 午の日・お稲荷さんの日"],
    koi: ["大吉｜想いを伝えて。今日の言葉は魔法になる","吉｜待っていた連絡が来るかも","中吉｜笑顔が最強の武器","小吉｜新しい出会いの予感","末吉｜焦らなくていい。縁は必ず巡ってくる","凶｜今日は自分を整える日"]
  },
  "2026-06-02": {
    date: "2026年6月2日（火）", kyusei: "五黄土星", eto: "乙未", rokuyo: "仏滅",
    special: ["🦄 麒麟日"],
    koi: ["大吉｜麒麟日パワー全開！告白・プロポーズに最高の日","大吉｜奇跡が起きる日。思い切って動いてみて","吉｜運命の出会いが待っている","吉｜復縁のチャンス。相手の心が開く日","中吉｜関係が一歩前進する予感","小吉｜良縁を引き寄せる言葉を声に出して"]
  },
  "2026-06-03": {
    date: "2026年6月3日（水）", kyusei: "四緑木星", eto: "丙申", rokuyo: "大安",
    special: [],
    koi: ["大吉｜大安の力で恋が加速","吉｜相手の本音が見える日","中吉｜距離が縮まるきっかけがやってくる","小吉｜自分磨きの成果が出始める","末吉｜焦らず流れに乗ることが吉","吉｜思わぬところから縁がつながる"]
  },
  "2026-06-04": {
    date: "2026年6月4日（木）", kyusei: "三碧木星", eto: "丁酉", rokuyo: "赤口",
    special: [],
    koi: ["吉｜コミュニケーションが実を結ぶ日","中吉｜LINEの一言が関係を変えるかも","吉｜相手があなたを意識し始めている","小吉｜今日の笑顔は10倍の効果あり","末吉｜一歩引いて相手の様子を見よう","凶｜感情的になりやすい日。冷静さを保って"]
  },
  "2026-06-05": {
    date: "2026年6月5日（金）", kyusei: "二黒土星", eto: "戊戌", rokuyo: "先勝",
    special: ["🌸 芒種"],
    koi: ["大吉｜金曜日の夜に向けて動き出して。今夜が勝負","吉｜好きな人から誘いが来るかも","吉｜素直な気持ちを伝えると吉","中吉｜週末に向けて関係が温まる","小吉｜偶然の再会に注意","末吉｜今週の疲れを癒やすことが来週の恋につながる"]
  },
  "2026-06-06": {
    date: "2026年6月6日（土）", kyusei: "一白水星", eto: "己亥", rokuyo: "友引",
    special: [],
    koi: ["大吉｜デートに最高の日。思い出をつくって","大吉｜友引パワーで相手をあなたに引き寄せる","吉｜偶然のような必然の出会いがある","吉｜関係が次のステージへ進む予感","中吉｜一緒に笑える時間が絆になる","小吉｜今日の優しさは必ず届いている"]
  },
  "2026-06-07": {
    date: "2026年6月7日（日）", kyusei: "九紫火星", eto: "庚子", rokuyo: "先負",
    special: [],
    koi: ["大吉｜今週の集大成。勇気を出した人に奇跡が起きる","吉｜直感で動いてOK","中吉｜週末の夜、想いが相手に届く","吉｜新しい週に向けて恋の準備を整えて","小吉｜ゆっくり休むことで運気がリセットされる","末吉｜来週に向けて良い流れが来ている"]
  }
};

async function postKoimikuji() {
  const today = getTodayKey();
  const storageKey = `koimikuji_${today}`;
  const already = await chrome.storage.local.get(storageKey);
  if (already[storageKey]) return;

  const data = FORTUNE_DATA[today];
  if (!data) return;

  const idx = Math.floor(Math.random() * data.koi.length);
  const [label, text] = data.koi[idx].split('｜');
  const specials = data.special.length > 0 ? `\n${data.special.join(' ')}` : '';

  const tweetText =
`📚まちのほんやさん 恋みくじ
${data.date}${specials}

🔮 ${label}
${text}

九星：${data.kyusei} ／ 干支：${data.eto} ／ ${data.rokuyo}

#恋みくじ #占い #恋愛運 #まちのほんやさん`;

  const saved = {};
  saved[storageKey] = true;
  await chrome.storage.local.set(saved);

  chrome.tabs.create({
    url: `https://twitter.com/intent/tweet?autopost=1&text=${encodeURIComponent(tweetText)}`
  });
}

// ===== note記事 自動投稿 =====

async function handleNoteArticle(tabId, url) {
  if (!NOTE_ARTICLE_PATTERN.test(url)) return;
  if (await isAlreadyPosted(url)) return;

  await new Promise(r => setTimeout(r, 2000));

  try {
    await chrome.scripting.executeScript({ target: { tabId }, files: ['content.js'] });
  } catch {}

  chrome.tabs.sendMessage(tabId, { type: 'GET_ARTICLE' }, async (res) => {
    if (chrome.runtime.lastError || !res) return;
    const budget = 255;
    let body = res.intro || res.title || '';
    if (body.length > budget) body = body.slice(0, budget - 1) + '…';
    const tweetText = body + `\n\n${url}`;
    await markAsPosted(url);
    chrome.tabs.create({
      url: `https://twitter.com/intent/tweet?autopost=1&text=${encodeURIComponent(tweetText)}`
    });
  });
}

// ===== アラーム（毎朝7:00 JST に自動投稿） =====

function setupDailyAlarm() {
  chrome.alarms.get('daily-koimikuji', (alarm) => {
    if (!alarm) {
      // 次の07:00 JSTを計算
      const now = new Date();
      const jst = new Date(now.getTime() + 9 * 60 * 60 * 1000);
      const next7 = new Date(jst);
      next7.setUTCHours(22, 0, 0, 0); // JST 07:00 = UTC 22:00
      if (jst.getUTCHours() >= 22) {
        next7.setUTCDate(next7.getUTCDate() + 1);
      }
      chrome.alarms.create('daily-koimikuji', {
        when: next7.getTime() - 9 * 60 * 60 * 1000,
        periodInMinutes: 24 * 60
      });
    }
  });
}

chrome.alarms.onAlarm.addListener((alarm) => {
  if (alarm.name === 'daily-koimikuji') {
    postKoimikuji();
  }
});

// ===== イベントリスナー =====

chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
  if (changeInfo.status === 'complete' && tab.url) {
    handleNoteArticle(tabId, tab.url);
  }
});

// 拡張起動時にアラームをセット
chrome.runtime.onStartup.addListener(setupDailyAlarm);
chrome.runtime.onInstalled.addListener(setupDailyAlarm);
