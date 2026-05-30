function extractNoteArticle() {
  // タイトル
  const titleEl =
    document.querySelector('h1.o-noteContentHeader__title') ||
    document.querySelector('h1[class*="title"]') ||
    document.querySelector('h1');
  const title = titleEl ? titleEl.innerText.trim() : document.title;

  // 本文の段落を順に取得して導入部を組み立てる
  const bodySelectors = [
    '.note-common-styles__textnote-body',
    '[class*="textnote-body"]',
    '.p-article__body',
    'article',
  ];

  let bodyEl = null;
  for (const sel of bodySelectors) {
    bodyEl = document.querySelector(sel);
    if (bodyEl) break;
  }

  let intro = '';
  if (bodyEl) {
    const paragraphs = Array.from(bodyEl.querySelectorAll('p')).filter(
      (p) => p.innerText.trim().length > 10
    );
    // 先頭から文字を積み上げて150字以内に収める
    for (const p of paragraphs) {
      const text = p.innerText.trim();
      if ((intro + text).length > 150) {
        const remaining = 150 - intro.length;
        if (remaining > 20) intro += text.slice(0, remaining) + '…';
        break;
      }
      intro += text + '\n';
      if (intro.length >= 100) break;
    }
    intro = intro.trim();
  }

  return { title, intro, url: location.href };
}

// popup.js からのメッセージに応答
chrome.runtime.onMessage.addListener((msg, _sender, sendResponse) => {
  if (msg.type === 'GET_ARTICLE') {
    sendResponse(extractNoteArticle());
  }
});
