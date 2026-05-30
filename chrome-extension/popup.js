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
  // URL は Twitter内部で自動的に23文字扱い
  const urlPart = `\n\n${url}`;
  const urlLen  = 23 + 2; // 改行2文字 + URL23文字
  const budget  = MAX_LEN - urlLen;

  let body = intro || title;
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
  if (!tab || !tab.url || !tab.url.includes('note.com')) {
    showError('note.com の記事ページを開いた状態でご利用ください。');
    titleEl.textContent = '—';
    return;
  }

  try {
    // content script が確実に存在するよう inject する
    await chrome.scripting.executeScript({
      target: { tabId: tab.id },
      files: ['content.js'],
    });
  } catch {
    // 既に inject 済みの場合はエラーになるので無視
  }

  chrome.tabs.sendMessage(tab.id, { type: 'GET_ARTICLE' }, (res) => {
    if (chrome.runtime.lastError || !res) {
      showError('記事データを取得できませんでした。ページを再読み込みして再度お試しください。');
      return;
    }
    titleEl.textContent = res.title || '（タイトル不明）';
    tweetArea.value = buildTweet(res.title, res.intro, res.url);
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
    showError(`${text.length - MAX_LEN}文字オーバーです。ツイート文を短くしてください。`);
    return;
  }
  const url = `https://twitter.com/intent/tweet?text=${encodeURIComponent(text)}`;
  chrome.tabs.create({ url });
  status.textContent = 'Xの投稿画面を開きました ✓';
});

loadArticle();
