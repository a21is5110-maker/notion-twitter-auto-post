// note.com の記事URLパターン
const NOTE_ARTICLE_PATTERN = /^https:\/\/note\.com\/[^/]+\/n\/[^/]+/;
// 恋みくじページのパターン（GitHub Pages or ローカル）
const KOIMIKUJI_PATTERN = /fortune\/index\.html/;

async function isAlreadyPosted(url) {
  const key = url.split('?')[0]; // クエリ除去
  const { postedUrls = [] } = await chrome.storage.local.get('postedUrls');
  return postedUrls.includes(key);
}

async function markAsPosted(url) {
  const key = url.split('?')[0];
  const { postedUrls = [] } = await chrome.storage.local.get('postedUrls');
  if (!postedUrls.includes(key)) {
    postedUrls.push(key);
    if (postedUrls.length > 200) postedUrls.shift();
    await chrome.storage.local.set({ postedUrls });
  }
}

// note記事の自動投稿
async function handleNoteArticle(tabId, url) {
  if (!NOTE_ARTICLE_PATTERN.test(url)) return;
  if (await isAlreadyPosted(url)) return;

  await new Promise(r => setTimeout(r, 2000));

  try {
    await chrome.scripting.executeScript({ target: { tabId }, files: ['content.js'] });
  } catch { /* 既にinject済み */ }

  chrome.tabs.sendMessage(tabId, { type: 'GET_ARTICLE' }, async (res) => {
    if (chrome.runtime.lastError || !res) return;

    const budget = 280 - 25;
    let body = res.intro || res.title || '';
    if (body.length > budget) body = body.slice(0, budget - 1) + '…';
    const tweetText = body + `\n\n${url}`;

    await markAsPosted(url);
    chrome.tabs.create({
      url: `https://twitter.com/intent/tweet?autopost=1&text=${encodeURIComponent(tweetText)}`
    });
  });
}

// 恋みくじの自動日次投稿（1日1回）
async function handleKoimikuji(tabId, url) {
  if (!KOIMIKUJI_PATTERN.test(url)) return;

  const today = getTodayKeyBg();
  const storageKey = `koimikuji_posted_${today}`;
  const result = await chrome.storage.local.get(storageKey);
  if (result[storageKey]) return; // 今日はもう投稿済み

  await new Promise(r => setTimeout(r, 3000));

  // ページからデータを取得してランダムみくじを投稿
  try {
    const [res] = await chrome.scripting.executeScript({
      target: { tabId },
      func: () => {
        if (typeof FORTUNE_DATA === 'undefined') return null;
        const keys = Object.keys(FORTUNE_DATA);
        const now = new Date();
        const jst = new Date(now.getTime() + 9 * 60 * 60 * 1000);
        const key = `${jst.getUTCFullYear()}-${String(jst.getUTCMonth()+1).padStart(2,'0')}-${String(jst.getUTCDate()).padStart(2,'0')}`;
        const data = FORTUNE_DATA[key];
        if (!data) return null;
        const idx = Math.floor(Math.random() * data.koi.length);
        const [label, text] = data.koi[idx].split('｜');
        return { date: data.date, kyusei: data.kyusei, eto: data.eto, rokuyo: data.rokuyo, special: data.special, label, text };
      }
    });

    if (!res || !res.result) return;
    const d = res.result;
    const specials = d.special.length > 0 ? `\n${d.special.join(' ')}` : '';
    const tweetText =
`📚まちのほんやさん 恋みくじ
${d.date}${specials}

🔮 ${d.label}
${d.text}

九星：${d.kyusei} ／ 干支：${d.eto} ／ ${d.rokuyo}

#恋みくじ #占い #恋愛運 #まちのほんやさん`;

    const stored = {};
    stored[storageKey] = true;
    await chrome.storage.local.set(stored);

    chrome.tabs.create({
      url: `https://twitter.com/intent/tweet?autopost=1&text=${encodeURIComponent(tweetText)}`
    });
  } catch (e) {
    console.error('恋みくじ自動投稿エラー:', e);
  }
}

function getTodayKeyBg() {
  const now = new Date();
  const jst = new Date(now.getTime() + 9 * 60 * 60 * 1000);
  return `${jst.getUTCFullYear()}-${String(jst.getUTCMonth()+1).padStart(2,'0')}-${String(jst.getUTCDate()).padStart(2,'0')}`;
}

// タブのURL変化を監視
chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
  if (changeInfo.status === 'complete' && tab.url) {
    handleNoteArticle(tabId, tab.url);
    handleKoimikuji(tabId, tab.url);
  }
});
