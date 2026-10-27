document.addEventListener('DOMContentLoaded', () => {
  // --- Dark / Light Theme Toggle (Domyślnie JASNY) ---
  const themeToggle = document.getElementById('theme-toggle');
  const savedTheme = localStorage.getItem('blog-theme') || 'light';
  
  function applyTheme(theme) {
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('blog-theme', theme);
    if (themeToggle) {
      if (theme === 'dark') {
        themeToggle.setAttribute('title', 'Przełącz na motyw jasny');
        themeToggle.setAttribute('aria-label', 'Przełącz na motyw jasny');
        themeToggle.innerHTML = '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="5"></circle><line x1="12" y1="1" x2="12" y2="3"></line><line x1="12" y1="21" x2="12" y2="23"></line><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"></line><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"></line><line x1="1" y1="12" x2="3" y2="12"></line><line x1="21" y1="12" x2="23" y2="12"></line><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"></line><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"></line></svg>';
      } else {
        themeToggle.setAttribute('title', 'Przełącz na motyw ciemny');
        themeToggle.setAttribute('aria-label', 'Przełącz na motyw ciemny');
        themeToggle.innerHTML = '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path></svg>';
      }
    }
  }
  
  applyTheme(savedTheme);
  
  if (themeToggle) {
    themeToggle.addEventListener('click', () => {
      const current = document.documentElement.getAttribute('data-theme') || 'light';
      applyTheme(current === 'dark' ? 'light' : 'dark');
    });
  }

  // --- Reading Progress Bar ---
  const progressBar = document.getElementById('reading-progress');
  const articleContent = document.querySelector('.article-body');
  
  if (progressBar && articleContent) {
    window.addEventListener('scroll', () => {
      const totalHeight = articleContent.clientHeight;
      const contentTop = articleContent.offsetTop;
      const scrollPos = window.scrollY - contentTop;
      
      if (scrollPos <= 0) {
        progressBar.style.width = '0%';
      } else {
        const progress = Math.min(100, Math.max(0, (scrollPos / (totalHeight - window.innerHeight + 300)) * 100));
        progressBar.style.width = progress + '%';
      }
    });
  }

  // --- Quick Share Button ---
  const shareBtn = document.getElementById('btn-share');
  if (shareBtn) {
    shareBtn.addEventListener('click', async () => {
      if (navigator.share) {
        try {
          await navigator.share({
            title: document.title,
            url: window.location.href
          });
        } catch (e) {
          // canceled
        }
      } else {
        navigator.clipboard.writeText(window.location.href);
        const originalText = shareBtn.innerText;
        shareBtn.innerText = 'Skopiowano link!';
        setTimeout(() => shareBtn.innerText = originalText, 2500);
      }
    });
  }

  // --- Cookie Consent Banner & Preferences ---
  initCookieConsent();
});

const COOKIE_STORAGE_KEY = 'laika_cookie_consent';

function getCookieConsent() {
  try {
    const val = localStorage.getItem(COOKIE_STORAGE_KEY);
    return val ? JSON.parse(val) : null;
  } catch (e) {
    return null;
  }
}

function setCookieConsent(preferences) {
  try {
    localStorage.setItem(COOKIE_STORAGE_KEY, JSON.stringify({
      ...preferences,
      timestamp: Date.now()
    }));
  } catch (e) {}
  hideCookieBanner();
  closeCookieSettingsModal();
}

function acceptAllCookies() {
  setCookieConsent({ necessary: true, analytics: true });
}

function acceptNecessaryCookies() {
  setCookieConsent({ necessary: true, analytics: false });
}

function saveCookieCustomPreferences() {
  const analytics = document.getElementById('pref-analytics')?.checked || false;
  setCookieConsent({ necessary: true, analytics: analytics });
}

function hideCookieBanner() {
  const b = document.getElementById('cookie-banner');
  if (b) b.style.display = 'none';
}

function openCookieBanner() {
  openCookieSettingsModal();
}

function openCookieSettingsModal() {
  const modal = document.getElementById('cookie-modal');
  const backdrop = document.getElementById('cookie-modal-backdrop');
  const consent = getCookieConsent();
  const analyticsCb = document.getElementById('pref-analytics');
  if (analyticsCb) {
    analyticsCb.checked = consent ? !!consent.analytics : true;
  }
  if (modal) modal.style.display = 'block';
  if (backdrop) backdrop.style.display = 'block';
}

function closeCookieSettingsModal() {
  const modal = document.getElementById('cookie-modal');
  const backdrop = document.getElementById('cookie-modal-backdrop');
  if (modal) modal.style.display = 'none';
  if (backdrop) backdrop.style.display = 'none';
}

function initCookieConsent() {
  const consent = getCookieConsent();
  if (!consent) {
    const b = document.getElementById('cookie-banner');
    if (b) b.style.display = 'block';
  }
}

// Global functions for inline HTML event handlers
window.acceptAllCookies = acceptAllCookies;
window.acceptNecessaryCookies = acceptNecessaryCookies;
window.openCookieSettingsModal = openCookieSettingsModal;
window.closeCookieSettingsModal = closeCookieSettingsModal;
window.saveCookieCustomPreferences = saveCookieCustomPreferences;
window.openCookieBanner = openCookieBanner;

