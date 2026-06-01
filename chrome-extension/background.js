// note.com の記事URLパターン: note.com/*/n/*
const NOTE_ARTICLE_PATTERN = /^https:\/\/note\.com\/[^/]+\/n\/[^/]+/;

// 投稿済みURLを管理（同じ記事を2回投稿しない）
async function isAlreadyPosted(url) {
  const { postedUrls = [] } = await chrome.storage.local.get('postedUrls');
  return postedUrls.includes(url);
}

async function markAsPosted(url) {
  const { postedUrls = [] } = await chrome.storage.local.get('postedUrls');
  if (!postedUrls.includes(url)) {
    postedUrls.push(url);
    // 最大100件まで保持
    if (postedUrls.length > 100) postedUrls.shift();
    await chrome.storage.local.set({ postedUrls });
  }
}

async function handleNoteArticle(tabId, url) {
  if (!NOTE_ARTICLE_PATTERN.test(url)) return;
  if (await isAlreadyPosted(url)) return;

  // ページが完全に読み込まれるまで少し待つ
  await new Promise(r => setTimeout(r, 2000));

  // content.js を inject して記事を取得
  try {
    await chrome.scripting.executeScript({ target: { tabId }, files: ['content.js'] });
  } catch { /* 既にinject済み */ }

  chrome.tabs.sendMessage(tabId, { type: 'GET_ARTICLE' }, async (res) => {
    if (chrome.runtime.lastError || !res) return;

    const MAX_LEN = 280;
    const urlPart = `\n\n${url}`;
    const budget = MAX_LEN - 25;
    let body = res.intro || res.title || '';
    if (body.length > budget) body = body.slice(0, budget - 1) + '…';
    const tweetText = body + urlPart;

    const intentUrl = `https://twitter.com/intent/tweet?autopost=1&text=${encodeURIComponent(tweetText)}`;
    await markAsPosted(url);
    chrome.tabs.create({ url: intentUrl });
  });
}

// タブのURL変化を監視
chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
  if (changeInfo.status === 'complete' && tab.url) {
    handleNoteArticle(tabId, tab.url);
  }
});
