document.addEventListener('DOMContentLoaded', () => {
  // --- Dark / Light Theme Toggle ---
  const themeToggle = document.getElementById('theme-toggle');
  const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
  const savedTheme = localStorage.getItem('blog-theme') || (prefersDark ? 'dark' : 'light');
  
  function applyTheme(theme) {
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('blog-theme', theme);
    if (themeToggle) {
      themeToggle.innerHTML = theme === 'dark' 
        ? '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="5"></circle><line x1="12" y1="1" x2="12" y2="3"></line><line x1="12" y1="21" x2="12" y2="23"></line><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"></line><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"></line><line x1="1" y1="12" x2="3" y2="12"></line><line x1="21" y1="12" x2="23" y2="12"></line><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"></line><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"></line></svg>' 
        : '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path></svg>';
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
});
