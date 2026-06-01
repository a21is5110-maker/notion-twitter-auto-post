// Twitter Web Intent ページで投稿ボタンを自動クリック
// URLに autopost=1 が付いている場合のみ動作
if (new URLSearchParams(location.search).get('autopost') === '1') {
  let countdown = 3;

  // カウントダウン表示を画面に追加
  const overlay = document.createElement('div');
  overlay.style.cssText = [
    'position:fixed', 'top:16px', 'left:50%', 'transform:translateX(-50%)',
    'background:#000', 'color:#fff', 'padding:10px 20px', 'border-radius:20px',
    'font-size:14px', 'font-family:sans-serif', 'z-index:99999',
    'box-shadow:0 2px 12px rgba(0,0,0,0.3)'
  ].join(';');
  overlay.textContent = `${countdown}秒後に自動投稿します…`;

  function tryPost() {
    // 「ポストする」「Tweet」ボタンを探す
    const btn =
      document.querySelector('[data-testid="tweetButton"]') ||
      document.querySelector('[data-testid="tweetButtonInline"]') ||
      document.querySelector('div[role="button"][data-testid*="tweet"]') ||
      Array.from(document.querySelectorAll('div[role="button"]'))
        .find(el => el.innerText.match(/^(ポスト|Post|Tweet)$/i));
    if (btn) {
      btn.click();
      overlay.textContent = '投稿しました ✓';
      setTimeout(() => overlay.remove(), 1500);
    } else {
      setTimeout(tryPost, 300);
    }
  }

  // ページ読み込み後に body へ追加
  function init() {
    document.body.appendChild(overlay);
    const timer = setInterval(() => {
      countdown--;
      if (countdown <= 0) {
        clearInterval(timer);
        overlay.textContent = '投稿中…';
        tryPost();
      } else {
        overlay.textContent = `${countdown}秒後に自動投稿します…`;
      }
    }, 1000);
  }

  if (document.body) {
    init();
  } else {
    document.addEventListener('DOMContentLoaded', init);
  }
}
