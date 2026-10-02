// ==UserScript==
// @name         SondeR Cat - Web AI Connector (Brave Browser)
// @namespace    https://github.com/Verisonder/SondeR-Cat
// @version      1.3.0
// @description  Menghubungkan Web AI (ChatGPT, Claude, Gemini, DeepSeek, Antigravity, Z.ai, Hermes, Brave Leo) ke kucing desktop SondeR Cat (Michan).
// @author       Verisonder / Antigravity
// @match        https://chatgpt.com/*
// @match        https://chat.openai.com/*
// @match        https://claude.ai/*
// @match        https://gemini.google.com/*
// @match        https://chat.deepseek.com/*
// @match        https://search.brave.com/*
// @match        https://*.z.ai/*
// @match        https://z.ai/*
// @match        https://hermes.nousresearch.com/*
// @match        https://*.nousresearch.com/*
// @match        http://localhost:*/*
// @match        http://127.0.0.1:*/*
// @grant        GM_xmlhttpRequest
// @connect      127.0.0.1
// @connect      localhost
// @run-at       document-idle
// ==/UserScript==

(function () {
  'use strict';

  const SONDER_URL = 'http://127.0.0.1:19842/agent';
  let isThinking = false;
  let debounceTimer = null;
  let maxThinkingTimeout = null;

  function getAiLabel() {
    const host = window.location.hostname;
    const title = (document.title || '').toLowerCase();

    // Deteksi Antigravity (jika dibuka di web / IDE webview)
    if (title.includes('antigravity') || host.includes('antigravity')) return 'Antigravity';

    if (host.includes('claude.ai')) return 'Claude';
    if (host.includes('chatgpt.com') || host.includes('openai.com')) return 'ChatGPT';
    if (host.includes('gemini.google.com')) return 'Gemini';
    if (host.includes('deepseek.com')) return 'DeepSeek';
    if (host.includes('z.ai')) return 'Z.ai';
    if (host.includes('nousresearch.com') || host.includes('hermes')) return 'Hermes';
    if (host.includes('brave.com')) return 'Brave Leo';
    return null;
  }

  function notifyCat(state) {
    const label = getAiLabel();
    if (!label && state !== 'clear') return;
    const payload = JSON.stringify({ state, label: label || 'Agent' });

    // Method 1: GM_xmlhttpRequest if available
    if (typeof GM_xmlhttpRequest !== 'undefined') {
      GM_xmlhttpRequest({
        method: 'POST',
        url: SONDER_URL,
        headers: { 'Content-Type': 'application/json' },
        data: payload,
        onload: () => console.log(`[SondeR Cat] Status sent: ${state} (${label})`),
        onerror: () => console.warn('[SondeR Cat] Failed to reach local desktop cat webhook.')
      });
    } else {
      // Method 2: Standard fetch
      fetch(SONDER_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: payload
      }).catch(() => console.warn('[SondeR Cat] Desktop cat webhook unreachable.'));
    }
  }

  function checkStreaming() {
    const host = window.location.hostname;
    const label = getAiLabel();
    if (!label) return;

    let generating = false;

    if (label === 'Antigravity') {
      generating = !!document.querySelector(
        '.generating, .streaming, [data-status="generating"], button[aria-label*="Stop"]'
      );
    } else if (host.includes('chatgpt.com') || host.includes('openai.com')) {
      generating = !!document.querySelector(
        'button[data-testid="stop-button"], button[aria-label*="Stop"], .result-streaming'
      );
    } else if (host.includes('claude.ai')) {
      generating = !!document.querySelector(
        'button[aria-label*="Stop Response"], button[aria-label*="Stop generating"], [data-testid="stop-generating"]'
      );
    } else if (host.includes('gemini.google.com')) {
      generating = !!document.querySelector(
        'button[aria-label*="Stop response"], button[aria-label*="Hentikan respons"], .animating, [data-test-id="stop-button"]'
      );
    } else if (host.includes('deepseek.com')) {
      generating = !!document.querySelector(
        '.ds-icon-button[aria-label*="Stop"], button[class*="stop"]'
      );
    } else if (host.includes('z.ai')) {
      // Selektor presisi untuk Z.ai (menghindari false positive button:has(rect))
      generating = !!document.querySelector(
        'button[aria-label*="Stop generating" i], button[aria-label="Stop" i], button[aria-label*="Hentikan" i], [data-testid*="stop-button"], .chat-streaming'
      );
    } else if (host.includes('nousresearch.com') || host.includes('hermes')) {
      generating = !!document.querySelector(
        'button[aria-label*="Stop" i], button[aria-label*="Hentikan" i], [data-testid*="stop-button"], .chat-streaming'
      );
    } else if (host.includes('brave.com')) {
      generating = !!document.querySelector(
        '[data-testid*="leo-generating"], [class*="leo-streaming"]'
      );
    }

    if (generating !== isThinking) {
      isThinking = generating;
      notifyCat(isThinking ? 'working' : 'done');

      // Watchdog pengaman: jika status thinking bertahan lebih dari 90 detik, otomatis reset
      if (maxThinkingTimeout) clearTimeout(maxThinkingTimeout);
      if (isThinking) {
        maxThinkingTimeout = setTimeout(() => {
          if (isThinking) {
            isThinking = false;
            notifyCat('done');
          }
        }, 90000);
      }
    }
  }

  // Bersihkan status saat tab ditutup atau berpindah halaman
  window.addEventListener('beforeunload', () => {
    if (isThinking) notifyCat('done');
  });
  window.addEventListener('pagehide', () => {
    if (isThinking) notifyCat('done');
  });

  // Observe DOM mutations dengan debouncing
  const observer = new MutationObserver(() => {
    if (debounceTimer) clearTimeout(debounceTimer);
    debounceTimer = setTimeout(checkStreaming, 250);
  });

  observer.observe(document.body, {
    childList: true,
    subtree: true,
    attributes: true,
    attributeFilter: ['aria-label', 'data-testid', 'class', 'disabled', 'title']
  });

  console.log(`[SondeR Cat v1.3.0] Web connector active for ${getAiLabel() || 'web page'}!`);
})();
