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

  // --- Responsive Hamburger Menu Toggle ---
  const hamburgerBtn = document.getElementById('hamburger-btn');
  const mobileDrawer = document.getElementById('mobile-nav-drawer');
  const mobileBackdrop = document.getElementById('mobile-nav-backdrop');

  function openMobileMenu() {
    if (!mobileDrawer || !hamburgerBtn) return;
    hamburgerBtn.classList.add('is-active');
    hamburgerBtn.setAttribute('aria-expanded', 'true');
    mobileDrawer.classList.add('is-open');
    mobileDrawer.setAttribute('aria-hidden', 'false');
    if (mobileBackdrop) mobileBackdrop.classList.add('is-open');
    document.body.style.overflow = 'hidden';
  }

  function closeMobileMenu() {
    if (!mobileDrawer || !hamburgerBtn) return;
    hamburgerBtn.classList.remove('is-active');
    hamburgerBtn.setAttribute('aria-expanded', 'false');
    mobileDrawer.classList.remove('is-open');
    mobileDrawer.setAttribute('aria-hidden', 'true');
    if (mobileBackdrop) mobileBackdrop.classList.remove('is-open');
    document.body.style.overflow = '';
  }

  if (hamburgerBtn && mobileDrawer) {
    hamburgerBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      const isOpen = mobileDrawer.classList.contains('is-open');
      if (isOpen) {
        closeMobileMenu();
      } else {
        openMobileMenu();
      }
    });

    if (mobileBackdrop) {
      mobileBackdrop.addEventListener('click', closeMobileMenu);
    }

    // Close on clicking any link inside the mobile drawer
    mobileDrawer.querySelectorAll('a').forEach(link => {
      link.addEventListener('click', closeMobileMenu);
    });

    // Close on Escape
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && mobileDrawer.classList.contains('is-open')) {
        closeMobileMenu();
      }
    });
  }
});

// --- Post & Teaser Inline Expander (Rozwijanie wpisów i zajawek) ---
function togglePostExpand(containerId, btn) {
  const container = document.getElementById(containerId);
  if (!container) return;
  const excerpt = container.querySelector('.excerpt-preview');
  const full = container.querySelector('.full-content');
  const expandLabel = btn ? btn.querySelector('.btn-label-expand') : null;
  const collapseLabel = btn ? btn.querySelector('.btn-label-collapse') : null;

  if (!full) return;

  const isExpanded = full.style.display !== 'none';
  if (isExpanded) {
    full.style.display = 'none';
    if (excerpt) excerpt.style.display = 'block';
    if (btn) btn.setAttribute('aria-expanded', 'false');
    if (expandLabel) expandLabel.style.display = 'inline';
    if (collapseLabel) collapseLabel.style.display = 'none';
    container.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
  } else {
    full.style.display = 'block';
    if (excerpt) excerpt.style.display = 'none';
    if (btn) btn.setAttribute('aria-expanded', 'true');
    if (expandLabel) expandLabel.style.display = 'none';
    if (collapseLabel) collapseLabel.style.display = 'inline';
  }
}

// --- In-place Articles Stream Expander (Rozwijanie kolejnych wpisów w strumieniu bez skakania po stronie) ---
function toggleExtraPosts(btn) {
  const stream = document.getElementById('extra-articles-stream');
  if (!stream) {
    toggleCatalog(btn);
    return;
  }
  const isExpanded = stream.style.display !== 'none';
  const expandLabel = btn ? btn.querySelector('.catalog-btn-expand') : null;
  const collapseLabel = btn ? btn.querySelector('.catalog-btn-collapse') : null;

  if (isExpanded) {
    stream.style.display = 'none';
    if (btn) btn.setAttribute('aria-expanded', 'false');
    if (expandLabel) expandLabel.style.display = 'inline';
    if (collapseLabel) collapseLabel.style.display = 'none';
    if (btn) btn.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
  } else {
    stream.style.display = 'block';
    if (btn) btn.setAttribute('aria-expanded', 'true');
    if (expandLabel) expandLabel.style.display = 'none';
    if (collapseLabel) collapseLabel.style.display = 'inline';
  }
}

// --- Catalog Section Expander (Zabezpieczony fallback bez niechcianych skoków) ---
function toggleCatalog(btn) {
  const catalog = document.getElementById('katalog-publikacji');
  if (!catalog) return;
  const isExpanded = catalog.style.display !== 'none';
  const expandLabel = btn ? btn.querySelector('.catalog-btn-expand') : null;
  const collapseLabel = btn ? btn.querySelector('.catalog-btn-collapse') : null;

  if (isExpanded) {
    catalog.style.display = 'none';
    if (btn) btn.setAttribute('aria-expanded', 'false');
    if (expandLabel) expandLabel.style.display = 'inline';
    if (collapseLabel) collapseLabel.style.display = 'none';
  } else {
    catalog.style.display = 'block';
    if (btn) btn.setAttribute('aria-expanded', 'true');
    if (expandLabel) expandLabel.style.display = 'none';
    if (collapseLabel) collapseLabel.style.display = 'inline';
  }
}

window.togglePostExpand = togglePostExpand;
window.toggleExtraPosts = toggleExtraPosts;
window.toggleCatalog = toggleCatalog;

// Auto-expand catalog if direct anchor in URL
window.addEventListener('DOMContentLoaded', () => {
  if (window.location.hash === '#katalog-publikacji') {
    const cat = document.getElementById('katalog-publikacji');
    const catBtn = document.getElementById('btn-toggle-catalog');
    if (cat && catBtn) {
      toggleCatalog(catBtn);
    }
  }
});

