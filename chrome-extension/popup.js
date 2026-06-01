const MAX_LEN = 280;

const titleEl   = document.getElementById('title');
const tweetArea = document.getElementById('tweet-text');
const counter   = document.getElementById('counter');
const errorEl   = document.getElementById('error');
const status    = document.getElementById('status');

function updateCounter() {
  const len = tweetArea.value.length;
  counter.textContent = `${len} / ${MAX_LEN}`;
  counter.className = 'counter' + (len > MAX_LEN ? ' over' : '');
}

function buildTweet(title, intro, url) {
  const urlPart = `\n\n${url}`;
  const budget  = MAX_LEN - 25;
  let body = (intro && intro.length > 0) ? intro : title;
  if (!body) body = '記事を読む';
  if (body.length > budget) body = body.slice(0, budget - 1) + '…';
  return body + urlPart;
}

async function loadArticle() {
  errorEl.style.display = 'none';
  titleEl.textContent = '読み込み中…';
  tweetArea.value = '';
  status.textContent = '';
  updateCounter();

  let tabs;
  try {
    tabs = await chrome.tabs.query({ active: true, currentWindow: true });
  } catch {
    showError('タブ情報を取得できませんでした。');
    return;
  }

  const tab = tabs[0];
  const pageUrl = tab?.url || '';

  if (!pageUrl.includes('note.com')) {
    showError('note.com の記事ページを開いた状態でご利用ください。');
    titleEl.textContent = '—';
    return;
  }

  // タブのURLとタイトルをまず使ってツイート文を作る（確実に表示）
  const pageTitle = tab.title ? tab.title.replace(/\s*[\|｜]\s*note.*$/, '').trim() : '';
  titleEl.textContent = pageTitle || pageUrl;
  tweetArea.value = buildTweet(pageTitle, '', pageUrl);
  updateCounter();

  // content.jsで本文の導入部も取得して上書き
  try {
    await chrome.scripting.executeScript({ target: { tabId: tab.id }, files: ['content.js'] });
  } catch {}

  chrome.tabs.sendMessage(tab.id, { type: 'GET_ARTICLE' }, (res) => {
    if (chrome.runtime.lastError || !res) return; // 失敗してもURLだけのツイートが既に入っている
    if (res.title) titleEl.textContent = res.title;
    // URLは必ずtab.urlを使う（確実）
    tweetArea.value = buildTweet(res.title || pageTitle, res.intro, pageUrl);
    updateCounter();
  });
}

function showError(msg) {
  errorEl.textContent = msg;
  errorEl.style.display = 'block';
}

document.getElementById('btn-reload').addEventListener('click', loadArticle);
tweetArea.addEventListener('input', updateCounter);

document.getElementById('btn-tweet').addEventListener('click', () => {
  const text = tweetArea.value.trim();
  if (!text) return;
  if (text.length > MAX_LEN) {
    showError(`${text.length - MAX_LEN}文字オーバーです。`);
    return;
  }
  chrome.tabs.create({ url: `https://twitter.com/intent/tweet?autopost=1&text=${encodeURIComponent(text)}` });
  status.textContent = '3秒後に自動投稿します ✓';
});

document.getElementById('btn-koimikuji').addEventListener('click', () => {
  const koiStatus = document.getElementById('koi-status');
  koiStatus.textContent = '投稿中…';
  chrome.runtime.sendMessage({ type: 'POST_KOIMIKUJI_NOW' }, (res) => {
    koiStatus.textContent = res?.ok ? '✓ 3秒後に自動投稿されます' : (res?.msg || 'エラーが発生しました');
  });
});

loadArticle();
