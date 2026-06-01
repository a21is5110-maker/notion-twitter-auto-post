function extractNoteArticle() {
  // タイトル（複数セレクターで試みる）
  const titleEl =
    document.querySelector('h1.o-noteContentHeader__title') ||
    document.querySelector('h1[class*="title"]') ||
    document.querySelector('h1[class*="Title"]') ||
    document.querySelector('h1[class*="header"]') ||
    document.querySelector('h1');
  const title = titleEl ? titleEl.innerText.trim() : document.title.replace(' | note', '').trim();

  // 本文エリアを広いセレクターで探す
  const bodySelectors = [
    '.note-common-styles__textnote-body',
    '[class*="textnote-body"]',
    '[class*="noteBody"]',
    '[class*="articleBody"]',
    '[class*="article-body"]',
    '[class*="article_body"]',
    '[class*="content-body"]',
    '[class*="contentBody"]',
    '.p-article__body',
    '[class*="p-article"]',
    'article .content',
    'article section',
    'article',
    'main',
  ];

  let bodyEl = null;
  for (const sel of bodySelectors) {
    const el = document.querySelector(sel);
    if (el && el.innerText.trim().length > 50) {
      bodyEl = el;
      break;
    }
  }

  let intro = '';
  if (bodyEl) {
    // p タグを試みる
    let paragraphs = Array.from(bodyEl.querySelectorAll('p')).filter(
      (p) => p.innerText.trim().length > 10
    );

    // p タグがない場合は div 等テキストノードを持つ要素を使う
    if (paragraphs.length === 0) {
      paragraphs = Array.from(bodyEl.querySelectorAll('div, span')).filter(
        (el) => el.children.length === 0 && el.innerText.trim().length > 10
      );
    }

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

    // それでも取れない場合は本文全体の先頭150字
    if (!intro) {
      intro = bodyEl.innerText.trim().slice(0, 150);
      if (bodyEl.innerText.trim().length > 150) intro += '…';
    }
  }

  return { title, intro, url: location.href };
}

// popup.js からのメッセージに応答
chrome.runtime.onMessage.addListener((msg, _sender, sendResponse) => {
  if (msg.type === 'GET_ARTICLE') {
    sendResponse(extractNoteArticle());
  }
});
